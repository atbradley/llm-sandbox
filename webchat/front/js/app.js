var chat = [];
var converter = new showdown.Converter();

var messagesDiv = document.getElementById("messages-div");

document.addEventListener('qChatBefore', function(event) {
    console.log("Before message send:", event.detail.content);
    chat.push({ role: "user", content: event.detail.content });
    sendMessage(chat);
    
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

async function sendMessage(chat) {
    console.log("Sending message:", chat);
    try {
        const response = await fetch('http://localhost:7000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(chat)
        });
        chat = await response.json();
        console.log("Response from server:", data);
    } catch (error) {
        console.error("Error sending message:", error);
    }

    // Display the message in messagesDiv or send to a server
    let message = chat[chat.length-1].content;
    let html      = converter.makeHtml(message);
    document.dispatchEvent(new CustomEvent("qChatReceive", {
        detail: { content: html }
    }));

    // scroll #messages-div to bottom
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

document.dispatchEvent(new CustomEvent("qChatReceive", {
    detail: { content: "<p>Hello. How can I help?</p>" }
}));