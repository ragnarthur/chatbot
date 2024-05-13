document.addEventListener('DOMContentLoaded', function () {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    async function sendMessage() {
        const userMessage = userInput.value.trim();
        if (!userMessage) return;

        // Adiciona a mensagem do usuário ao chat
        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('user-message');
        userMessageElement.innerHTML = `<strong>Você:</strong> ${userMessage}`;
        chatWindow.appendChild(userMessageElement);
        userInput.value = ''; // Limpa o campo de input

        try {
            // Envia a mensagem ao backend para obter a resposta
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage })
            });
            const data = await response.json();
            const botResponse = data.response;

            // Adiciona a resposta do bot ao chat
            const botMessageElement = document.createElement('div');
            botMessageElement.classList.add('bot-message');
            botMessageElement.innerHTML = `<strong>Bot:</strong> ${botResponse}`;
            chatWindow.appendChild(botMessageElement);

            // Rola para a última mensagem
            chatWindow.scrollTop = chatWindow.scrollHeight;

        } catch (error) {
            console.error('Error:', error);
        }
    }

    sendButton.addEventListener('click', sendMessage);

    // Envia a mensagem quando pressionar Enter
    userInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});
