document.addEventListener('DOMContentLoaded', function () {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const languageSelect = document.getElementById('language-select');
    const loadingMessage = document.getElementById('loading-message');

    // Função para exibir mensagem de boas-vindas
    function showWelcomeMessage() {
        const welcomeMessage = "Bem vindo ao ChatBot - Guide, seu guia para estudos em programação! Lembre-se de relacionar os temas do seu estudo com a linguagem específica! Bons estudos!";
        addMessageToChat('Guide', welcomeMessage, 'bot-message');
    }

    async function sendMessage() {
        const userMessage = userInput.value.trim();
        const selectedLanguage = languageSelect.value.trim();
        if (!userMessage || !selectedLanguage) return;

        addMessageToChat('Você', userMessage, 'user-message');
        userInput.value = ''; // Limpa o campo de input

        showLoading(true);

        try {
            const response = await fetch('https://<seu-app>.up.railway.app/chatbot', {  // Atualize esta URL
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage, language: selectedLanguage })
            });
            const data = await response.json();
            const botResponse = escapeHtml(data.response);
            addMessageToChat('Guide', botResponse, 'bot-message');
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

    function updateSelectIcon() {
        const selectedOption = languageSelect.options[languageSelect.selectedIndex];
        const iconUrl = selectedOption.getAttribute('data-icon');
        languageSelect.style.backgroundImage = `url(${iconUrl})`;
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    languageSelect.addEventListener('change', updateSelectIcon);

    // Inicializa o ícone com a opção selecionada por padrão
    updateSelectIcon();

    // Exibir a mensagem de boas-vindas ao carregar a página
    showWelcomeMessage();
});
