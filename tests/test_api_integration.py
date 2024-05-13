import pytest
from unittest.mock import patch
from flask import json
import sys

# Certifique-se de que o caminho para o seu app está correto
sys.path.append(r'C:\Users\arthu\OneDrive\Desktop\ChatBot_v1')
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('requests.post')
def test_integration_with_openai(mock_post, client):
    # Configura a simulação da resposta da API
    mock_response = {
        "choices": [
            {"message": {"content": "Python é uma linguagem de programação poderosa."}}
        ]
    }
    mock_post.return_value.json.return_value = mock_response
    mock_post.return_value.status_code = 200

    # Dados para enviar para o endpoint
    data = {
        'message': 'O que é Python?',
        'language': 'python'
    }
    
    # Enviar a requisição simulada
    response = client.post('/chatbot', data=json.dumps(data), content_type='application/json')

    # Verificar se a resposta é a esperada
    assert response.status_code == 200
    data = json.loads(response.data)
    expected_response = "Python é uma linguagem de programação poderosa."
    assert data['response'] == expected_response
    mock_post.assert_called_once()  # Verifica se a API foi chamada uma vez

# Execute o teste se este arquivo for executado diretamente
if __name__ == '__main__':
    pytest.main()
