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
    detail: { content: "<p>I'm baby pabst VHS synth, roof party letterpress prism tacos fanny pack lumbersexual. Edison bulb hashtag 3 wolf moon biodiesel viral, bodega boys tumblr lomo. Kitsch meditation tofu, selfies bespoke cray flannel. Crucifix cray retro, authentic wayfarers blackbird spyplane XOXO DIY viral. Synth VHS artisan 3 wolf moon occupy austin subway tile. Palo santo edison bulb iPhone, tattooed master cleanse yuccie same street art.</p>" }
}));

document.dispatchEvent(new CustomEvent("qChatReceive", {
    detail: { content: "<p>I'm baby williamsburg squid deep v beard, bicycle rights yr cornhole. Ugh deep v freegan, typewriter poutine neutral milk hotel sriracha kitsch. Cold-pressed hell of succulents unicorn. Whatever hexagon ugh gatekeep keffiyeh ethical narwhal bicycle rights lumbersexual woke praxis snackwave. Organic gatekeep freegan forage, bushwick bruh crucifix. Synth gluten-free hell of, pinterest big mood bodega boys hot chicken kogi yr prism selvage bespoke chia green juice. Paleo 90's small batch umami occupy ramps salvia blog readymade.</p>" }
}));