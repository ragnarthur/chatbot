document.addEventListener('DOMContentLoaded', function () {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const languageSelect = document.getElementById('language-select');

    async function sendMessage() {
        const userMessage = userInput.value.trim();
        const selectedLanguage = languageSelect.value.trim();
        if (!userMessage || !selectedLanguage) return;

        // Adiciona a mensagem do usuário ao chat
        addMessageToChat('user', userMessage);
        userInput.value = ''; // Limpa o campo de input

        // Mostra a mensagem de carregamento e esconde após resposta
        showLoadingMessage(true);

        try {
            // Envia a mensagem ao backend para obter a resposta
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage, language: selectedLanguage })
            });
            const data = await response.json();
            const botResponse = escapeHtml(data.response);

            // Adiciona a resposta do bot ao chat
            addMessageToChat('bot', botResponse);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            // Sempre esconde a mensagem de carregamento
            showLoadingMessage(false);
        }
    }

    function addMessageToChat(role, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add(`${role}-message`);
        messageElement.innerHTML = `<strong>${role === 'user' ? 'Você' : 'Bot'}:</strong> ${message}`;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function showLoadingMessage(show) {
        const loadingMessage = document.getElementById('loading-message') || createLoadingMessage();
        loadingMessage.style.display = show ? 'block' : 'none';
    }

    function createLoadingMessage() {
        const loadingMessage = document.createElement('div');
        loadingMessage.id = 'loading-message';
        loadingMessage.textContent = 'Pesquisando...';
        loadingMessage.style.display = 'none';
        chatWindow.appendChild(loadingMessage);
        return loadingMessage;
    }

    function escapeHtml(text) {
        return text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});
