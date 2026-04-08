/**
 * Jaybird Automations AI Chat Widget
 * Connects to a Cloudflare Worker that proxies Claude API requests.
 * Captures leads (name, email) and stores them via the worker.
 */

(function () {
  'use strict';

  // ─── CONFIG ────────────────────────────────────────────────────────
  // IMPORTANT: Replace this with your actual Cloudflare Worker URL after deployment
  const WORKER_URL = 'https://jaybird-chat.lospatosllc23.workers.dev';
  // ─── STATE ─────────────────────────────────────────────────────────
  let conversationHistory = [];
  let isOpen = false;
  let isWaiting = false;
  let leadCaptured = false;

  // Try to restore state from sessionStorage
  try {
    const saved = sessionStorage.getItem('jb-chat-state');
    if (saved) {
      const state = JSON.parse(saved);
      conversationHistory = state.history || [];
      leadCaptured = state.leadCaptured || false;
    }
  } catch (e) { /* ignore */ }

  // ─── BUILD DOM ─────────────────────────────────────────────────────
  function buildWidget() {
    // Toggle button
    const toggle = document.createElement('button');
    toggle.id = 'jb-chat-toggle';
    toggle.setAttribute('aria-label', 'Chat with Jaybird AI');
    toggle.innerHTML = `
      <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/>
        <path d="M7 9h2v2H7zm4 0h2v2h-2zm4 0h2v2h-2z"/>
      </svg>`;
    toggle.addEventListener('click', toggleChat);

    // Chat window
    const win = document.createElement('div');
    win.id = 'jb-chat-window';
    win.innerHTML = `
      <div id="jb-chat-header">
        <div class="jb-avatar">&#9889;</div>
        <div class="jb-header-info">
          <div class="jb-header-name">Jaybird AI Assistant</div>
          <div class="jb-header-status">Online &mdash; Powered by AI</div>
        </div>
        <button id="jb-chat-close" aria-label="Close chat">&times;</button>
      </div>
      <div id="jb-chat-messages"></div>
      <div id="jb-chat-input-area">
        <textarea id="jb-chat-input" placeholder="Type your message..." rows="1"></textarea>
        <button id="jb-chat-send" aria-label="Send message">
          <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
        </button>
      </div>
      <div id="jb-chat-footer">Powered by Jaybird Automations AI</div>`;

    document.body.appendChild(toggle);
    document.body.appendChild(win);

    // Event listeners
    document.getElementById('jb-chat-close').addEventListener('click', toggleChat);
    document.getElementById('jb-chat-send').addEventListener('click', sendMessage);
    const input = document.getElementById('jb-chat-input');
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
    // Auto-resize textarea
    input.addEventListener('input', function () {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 80) + 'px';
    });

    // Restore messages if any
    if (conversationHistory.length > 0) {
      restoreMessages();
    }
  }

  // ─── TOGGLE ────────────────────────────────────────────────────────
  function toggleChat() {
    isOpen = !isOpen;
    const win = document.getElementById('jb-chat-window');
    const toggle = document.getElementById('jb-chat-toggle');

    if (isOpen) {
      win.classList.add('visible');
      toggle.classList.add('open');
      // Send welcome message on first open
      if (conversationHistory.length === 0) {
        showWelcome();
      }
      // Focus input
      setTimeout(() => document.getElementById('jb-chat-input').focus(), 300);
    } else {
      win.classList.remove('visible');
      toggle.classList.remove('open');
    }
  }

  // ─── WELCOME ───────────────────────────────────────────────────────
  function showWelcome() {
    const welcome = "Hey! I'm Jaybird's AI assistant. I can answer questions about our AI services, pricing, or help you book a free discovery call. What can I help you with?";
    addMessage('bot', welcome);
    conversationHistory.push({ role: 'assistant', content: welcome });

    // Add quick action buttons
    const messagesDiv = document.getElementById('jb-chat-messages');
    const quickDiv = document.createElement('div');
    quickDiv.className = 'jb-quick-actions';
    const quickButtons = [
      'What services do you offer?',
      'How much does it cost?',
      'Tell me about AI commercials',
      'I want to book a call'
    ];
    quickButtons.forEach(text => {
      const btn = document.createElement('button');
      btn.className = 'jb-quick-btn';
      btn.textContent = text;
      btn.addEventListener('click', function () {
        quickDiv.remove();
        document.getElementById('jb-chat-input').value = text;
        sendMessage();
      });
      quickDiv.appendChild(btn);
    });
    messagesDiv.appendChild(quickDiv);
    scrollToBottom();
    saveState();
  }

  // ─── SEND MESSAGE ──────────────────────────────────────────────────
  async function sendMessage() {
    const input = document.getElementById('jb-chat-input');
    const text = input.value.trim();
    if (!text || isWaiting) return;

    // Remove quick action buttons if present
    const quickActions = document.querySelector('.jb-quick-actions');
    if (quickActions) quickActions.remove();

    // Show user message
    addMessage('user', text);
    conversationHistory.push({ role: 'user', content: text });
    input.value = '';
    input.style.height = 'auto';

    // Show typing indicator
    isWaiting = true;
    document.getElementById('jb-chat-send').disabled = true;
    const typingEl = showTyping();

    try {
      const response = await fetch(WORKER_URL + '/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: conversationHistory,
          leadCaptured: leadCaptured
        })
      });

      if (!response.ok) throw new Error('Server error');

      const data = await response.json();
      typingEl.remove();

      // Show bot response
      addMessage('bot', data.reply);
      conversationHistory.push({ role: 'assistant', content: data.reply });

      // Check if lead was captured
      if (data.leadCaptured) {
        leadCaptured = true;
      }
    } catch (err) {
      typingEl.remove();
      addMessage('bot', "Sorry, I'm having trouble connecting right now. You can reach Jay directly at (702) 335-0344 or lospatosllc23@gmail.com!");
    }

    isWaiting = false;
    document.getElementById('jb-chat-send').disabled = false;
    saveState();
  }

  // ─── ADD MESSAGE ───────────────────────────────────────────────────
  function addMessage(type, text) {
    const messagesDiv = document.getElementById('jb-chat-messages');
    const msg = document.createElement('div');
    msg.className = 'jb-msg ' + type;

    if (type === 'bot') {
      msg.innerHTML = `
        <div class="jb-msg-avatar">&#9889;</div>
        <div class="jb-msg-bubble">${escapeHtml(text)}</div>`;
    } else {
      msg.innerHTML = `<div class="jb-msg-bubble">${escapeHtml(text)}</div>`;
    }

    messagesDiv.appendChild(msg);
    scrollToBottom();
  }

  // ─── TYPING INDICATOR ─────────────────────────────────────────────
  function showTyping() {
    const messagesDiv = document.getElementById('jb-chat-messages');
    const msg = document.createElement('div');
    msg.className = 'jb-msg bot';
    msg.id = 'jb-typing';
    msg.innerHTML = `
      <div class="jb-msg-avatar">&#9889;</div>
      <div class="jb-msg-bubble">
        <div class="jb-typing"><span></span><span></span><span></span></div>
      </div>`;
    messagesDiv.appendChild(msg);
    scrollToBottom();
    return msg;
  }

  // ─── RESTORE MESSAGES ─────────────────────────────────────────────
  function restoreMessages() {
    conversationHistory.forEach(msg => {
      if (msg.role === 'assistant') addMessage('bot', msg.content);
      else if (msg.role === 'user') addMessage('user', msg.content);
    });
  }

  // ─── HELPERS ───────────────────────────────────────────────────────
  function scrollToBottom() {
    const messagesDiv = document.getElementById('jb-chat-messages');
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function saveState() {
    try {
      sessionStorage.setItem('jb-chat-state', JSON.stringify({
        history: conversationHistory.slice(-20), // Keep last 20 messages
        leadCaptured: leadCaptured
      }));
    } catch (e) { /* ignore */ }
  }

  // ─── INIT ──────────────────────────────────────────────────────────
  // Load CSS
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = 'chatbot/chat-widget.css';
  document.head.appendChild(link);

  // Build widget when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildWidget);
  } else {
    buildWidget();
  }
})();
