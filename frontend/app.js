document.addEventListener('DOMContentLoaded', function () {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const customSelectButton = document.getElementById('custom-select-button');
    const customSelectList = document.getElementById('custom-select-list');
    const customSelectContainer = document.getElementById('custom-select-container');
    const loadingMessage = document.getElementById('loading-message');

    let selectedLanguage = '';

    async function sendMessage() {
        const userMessage = userInput.value.trim();
        if (!userMessage || !selectedLanguage) return;

        addMessageToChat('Você', userMessage, 'user-message');
        userInput.value = ''; // Limpa o campo de input

        showLoading(true);

        try {
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage, language: selectedLanguage })
            });
            const data = await response.json();
            const botResponse = escapeHtml(data.response);
            addMessageToChat('Bot', botResponse, 'bot-message');
        } catch (error) {
            console.error('Error:', error);
        } finally {
            showLoading(false);
        }
    }

    function addMessageToChat(sender, message, messageType) {
        const messageElement = document.createElement('div');
        messageElement.classList.add(messageType);
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function showLoading(isLoading) {
        loadingMessage.style.display = isLoading ? 'block' : 'none';
    }

    function escapeHtml(text) {
        return text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    customSelectButton.addEventListener('click', function () {
        customSelectList.classList.toggle('show');
    });

    customSelectList.addEventListener('click', function (e) {
        if (e.target.tagName === 'LI') {
            selectedLanguage = e.target.getAttribute('data-value');
            customSelectButton.innerHTML = e.target.innerHTML;
            customSelectList.classList.remove('show');
        }
    });

    document.addEventListener('click', function (e) {
        if (!customSelectContainer.contains(e.target) && e.target !== customSelectButton) {
            customSelectList.classList.remove('show');
        }
    });

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});
