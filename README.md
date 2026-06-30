# Detector de Plágio

Número da Lista: 48<br>
Conteúdo da Disciplina: Programação Dinâmica<br>

**Apresentação:** -

## Alunos

| Matrícula  | Aluno                    |
| ---------- | ------------------------ |
| 23/1034082 | ARTUR HANDOW KRAUSPENHAR |
| 21/1031593 | ANDRE LOPES DE SOUSA     |

## Sobre

Aplicação web (Flask) que **detecta plágio entre dois textos** usando o
algoritmo de **Alinhamento de Sequência (Needleman-Wunsch)**, implementado
de forma **iterativa** (preenchimento de matriz de Programação Dinâmica +
*traceback*).

Cada texto é tokenizado em palavras (normalizadas: minúsculas e sem acento).
O algoritmo alinha globalmente as duas sequências de palavras e classifica
cada posição como:

- **igual** — palavra copiada (casamento),
- **substituído** — palavra trocada por outra (*mismatch*),
- **só em A / só em B** — palavra inserida ou removida (lacuna/*gap*).

A partir do alinhamento, calcula uma **similaridade (%)** e dá um veredito
(baixo / moderado / forte indício de plágio).

### Por que Programação Dinâmica?

O alinhamento ótimo é construído resolvendo subproblemas menores e
combinando-os. A recorrência usada (iterativa) é:

```
m[i][j] = max(
    m[i-1][j-1] + (match se A[i]==B[j] senão mismatch),  # casar / substituir
    m[i-1][j]   + gap,                                    # remover de A
    m[i][j-1]   + gap                                     # inserir de B
)
```

Pesos: match = +1, mismatch = −1, gap = −1.

## Screenshots

> Adicionar 3 screenshots: (1) tela inicial com os dois textos,
> (2) resultado com gauge de similaridade,
> (3) alinhamento palavra a palavra destacado.

## Instalação

Linguagem: Python 3<br>
Framework: Flask<br>

```bash
pip install -r requirements.txt
```

## Uso

```bash
python app.py
```

Abra o navegador em **http://localhost:5000**, cole os dois textos e clique
em **Comparar textos**.

## Outros

- `alignment.py` — algoritmo Needleman-Wunsch iterativo (motor).
- `app.py` — servidor Flask e rotas.
- `templates/index.html` + `static/style.css` — interface.