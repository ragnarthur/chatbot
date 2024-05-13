import pytest
from flask import json, Flask
from flask_testing import TestCase

# Adicione o caminho ao seu diretório de aplicativos para importação
# Use raw strings para evitar problemas de escape com caminhos no Windows
import sys
sys.path.append(r'C:\Users\arthu\OneDrive\Desktop\ChatBot_v1')

from app import app  # Importa o app Flask configurado

class TestChatBot(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_successful_response(self):
        # Um exemplo de entrada válida para Python
        response = self.client.post('/chatbot', data=json.dumps({
            'message': 'hello world',
            'language': 'python'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('response' in data)  # Verifica se a chave 'response' existe na resposta

    def test_failure_response(self):
        # Uma entrada que não contém termos relacionados
        response = self.client.post('/chatbot', data=json.dumps({
            'message': 'how is the weather today?',
            'language': 'python'
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Desculpe, atualmente eu só posso responder perguntas diretamente relacionadas", data['response'])

# Executa o teste se este arquivo for executado diretamente
if __name__ == '__main__':
    pytest.main()
