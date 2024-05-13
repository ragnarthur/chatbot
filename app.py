from flask import Flask, request, jsonify, send_from_directory
import requests
import json
from backend.senha import API_KEY

app = Flask(__name__, static_folder='frontend')

# Configuração da API OpenAI
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
link = "https://api.openai.com/v1/chat/completions"
id_modelo = "gpt-3.5-turbo"

@app.route("/")  # Rota para servir a página HTML principal
def index():
    return send_from_directory('frontend', 'index.html')

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    user_message = data.get("message", "")

    body_mensagem = {
        "model": id_modelo,
        "messages": [{"role": "user", "content": user_message}]
    }
    body_mensagem = json.dumps(body_mensagem)

    requisicao = requests.post(link, headers=headers, data=body_mensagem)
    response = requisicao.json()

    # Extraindo a mensagem da resposta
    resposta_content = response.get("choices", [{}])[0].get("message", {}).get("content", "")

    return jsonify({"response": resposta_content})

@app.route('/<path:path>')  # Rota para servir arquivos estáticos
def static_file(path):
    return send_from_directory('frontend', path)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
