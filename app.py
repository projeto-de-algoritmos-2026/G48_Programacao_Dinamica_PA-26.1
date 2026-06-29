from flask import Flask, render_template, request

from alignment import alinhar

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    texto_a = ""
    texto_b = ""

    if request.method == "POST":
        texto_a = request.form.get("texto_a", "")
        texto_b = request.form.get("texto_b", "")
        if texto_a.strip() and texto_b.strip():
            resultado = alinhar(texto_a, texto_b)

    return render_template(
        "index.html",
        resultado=resultado,
        texto_a=texto_a,
        texto_b=texto_b,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
