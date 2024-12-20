document.addEventListener('DOMContentLoaded', () => {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWidget = document.getElementById('chat-widget');
    const chatClose = document.getElementById('chat-close');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatMessages = document.getElementById('chat-messages');

    // Function to open chat widget and hide the toggle button
    chatToggle.addEventListener('click', () => {
        chatWidget.style.display = 'block';
        chatToggle.style.display = 'none';  // Hide the "Chat with us" button when chat is open
        chatInput.focus();  // Focus on the input when chat is opened
    });

    // Close the chat widget and show the toggle button again
    chatClose.addEventListener('click', () => {
        chatWidget.style.display = 'none';
        chatToggle.style.display = 'block';  // Show the button again when chat is closed
    });

    // Handle sending messages
    chatSend.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        const userMessage = chatInput.value.trim();
        if (userMessage) {
            addMessageToChat('You', userMessage, 'user-message');
            chatInput.value = ''; // Clear input field

            // Send the message to the backend
            fetch('/helpdesk/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            })
                .then((response) => response.json())
                .then((data) => {
                    addMessageToChat('Helpdesk', data.response, 'bot-message');
                })
                .catch(() => {
                    addMessageToChat(
                        'Helpdesk',
                        'Something went wrong. Please try again later.',
                        'bot-message'
                    );
                });
        }
    }

    function addMessageToChat(sender, message, className) {
        const messageBubble = document.createElement('div');
        messageBubble.classList.add('chat-bubble', className);
        messageBubble.innerHTML = `<strong>${sender}:</strong> ${message}`;

        // Add the new message to the top of the chat
        chatMessages.insertBefore(messageBubble, chatMessages.firstChild);

        // Automatically scroll to the top of the chat container
        scrollToTop();
    }

    function scrollToTop() {
        // Scroll to the top of the chat container to show the latest message
        chatMessages.scrollTop = 0;
    }

    // Scroll to top when new messages are added (via DOMNodeInserted)
    chatMessages.addEventListener('DOMNodeInserted', () => {
        scrollToTop();
    });

    // Scroll to top when sending a message
    chatSend.addEventListener('click', () => {
        scrollToTop();
    });
});
