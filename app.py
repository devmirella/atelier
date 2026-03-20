from flask import Flask, render_template, jsonify, request
import json
import os
from pathlib import Path
from werkzeug.utils import secure_filename # secure_filename → função do Flask que limpa o nome do arquivo
from extensoes import db
from models import Inspiracao, Arte, Exposed, ArteInterna


app = Flask(__name__)

# Configuração de UPLOAD
UPLOAD_FOLDER = os.path.join("static", "images")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER 


# Configuração do banco de dados 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///atelier.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa o banco de dados com o app
db.init_app(app)

# Cria as tabelas no banco se ainda não existem
with app.app_context():
    db.create_all()


# Função auxiliar: verificar extensão
def extensao_permitida(nome_arquivo):
    return "." in nome_arquivo and \
    nome_arquivo.rsplit(".", 1)[-1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/arte")
def arte():
    
    # Busca todas as artes no banco de dados
    artes = Arte.query.all()
    lista = [{"id": a.id, "imagem": a.imagem} for a in artes]

    return render_template("arte.html", artes=lista)


@app.route("/arte/adicionar", methods=["POST"])
def adicionar_arte():
   
    if "imagem" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    arquivo = request.files["imagem"] # pega o arquivo do dicionário, é um objeto FileStorage do Flask
    
    if arquivo.filename == "":
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400
    
    if not extensao_permitida(arquivo.filename):
        return jsonify({"erro": "Tipo de arquivo não permitido"}), 400

    nome_seguro = secure_filename(arquivo.filename) # Limpa o nome do arquivo
    caminho_arquivo = os.path.join(app.config["UPLOAD_FOLDER"], nome_seguro)
    arquivo.save(caminho_arquivo)
    caminho_imagem = f"/static/images/{nome_seguro}"

    # Cria um novo objeto arte e salva no banco
    nova = Arte(imagem=caminho_imagem)
    db.session.add(nova)
    db.session.commit()

    return jsonify({"id": nova.id, "imagem": nova.imagem}), 201

@app.route("/arte/apagar", methods=["POST"])
def apagar_arte():
   
    dados = request.get_json()

    if not dados or "id" not in dados:
        return jsonify({"erro": "ID é obrigatório"}), 400

    # Busca a arte no banco pelo id
    arte = Arte.query.get(dados["id"])

    if not arte:
        return jsonify({"erro": "Arte não encontrada"}), 404
    
    db.session.delete(arte)
    db.session.commit()

    # Retorna sucesso como true e status 200 (requisição OK)
    return jsonify({"sucesso": True}), 200


@app.route("/exposed")
def exposed():

    itens = Exposed.query.all()

    # Converte para dicionário incluindo as artes internas
    lista = []
    for item in itens:
        lista.append({
            "id": item.id, 
            "imagem": item.imagem,
            "titulo": item.titulo,
            "tag": item.tag,
            "artes": [a.imagem for a in item.artes]        
        })

    return render_template("exposed.html", exposed=lista)

@app.route("/exposed/adicionar", methods=["POST"])
def adicionar_exposed():
    

    if "imagem" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    arquivo = request.files["imagem"]

    if arquivo.filename == "":
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400
    
    if not extensao_permitida(arquivo.filename):
        return jsonify({"erro": "Tipo de arquivo não permitido"}), 400
    
    nome_seguro = secure_filename(arquivo.filename)
    caminho_arquivo = os.path.join(app.config["UPLOAD_FOLDER"], nome_seguro)
    arquivo.save(caminho_arquivo)
    caminho_imagem = f"/static/images/{nome_seguro}"

    titulo = request.form.get("titulo", "")
    tag = request.form.get("tag", "")

    # Cria novo card do exposed no banco
    novo = Exposed(imagem=caminho_imagem, titulo=titulo, tag=tag)
    db.session.add(novo)
    db.session.commit()

    return jsonify({
        "id": novo.id,
        "imagem": novo.imagem,
        "titulo": novo.titulo,
        "tag": novo.tag,
        "artes": []
    }), 201



@app.route("/exposed/apagar", methods=["POST"])
def apagar_exposed(): # Define a função Python que será chamada quando a rota for acessada.

    dados = request.get_json()

    # Validação básica
    if not dados or "id" not in dados:
        return jsonify({"erro": "ID é obrigatório"}), 400
    
    item = Exposed.query.get(dados["id"])

    if not item:
        return jsonify({"erro": "Item não encontrado"}), 404
    
    db.session.delete(item)
    db.session.commit()

    return jsonify({"sucesso": True}), 200

@app.route("/exposed/adicionar-arte", methods=["POST"])
def adicionar_arte_exposed():

    
    id_card = request.form.get("id") 
    if not id_card:
        return jsonify({"erro": "ID do card é obrigatório"}), 400
    
    if "imagem" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    arquivo = request.files["imagem"]

    if arquivo.filename == "":
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400
    
    if not extensao_permitida(arquivo.filename):
        return jsonify({"erro": "Tipo de arquivo não permitido"}), 400
    
    nome_seguro = secure_filename(arquivo.filename)
    caminho_arquivo = os.path.join(app.config["UPLOAD_FOLDER"], nome_seguro)
    arquivo.save(caminho_arquivo)
    caminho_imagem = f"/static/images/{nome_seguro}"

    # Busca o card pai no banco
    card = Exposed.query.get(int(id_card))
    
    if not card:
        return jsonify({"erro": "Card não encontrado"}), 404
    
    # Cria nova arte interna ligada ao card
    nova_arte = ArteInterna(imagem=caminho_imagem, exposed_id=card.id)
    db.session.add(nova_arte)
    db.session.commit()

    return jsonify({"imagem": caminho_imagem}), 201


@app.route("/exposed/apagar-arte", methods=["POST"])
def apagar_arte_interna():

    dados = request.get_json()

    if not dados or "id_card" not in dados or "caminho" not in dados:
        return jsonify({"erro": "id_card e caminho são obrigatórios"}), 400
    
    # Busca arte interna pelo caminho e id do card
    arte = ArteInterna.query.filter_by(
        exposed_id=dados["id_card"],
        imagem=dados["caminho"]
    ).first()

    if not arte:
        return jsonify({"erro": "Arte não encontrada"}), 404
    
    db.session.delete(arte)
    db.session.commit()
    
    return jsonify({"sucesso": True}), 200


@app.route("/inspiracoes")
def inspiracoes():
    # Busca todas as informações no banco de dados de uma vez
    inspiracoes = Inspiracao.query.all()

    # ORM retorna objetos → convertendo para dicionários para o Jinja usar
    lista = [{"id": i.id, "imagem": i.imagem} for i in inspiracoes]

    # Envia a lista para template inspiracoes.html
    return render_template("inspiracoes.html", inspiracoes=lista)


@app.route("/inspiracoes/adicionar", methods=["POST"])
def adicionar_inspiracao():

    # Verifica se o arquivo foi enviado na requisição
    if "imagem" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    arquivo = request.files["imagem"]

    if arquivo.filename == "":
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400
    
    if not extensao_permitida(arquivo.filename):
        return jsonify({"erro": "Tipo de arquivo não permitido"}), 400
    
    nome_seguro = secure_filename(arquivo.filename)

    caminho_arquivo = os.path.join(app.config["UPLOAD_FOLDER"], nome_seguro)
    arquivo.save(caminho_arquivo)

    # Monta o caminho que será salvo no banco
    caminho_imagem = f"/static/images/{nome_seguro}"

    # Cria um novo objeto Inspiracao com o caminho salvo
    nova = Inspiracao(imagem=caminho_imagem)

    db.session.add(nova)  # Adiciona o objeto na sessão para salvar
    db.session.commit()   # salva no banco de verdade

    return jsonify({"mensagem": "Inspiração adicionada!", "imagem": caminho_imagem}), 201


@app.route("/inspiracoes/apagar", methods=["POST"])
def apagar_inspiracao():
    
    # Recebe os dados enviados pelo JS em formato JSON
    dados = request.get_json()

    if not dados or "id" not in dados:
        return jsonify({"erro": "Campo 'id' é obrigatório."}), 400
    
    # Busca inspiração no banco pelo id
    inspiracao = Inspiracao.query.get(dados["id"])

    if not inspiracao:
        return jsonify({"erro": "Inspiração não encontrada."}), 404

    db.session.delete(inspiracao)
    db.session.commit()
    
    
    return jsonify({"mensagem": "Inspiração apagada com sucesso!"}), 200

#Execução do App
if __name__ == "__main__":
    app.run(debug=True)
    