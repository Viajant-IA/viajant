from flask import Flask, request, jsonify, render_template
import requests
import json
import os
from dotenv import load_dotenv

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
