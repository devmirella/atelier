from flask import Flask, render_template, jsonify, request
import json
import os
from pathlib import Path
from werkzeug.utils import secure_filename # secure_filename → função do Flask que limpa o nome do arquivo

app = Flask(__name__)

# Configuração de UPLOAD
UPLOAD_FOLDER = os.path.join("static", "images")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER 

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
    caminho = Path("data/arte.json")

    if caminho.exists():
        with open(caminho, encoding="utf-8") as f:
            artes = json.load(f)
    else: 
        artes = []
    return render_template("arte.html", artes=artes)

@app.route("/arte/adicionar", methods=["POST"])
def adicionar_arte():
    caminho_json = Path("data/arte.json") # Caminho relativo para o arquivo arte.json

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

    if caminho_json.exists():
        with open(caminho_json, encoding="utf-8") as f:
            artes = json.load(f)

    else: # Se o arquivo JSON não existir crie um lista vazia
        artes = []
    
    novo_id = 1 # Gerar um novo ID
    if artes: 
        novo_id = max(item["id"] for item in artes) + 1
    
    nova_arte = {
        "id": novo_id,
        "imagem": caminho_imagem # Agora salva o caminho local, não mais a URL externa 
    }
    artes.append(nova_arte)

    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(artes, f, ensure_ascii=False, indent=2)

    return jsonify(nova_arte), 201


@app.route("/arte/apagar", methods=["POST"])
def apagar_arte():
    caminho = Path("data/arte.json")

    dados = request.get_json()

    # Validação básica 
    if not dados or "id" not in dados:
        return jsonify({"erro": "ID é obrigatório"}), 400
    
    id_para_apagar = dados["id"]

    # Se o arquivo não existir, não há o que apagar
    if not caminho.exists():
        return jsonify({"erro": "Arquivo de arte não encontrado"}), 404
    
    # Lê o JSON 
    with open(caminho, encoding="utf-8") as f:
        artes = json.load(f)

    # Filtra removendo apenas o ID informado
    artes_filtradas = [arte for arte in artes if arte["id"] != id_para_apagar]

    # Se nada mudou, o ID não existia
    if len(artes) == len(artes_filtradas):
        return jsonify({"erro": "Arte não encontrada"}), 404
    
    # Salva o JSON atualizado
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(artes_filtradas, f, ensure_ascii=False, indent=2)

    return jsonify({"sucesso": True}), 200

@app.route("/exposed")
def exposed():
    caminho = Path("data/exposed.json")

    if caminho.exists():
        with open(caminho, encoding="utf-8") as f:
            exposed = json.load(f)
    else:
        exposed = []

    return render_template("exposed.html", exposed=exposed)

@app.route("/exposed/adicionar", methods=["POST"])
def adicionar_exposed():
    # Define o caminho do arquivo JSON onde as artes do exposed são salvas
    caminho = Path("data/exposed.json")

    dados = request.get_json()
    if not dados or "imagem" not in dados or dados["imagem"].strip() == "":
        return jsonify({"erro": "URL da imagem é obrigatoria"}), 400
    
    # Verifica se o arquivo exposed.json já existe
    if caminho.exists():
        with open(caminho, encoding="utf-8") as f:
            exposed = json.load(f)
    else:
        # Se não existir, inicia uma lista vazia
        exposed = []
    novo_id = 1
    if exposed:
        novo_id = max(item["id"] for item in exposed) + 1
    # Cria um novo item que será salvo no JSON
    novo_item = {
        "id": novo_id,
        "imagem": dados["imagem"],
        "titulo": dados.get("titulo", ""),
        "tag": dados.get("tag", "")
    }
    # Adicionar o novo item á lista existente
    exposed.append(novo_item)
    # Abre o arquivo JSON em modo escrita
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(exposed, f, ensure_ascii=False, indent=2) #  # indent=2 deixa o JSON legível
    # Retorna o item criado como resposta JSON
    return jsonify(novo_item), 201

@app.route("/exposed/apagar", methods=["POST"])
def apagar_exposed(): # Define a função Python que será chamada quando a rota for acessada.

    caminho = Path("data/exposed.json") 
    dados = request.get_json()

    # Validação básica
    if not dados or "id" not in dados:
        return jsonify({"erro": "ID é obrigatório"}), 400
    id_para_apagar = dados["id"]

    # Se o arquivo não existir
    if not caminho.exists():
        return jsonify({"erro": "Arquivo não encontrado"}), 404
    
    # Lê o JSON
    with open(caminho, encoding="utf-8") as f:
        exposed = json.load(f)

    # Remove item com o id informado
    novos_items = [item for item in exposed if item["id"] != id_para_apagar]

    # Se nada foi removido 
    if len(novos_items) == len(exposed):
        return jsonify({"erro": "Item não encontrado"}), 404
    
    # Salva o JSON atualizado
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(novos_items, f, ensure_ascii=False, indent=2)

    return jsonify({"sucesso": True}), 200

@app.route("/inspiracoes")
def inspiracoes():
    caminho_json = Path("data/inspiracoes.json")

    if caminho_json.exists():
        with open(caminho_json, encoding="utf-8") as f:
            inspiracoes = json.load(f)
    else:
        inspiracoes = []

    return render_template("inspiracoes.html", inspiracoes=inspiracoes)


@app.route("/inspiracoes/adicionar", methods=["POST"])
def adicionar_inspiracao():

    caminho_json = Path("data/inspiracoes.json") 
    if "imagem" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    arquivo = request.files["imagem"]

    if arquivo.filename == "": 
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400
    
    if not extensao_permitida(arquivo.filename): # Verifica se a extensão do arquivo é permitida (jpg, png, gif, webp...)
        return jsonify({"erro": "Tipo de arquivo não permitido"}), 400 
    
    nome_seguro = secure_filename(arquivo.filename)

    caminho_arquivo = os.path.join(app.config["UPLOAD_FOLDER"], nome_seguro)
    arquivo.save(caminho_arquivo)
    caminho_imagem = f"/static/images/{nome_seguro}" # Monta o caminho que será salvo no JSON e usado pelo HTML para exibir a imagem

    if caminho_json.exists():
        with open(caminho_json, encoding="utf-8") as f:
            inspiracoes = json.load(f)
    else:
        inspiracoes = [] 

    novo_id = 1 
    if inspiracoes:
        novo_id = max(item["id"] for item in inspiracoes) + 1

    nova_inspiracao = {"id": novo_id, "imagem": caminho_imagem}
    inspiracoes.append(nova_inspiracao)

    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(inspiracoes, f, ensure_ascii=False)

    return jsonify({"mensagem": "Inspiração adicionada!", "imagem": caminho_imagem}), 201

@app.route("/inspiracoes/apagar", methods=["POST"])
def apagar_inspiracao():
    caminho_json = Path("data/inspiracoes.json")
    dados = request.get_json()

    if not dados or "id" not in dados:
        return jsonify({"erro": "Campo 'id' é obrigatório."}), 400
    
    id_para_apagar = dados["id"]

    if not caminho_json.exists():
        return jsonify({"erro": "Arquivo não encontrado"}), 404
    
    with open(caminho_json, encoding="utf-8") as f:
        inspiracoes = json.load(f)

    novas_inspiracoes = [item for item in inspiracoes if item["id"] != id_para_apagar]

    if len(novas_inspiracoes) == len(inspiracoes):
        return jsonify({"erro": "Inspiração não encontrada."}), 404
    
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(novas_inspiracoes, f, ensure_ascii=False, indent=2)

    return jsonify({"mensagem": "Inspiração apagada com sucesso!"}), 200

#Execução do App
if __name__ == "__main__":
    app.run(debug=True)
    