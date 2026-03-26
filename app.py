from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
from werkzeug.utils import secure_filename # secure_filename → função do Flask que limpa o nome do arquivo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from extensoes import db, login_manager
from models import Inspiracao, Arte, Exposed, ArteInterna, Usuario


app = Flask(__name__)

# Configuração de UPLOAD
UPLOAD_FOLDER = os.path.join("static", "images")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER 


# Configuração do banco de dados 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///atelier.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "atelier_secret_key"

# Inicializa o banco de dados com o app
db.init_app(app) # Conecta o banco de dados ao app Flask
login_manager.init_app(app) # Conecta o gerenciador de login ao app Flask
login_manager.login_view = "index" # define a rota de redirecionamento caso o usuário não esteja logado ("index" é o nome da função da rota)


# Carregador de usuário 
@login_manager.user_loader # Ensina o Flask-Login a reconhecer o usuário pelo id
def carregar_usuario(usuario_id):
    return Usuario.query.get(int(usuario_id)) # Busca o usuário no banco pelo id

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
@login_required
def home():
    return render_template("home.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":

        # Pega os dados do formulário
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        # verifica se o email já existe no banco e, se existir, impede o cadastro e redireciona para a tela de cadastro
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return render_template("cadastro.html", erro="Email já cadastrado." )
        
        # Cria o hash da senha - nunca salva a senha pura no banco 
        senha_hash = generate_password_hash(senha)

        # Cria o novo usuário
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()

        # Redireciona para login após cadastro
        return redirect(url_for("index"))
    
    return render_template("cadastro.html")

@app.route("/login", methods=["POST"])
def login():

    # Pega os dados enviados pelo formulário
    email = request.form.get("email")
    senha = request.form.get("senha")

    # Busca o usuário no banco pelo email
    usuario = Usuario.query.filter_by(email=email).first()

    # Verifica se o usuário não existe ou se a senha está incorreta
    if not usuario or not check_password_hash(usuario.senha, senha):
        return render_template("index.html", erro="Email ou senha incorretos.")
    
    # Verifica se o usuário esta ativo
    if not usuario.ativo:
        return render_template("index.html", erro="Conta desativada")
    
    login_user(usuario)

    return redirect(url_for("home"))

@app.route("/logout")
@login_required # Só pode fazer logout quem está logado
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/recuperar-senha", methods=["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":

        email = request.form.get("email")
        nova_senha = request.form.get("nova_senha")

        # Busca o usuário no banco pelo email digitado
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            return render_template("recuperar.html", erro="Email não encontrado")
        
        usuario.senha = generate_password_hash(nova_senha)
        db.session.commit()

        return render_template("recuperar.html", sucesso="Senha atualizada! faça login com a nova senha. ")

    return render_template("recuperar.html")

@app.route("/admin")
@login_required
def admin():
    
    if not current_user.is_admin:
        return redirect(url_for("home"))
    
    usuarios = Usuario.query.all()

    return render_template("admin.html", usuarios=usuarios)

@app.route("/admin/toggleativar/<int:id>", methods=["POST"])
@login_required
def toggle_ativar(id):

    # Só admin pode acessar
    if not current_user.is_admin:
        return redirect(url_for("home"))

    # Busca o usuário no banco pelo id que veio na URL  
    usuario = Usuario.query.get(id)

    if not usuario:
        return redirect(url_for("admin"))
    
    # Inverte o status 
    usuario.ativo = not usuario.ativo
    db.session.commit()

    return redirect(url_for("admin"))

@app.route("/admin/apagar/<int:id>", methods=["POST"])
@login_required
def apagar_usuario(id):

    if not current_user.is_admin:
        return redirect(url_for("home"))
    
    # Busca o usuário no banco pelo id que veio na URL
    usuario = Usuario.query.get(id)

    if not usuario:
        return redirect(url_for("admin"))
    
    db.session.delete(usuario)
    db.session.commit()

    return redirect(url_for("admin"))


@app.route("/arte")
@login_required
def arte():
    
    # Busca todas as artes no banco de dados
    artes = Arte.query.filter_by(usuario_id=current_user.id).all()
    lista = [{"id": a.id, "imagem": a.imagem} for a in artes]

    return render_template("arte.html", artes=lista)


@app.route("/arte/adicionar", methods=["POST"])
@login_required
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
    nova = Arte(imagem=caminho_imagem, usuario_id=current_user.id)
    db.session.add(nova)
    db.session.commit()

    return jsonify({"id": nova.id, "imagem": nova.imagem}), 201

@app.route("/arte/apagar", methods=["POST"])
@login_required
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
@login_required
def exposed():

    itens = Exposed.query.filter_by(usuario_id=current_user.id).all()

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
@login_required
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
    novo = Exposed(imagem=caminho_imagem, titulo=titulo, tag=tag, usuario_id=current_user.id)
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
@login_required
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
@login_required
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
@login_required
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
@login_required
def inspiracoes():
    # Busca todas as informações no banco de dados de uma vez
    inspiracoes = Inspiracao.query.filter_by(usuario_id=current_user.id).all()

    # ORM retorna objetos → convertendo para dicionários para o Jinja usar
    lista = [{"id": i.id, "imagem": i.imagem} for i in inspiracoes]

    # Envia a lista para template inspiracoes.html
    return render_template("inspiracoes.html", inspiracoes=lista)


@app.route("/inspiracoes/adicionar", methods=["POST"])
@login_required
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
    nova = Inspiracao(imagem=caminho_imagem, usuario_id=current_user.id)

    db.session.add(nova)  # Adiciona o objeto na sessão para salvar
    db.session.commit()   # salva no banco de verdade

    return jsonify({"mensagem": "Inspiração adicionada!", "imagem": caminho_imagem}), 201


@app.route("/inspiracoes/apagar", methods=["POST"])
@login_required
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
    