from flask import Flask, request, jsonify, send_from_directory
import requests
import json
from backend.senha import API_KEY

app = Flask(__name__, static_folder='.')

session = requests.Session()  # Cria uma sessão para reutilizar conexões TCP

# Dicionário de linguagens de programação permitidas e termos relacionados
allowed_languages = {
    'python': ['python', 'py', 'pandas', 'flask', 'django', 'numpy', 'scipy', 'tkinter', 'matplotlib', 
               'seaborn', 'pytest', 'pycharm', 'jupyter', 'anaconda', 'pip', 'virtualenv', 'dataframe', 'sklearn', 
               'tensorflow', 'keras', 'framework', 'ruby'],
    'javascript': ['javascript', 'js', 'node.js', 'node', 'react', 'react.js', 'vue', 'vue.js', 'angular',
                    'angular.js', 'express', 'npm', 'yarn', 'webpack', 'babel', 'typescript', 'ts', 'jest', 'mocha', 
                    'chai', 'electron', 'd3.js', 'three.js', 'framework'],
    'css': ['css', 'css3', 'flexbox', 'grid', 'media queries', 'sass', 'scss', 'less', 'bootstrap', 'tailwind', 
            'responsive design', 'animations', 'transitions', 'selectors', 'variables', 'borders', 'margins', 'padding'],
    'html': ['html', 'html5', 'semantic html', 'forms', 'input types', 'canvas', 'svg', 'tables', 'head', 'meta', 'links',
              'doctype', 'elements', 'tags', 'attributes', 'inline', 'block', 'iframes', 'media', 'accessibility', 
              'web components'],
    'langchain': ['langchain', 'lcc', 'language chain', 'nlp', 'text processing', 'tokenization', 'lemmatization', 
                  'stemming', 'ner', 'named entity recognition', 'sentiment analysis', 'language models', 'text generation', 
                  'language modeling'],
    'react': ['react', 'react.js', 'jsx', 'react native', 'redux', 'react hooks', 'context api', 'next.js', 'gatsby', 
              'create-react-app', 'component', 'props', 'state', 'lifecycle', 'effect', 'memo', 'ref', 'router', 'flux',
                'server-side rendering', 'ssr', 'hydration', 'virtual dom'],
    'java': ['java', 'javafx', 'spring', 'jvm', 'jdk', 'jre', 'maven', 'gradle', 'intellij', 'eclipse', 'netbeans', 
             'servlet', 'jsp', 'jdbc', 'hibernate', 'junit', 'lambda', 'streams', 'multithreading', 'concurrency', 
             'collections', 'garbage collection', 'jpa', 'swing', 'applet']
}

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
link = "https://api.openai.com/v1/chat/completions"
id_modelo = "gpt-3.5-turbo"

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    user_message = data.get("message", "").lower()
    selected_language = data.get("language", "").lower()

    # Verifica se a linguagem selecionada é permitida e a mensagem contém termos relacionados
    if selected_language in allowed_languages and any(term in user_message for term in allowed_languages[selected_language]):
        body_mensagem = {
            "model": id_modelo,
            "messages": [{"role": "user", "content": user_message}],
            "temperature": 0.2,
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
    return send_from_directory('.', path)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
