from flask import Flask, render_template, request
from tinydb import TinyDB, Query


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

db=TinyDB('caminhos.json')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/caminhos")
def caminhos():
    caminhos = db.all()
    return render_template("caminhos.html", caminhos=caminhos)

@app.route("/caminhos/novo", methods=["GET", "POST"])
def novo_caminho():
    if request.method == "POST":
        busca = Query()
        id = db.search(Query().id.exists())[-1]['id']
        db.insert({"id": id, "caminho": request.form})
        return "Caminho adicionado com sucesso!<a href='/caminhos'>Voltar</a>"
    return render_template("novo.html")

@app.route("/caminhos/atualizar", methods=["GET", "POST"])
def editar_caminho():
    if request.method == "POST":
        return render_template("editar.html")
    return render_template("atualizar.html")

@app.route("/caminhos/editar", methods=["GET", "POST"])
def editar_caminho():
    if request.method == "POST":
        db.update(request.form, doc_ids= request.form["id"])
        return "Caminho atualizado com sucesso!<a href='/caminhos'>Voltar</a>"
    caminho_a_editar = db.get(doc_id= request.form["id"])
    return render_template("editar.html", caminho = caminho_a_editar)

@app.route("/caminhos/deletar/", methods=["GET", "POST"])
def deletar_caminho():
    if request.method == "POST":
        db.remove(doc_ids= request.form["id"])
        return "Caminho deletado com sucesso!<a href='/caminhos'>Voltar</a>"
    return render_template("deletar.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)