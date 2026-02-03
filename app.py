from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/arte")
def arte():
    return render_template("arte.html")

@app.route("/exposed")
def exposed():
    return render_template("exposed.html")

@app.route("/inspiracoes")
def inspiracoes():
    return render_template("inspiracoes.html")

if __name__ == "__main__":
    app.run(debug=True)
