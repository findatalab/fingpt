const chatForm = document.getElementById('chat-form');
const input = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');

function renderMarkdown(text) {
    if (!window.marked || !window.DOMPurify) {
        return text;
    }

    const rawHtml = window.marked.parse(text, {
        breaks: true,
        gfm: true,
    });

    return window.DOMPurify.sanitize(rawHtml);
}

function hydrateMarkdownMessages() {
    const markdownBodies = chatBox.querySelectorAll('.message-body[data-markdown]');

    markdownBodies.forEach((body) => {
        const sourceText = body.textContent;
        body.innerHTML = renderMarkdown(sourceText);
    });
}

function appendMessage(role, sender, text) {
    const message = document.createElement('div');
    message.className = `message ${role}`;

    const senderNode = document.createElement('span');
    senderNode.className = 'sender';
    senderNode.textContent = sender;

    const bodyNode = document.createElement('div');
    bodyNode.className = 'message-body';

    if (role === 'llm') {
        bodyNode.dataset.markdown = 'true';
        bodyNode.innerHTML = renderMarkdown(text);
    } else {
        bodyNode.textContent = text;
    }

    message.appendChild(senderNode);
    message.appendChild(bodyNode);
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

hydrateMarkdownMessages();
chatBox.scrollTop = chatBox.scrollHeight;

chatForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    const userMessage = input.value.trim();
    if (!userMessage) return;

    appendMessage('user', 'Вы: ', userMessage);
    input.value = '';
    input.focus();

    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
    });
    const data = await response.json();
    appendMessage('llm', 'FinGPT: ', data.reply);
});