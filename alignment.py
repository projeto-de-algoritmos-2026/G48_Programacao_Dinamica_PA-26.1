import re
import unicodedata

# Pesos do alinhamento
MATCH = 1       # palavras iguais
MISMATCH = -1   # palavras diferentes (substituicao)
GAP = -1        # insercao/remocao (lacuna)


def normalizar(token: str) -> str:
    """Minusculas + remove acentos, para comparar palavras de forma justa."""
    token = token.lower()
    nfkd = unicodedata.normalize("NFKD", token)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def tokenizar(texto: str):
    """Quebra o texto em palavras (mantem a forma original p/ exibir)."""
    brutos = re.findall(r"\w+", texto, flags=re.UNICODE)
    return brutos


def alinhar(texto_a: str, texto_b: str):
    """
    Roda Needleman-Wunsch iterativo sobre as palavras dos dois textos.

    Retorna dict com:
      - tokens_a, tokens_b: listas de palavras
      - matriz: tabela de PD (n+1 x m+1)
      - alinhamento: lista de (palavra_a | None, palavra_b | None, tipo)
      - similaridade: 0..100 (%)
      - score: pontuacao final do alinhamento
      - matches: numero de palavras casadas
    """
    tokens_a = tokenizar(texto_a)
    tokens_b = tokenizar(texto_b)
    na, nb = len(tokens_a), len(tokens_b)

    norm_a = [normalizar(t) for t in tokens_a]
    norm_b = [normalizar(t) for t in tokens_b]

    # --- Preenchimento ITERATIVO da matriz de PD ---
    # m[i][j] = melhor score alinhando os primeiros i tokens de A
    #           com os primeiros j tokens de B.
    m = [[0] * (nb + 1) for _ in range(na + 1)]

    for i in range(1, na + 1):
        m[i][0] = i * GAP          # so lacunas: gastou i remocoes
    for j in range(1, nb + 1):
        m[0][j] = j * GAP          # so lacunas: gastou j insercoes

    for i in range(1, na + 1):
        for j in range(1, nb + 1):
            custo = MATCH if norm_a[i - 1] == norm_b[j - 1] else MISMATCH
            diag = m[i - 1][j - 1] + custo   # casar/substituir
            cima = m[i - 1][j] + GAP         # remover de A
            esq = m[i][j - 1] + GAP          # inserir de B
            m[i][j] = max(diag, cima, esq)

    alinhamento = []
    i, j = na, nb
    matches = 0
    caminho = {(i, j)}            # celulas (i,j) visitadas no traceback
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            custo = MATCH if norm_a[i - 1] == norm_b[j - 1] else MISMATCH
            if m[i][j] == m[i - 1][j - 1] + custo:
                tipo = "match" if custo == MATCH else "mismatch"
                if tipo == "match":
                    matches += 1
                alinhamento.append((tokens_a[i - 1], tokens_b[j - 1], tipo))
                i -= 1
                j -= 1
                caminho.add((i, j))
                continue
        if i > 0 and m[i][j] == m[i - 1][j] + GAP:
            alinhamento.append((tokens_a[i - 1], None, "gap_b"))
            i -= 1
            caminho.add((i, j))
            continue
        # resta lacuna em A
        alinhamento.append((None, tokens_b[j - 1], "gap_a"))
        j -= 1
        caminho.add((i, j))

    alinhamento.reverse()

    # Similaridade: casamentos sobre o texto mais longo (0..100%)
    denom = max(na, nb) or 1
    similaridade = round(100.0 * matches / denom, 1)

    # caminho como lista de listas (i,j) p/ consulta facil no template
    caminho_lista = sorted(caminho)

    return {
        "tokens_a": tokens_a,
        "tokens_b": tokens_b,
        "matriz": m,
        "caminho": caminho_lista,
        "alinhamento": alinhamento,
        "similaridade": similaridade,
        "score": m[na][nb],
        "matches": matches,
    }