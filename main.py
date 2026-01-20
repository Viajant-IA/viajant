from flask import Flask, request, jsonify, render_template
import requests
import json
import os
from dotenv import load_dotenv
from datetime import timedelta, datetime
import jwt
import hashlib

# Config. API
load_dotenv()
api_key = os.getenv("API_KEY")
resp = requests.post(
    "https://api.openai.com/v2/chat/completions",
    headers={
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json"
    },
    json={
      "model": "gpt-5-nano",
      "messages": [{"role":"user","content":"Olá!"}],
    }
)

SECRET_KEY = os.environ.get('SECRET_KEY')
TOKEN_EXPIRATION_DAYS = 1

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Rotas
@app.route("/")
def home():
    return render_template ("index.html")

# Configuração do users.json para fazer com que escreva os usuários
# Em Breve...

# Configuração de API
@app.route("/api", methods=["POST"])
def api():
    dados = request.get_json()
    print(dados)
    return "{ok: True}"

# Rotas de API
@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    user_msg = data.get("message", "")

    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-5-nano",
            "messages": [{"role": "user", "content": user_msg}]
        }
    )

    return jsonify(resp.json())

# Rotas
@app.route("/chat")
def chat():
    user = request.args.get("user")
    return render_template ("chat.html", user=user)

@app.route("/docs")
def docs():
    return render_template ("docs.html")

@app.route("/about-us")
def about_us():
    return render_template ("about-us.html")

@app.route("/download/android")
def android():
    return render_template("android.html")

@app.route("/download/ios")
def iphone():
    return render_template ("ios.html")



def hash_password(password):
    return hashlib.(password.encode()).hexdigest()

def generate_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=TOKEN_EXPIRATION_DAYS),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='')
    except Exception as e:
        return str(e)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "JSON inválido"}), 400

    username = data.get('username')
    password = data.get('password')

    ... # O Resto aqui é totalmente confidencial para deixar Open Source.


if __name__ == '__main__':
    app.run(debug=True, port=5000)
