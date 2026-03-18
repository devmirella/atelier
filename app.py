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
    caminho = Path("data/exposed.json")

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

    if caminho.exists():
        with open(caminho, encoding="utf-8") as f:
            exposed = json.load(f)
    else:
        exposed = []

    novo_id = 1
    if exposed:
        novo_id = max(item["id"] for item in exposed) + 1

    novo_item = {
        "id": novo_id,
        "imagem": caminho_imagem,
        "titulo": titulo,
        "tag": tag,
        "artes": []
    }

    exposed.append(novo_item)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(exposed, f, ensure_ascii=False, indent=2)

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

@app.route("/exposed/adicionar-arte", methods=["POST"])
def adicionar_arte_exposed():

    caminho = Path("data/exposed.json")
    id_card = request.form.get("id") # Pega o id do card pai enviado pelo JS via FormData
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
    with open(caminho, encoding="utf-8") as f:
        exposed = json.load(f)
    
    # Encontra o card pelo id e adiciona a arte na lista de artes
    for item in exposed:
        if item["id"] == int(id_card): 
            # Se o card ainda não tem lista de artes, cria uma vazia
            if "artes" not in item:
                item["artes"] = []
            # Adiciona o caminho da nova arte na lista
            item["artes"].append(caminho_imagem)
            break

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(exposed, f, ensure_ascii=False, indent=2)

    return jsonify({"imagem": caminho_imagem}), 201


@app.route("/exposed/apagar-arte", methods=["POST"])
def apagar_arte_interna():

    caminho = Path("data/exposed.json")

    dados = request.get_json()

    if not dados or "id_card" not in dados or "caminho" not in dados:
        return jsonify({"erro": "id_card e caminho são obrigatórios"}), 400
    
    # Pega o id do card e caminho da imagem a ser removida
    id_card = dados["id_card"]
    caminho_arte = dados["caminho"]

    with open(caminho, encoding="utf-8") as f:
        exposed = json.load(f)

    # Encontra o card pleo id e remove a arte da lista
    for item in exposed:
        if item["id"] == id_card:
            if "artes" in item:
                # Filtra mantendo todas as artes Exceto a que tem o caminho informado
                item["artes"] = [a for a in item["artes"] if a != caminho_arte]
                break 
    
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(exposed, f, ensure_ascii=False, indent=2)
    
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
    