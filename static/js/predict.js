document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.querySelector('.chat-container');
    // If the chat interface isn't on the page, don't run the script
    if (!chatContainer) return;

    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const cropName = chatContainer.dataset.cropName;

    // --- NEW: Load chat history from the browser's localStorage ---
    const loadChatHistory = () => {
        const history = JSON.parse(localStorage.getItem(`chatHistory_${cropName}`));
        // Only load if there's more than the default welcome message
        if (history && history.length > 1) { 
            chatBox.innerHTML = ''; // Clear the default welcome message
            history.forEach(msg => appendMessage(msg.message, msg.sender, false)); // Don't save while loading
        }
    };

    // --- NEW: Save chat history to localStorage ---
    const saveChatHistory = () => {
        const messages = [];
        chatBox.querySelectorAll('.chat-message').forEach(div => {
            // Exclude any temporary loading indicators from being saved
            if (!div.classList.contains('chat-loader')) {
                messages.push({
                    sender: div.classList.contains('user') ? 'user' : 'bot',
                    message: div.innerHTML
                });
            }
        });
        localStorage.setItem(`chatHistory_${cropName}`, JSON.stringify(messages));
    };

    // --- NEW: Clear chat history for the current crop ---
    const clearChatHistory = () => {
        localStorage.removeItem(`chatHistory_${cropName}`);
        chatBox.innerHTML = '<div class="chat-message bot">Welcome! Ask me anything about this crop.</div>';
        saveChatHistory(); // Save the welcome message as the initial state
    };

    // Check if the current cropName is different from the last one saved in session/local storage
    // If it's different, clear the history. This ensures a fresh start for each new prediction.
    const lastCropName = localStorage.getItem('lastPredictedCrop');
    if (lastCropName !== cropName) {
        clearChatHistory();
        localStorage.setItem('lastPredictedCrop', cropName);
    } else {
        loadChatHistory(); // Load history only if it's the same crop as before
    }

    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (message === "") return;

        appendMessage(message, 'user');
        userInput.value = '';
        
        appendTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ crop: cropName, question: message })
            });

            removeTypingIndicator();
            
            const botMessageDiv = document.createElement('div');
            botMessageDiv.className = 'chat-message bot';
            
            const textSpan = document.createElement('span');
            const cursorSpan = document.createElement('span');
            cursorSpan.className = 'typing-cursor';
            
            botMessageDiv.appendChild(textSpan);
            botMessageDiv.appendChild(cursorSpan);
            chatBox.appendChild(botMessageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            while (true) {
                const { value, done } = await reader.read();
                if (done) {
                    botMessageDiv.removeChild(cursorSpan);
                    saveChatHistory(); // Save history after bot finishes responding
                    break;
                }
                
                const chunk = decoder.decode(value);
                textSpan.innerHTML += chunk;
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        } catch (error) {
            console.error('Streaming Error:', error);
            removeTypingIndicator();
            appendMessage('Sorry, an error occurred. Please try again.', 'bot');
        }
    };

    const appendMessage = (message, sender, shouldSave = true) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}`;
        messageDiv.innerHTML = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        if (shouldSave) {
            saveChatHistory();
        }
    };
    
    // --- Helper functions for loading indicator ---
    const appendTypingIndicator = () => {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message bot chat-loader';
        typingDiv.innerHTML = `
            <div class="spinner"></div>
            <span>Please wait, the chat is loading...</span>
        `;
        chatBox.appendChild(typingDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    const removeTypingIndicator = () => {
        const indicator = chatBox.querySelector('.chat-loader');
        if (indicator) {
            chatBox.removeChild(indicator);
        }
    };

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Load history as soon as the page is ready
    // loadChatHistory(); // This line is now handled by the new_code
});