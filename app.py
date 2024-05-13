from flask import Flask, request, jsonify, send_from_directory
import requests
import json
from backend.senha import API_KEY

app = Flask(__name__, static_folder='frontend')

# Dicionário de linguagens de programação permitidas e termos relacionados
allowed_languages = {
    'python': ['python', 'py', 'pandas', 'flask', 'django', 'numpy', 'scipy', 'pip', 'matplotlib',
               'tkinter',"seaborn",'pytest', 'pycharm', 'jupyter','anacondax', 'virtualenv',
               'dataframe', 'sklearn', 'tensorflow','keras'],
    'javascript': ['javascript', 'js', 'node.js', 'node', 'react', 'react.js', 'vue', 'vue.js', 
                   'angular', 'angular.js', 'express', 'npm', 'yarn', 'webpack', 'babel',
                   'typescript', 'ts', 'jest'],
    'css': ['css', 'css3', 'flexbox', 'grid'],
    'html': ['html', 'html5'],
    'langchain': ['langchain', 'lcc'],
    'react': ['react', 'react.js', 'jsx', 'react native'],
    'java': ['java', 'javafx', 'spring', 'jvm', 'jdk']
}

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
link = "https://api.openai.com/v1/chat/completions"
id_modelo = "gpt-3.5-turbo"

@app.route("/")
def index():
    return send_from_directory('frontend', 'index.html')

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    user_message = data.get("message", "").lower()
    selected_language = data.get("language", "").lower()

    # Verifica se a linguagem selecionada é permitida e a mensagem contém termos relacionados
    if selected_language in allowed_languages and any(term in user_message for term in allowed_languages[selected_language]):
        body_mensagem = {
            "model": id_modelo,
            "messages": [{"role": "user", "content": user_message}]
        }
        body_mensagem = json.dumps(body_mensagem)
        requisicao = requests.post(link, headers=headers, data=body_mensagem)
        response = requisicao.json()
        resposta_content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    else:
        resposta_content = "Desculpe, atualmente eu só posso responder perguntas diretamente relacionadas a Python, JavaScript, CSS, HTML, LangChain, React, e Java. Por favor, verifique se sua pergunta está relacionada a esses tópicos."

    return jsonify({"response": resposta_content})

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('frontend', path)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
