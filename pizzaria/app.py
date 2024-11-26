#python -m venv venv
#.\venv\Scripts\activate
#pip install flask
# pip install python-dotenv
#pip freeze > requirements.txt
#pip install -r requirements.txt
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"  # Necessária para sessões e mensagens flash

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/cardapio')
def cardapio():
    pizzas = [
        {
            "nome": "Calabresa",
            "ingredientes": "Molho de tomate, mussarela, calabresa, cebola e orégano",
            "preco": 30.00
        },
        {
            "nome": "Mussarela",
            "ingredientes": "Molho de tomate, mussarela e orégano",
            "preco": 25.00
        },
        {
            "nome": "Portuguesa",
            "ingredientes": "Molho de tomate, mussarela, presunto, ovos, cebola, azeitona e orégano",
            "preco": 35.00
        }
    ]
    return render_template("cardapio.html", pizzas=pizzas)

@app.route('/avaliacoes', methods=["GET", "POST"])
def avaliacoes():
    avaliacoes = session.get('avaliacoes', [])
    if request.method == "POST":
        cliente = request.form.get("cliente")
        comentario = request.form.get("comentario")
        estrelas = request.form.get("estrelas")
        if cliente and estrelas:
            nova_avaliacao = {
                "cliente": cliente,
                "comentario": comentario,
                "estrelas": int(estrelas)
            }
            avaliacoes.append(nova_avaliacao)
            session['avaliacoes'] = avaliacoes
            flash("Avaliação enviada com sucesso!", "success")
        else:
            flash("Preencha os campos obrigatórios.", "danger")
    return render_template("avaliacoes.html", avaliacoes=avaliacoes)

@app.route('/fale_conosco', methods=["GET", "POST"])
def fale_conosco():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        mensagem = request.form.get("mensagem")
        if nome and email and mensagem:
            flash("Mensagem enviada com sucesso! Entraremos em contato em breve.", "success")
        else:
            flash("Todos os campos são obrigatórios.", "danger")
    return render_template("fale_conosco.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    usuarios = {
        "admin": "1234",
        "cliente1": "senha1",
        "cliente2": "senha2"
    }
    if request.method == "POST":
        username = request.form.get("username")
        senha = request.form.get("senha")
        if username in usuarios and usuarios[username] == senha:
            session['usuario'] = username
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("index"))
        else:
            flash("Credenciais inválidas. Tente novamente.", "danger")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
