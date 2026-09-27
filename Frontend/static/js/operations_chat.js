/**
 * features/operations_chat/operations_chat.js — chat panel behavior:
 * sending messages to /api/chat, rendering the conversation, quick-action
 * chips, and syncing the Agent Context panel's mode indicator with the
 * shared connection status from core/shell.js.
 */

(() => {
  const chatMessages = document.getElementById("chatMessages");
  const chatForm = document.getElementById("chatForm");
  const chatInput = document.getElementById("chatInput");
  const sendBtn = document.getElementById("sendBtn");
  const charCount = document.getElementById("charCount");
  const integrationStatusBtn = document.getElementById("integrationStatusBtn");

  const modeDot = document.getElementById("modeDot");
  const modeText = document.getElementById("modeText");

  const MAX_LEN = 4000;
  let history = [];
  let sending = false;

  function timeNow() {
    return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  document.querySelectorAll("[data-now]").forEach((el) => (el.textContent = timeNow()));

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function appendMessage({ role, text }) {
    const wrap = document.createElement("div");
    wrap.className = `msg msg-${role}`;

    const avatar = document.createElement("div");
    avatar.className = `msg-avatar msg-avatar-${role === "user" ? "user" : "agent"}`;
    avatar.innerHTML =
      role === "user"
        ? '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 4-6 8-6s8 2 8 6"/></svg>'
        : '<svg viewBox="0 0 24 24"><path d="M12 2l1.5 3.5L17 7l-3.5 1.5L12 12l-1.5-3.5L7 7l3.5-1.5L12 2z"/></svg>';

    const bubble = document.createElement("div");
    bubble.className = "msg-bubble";

    const meta = document.createElement("div");
    meta.className = "msg-meta";
    meta.textContent = `${role === "user" ? "You" : "OpsAgent"} · ${timeNow()}`;

    const body = document.createElement("div");
    body.className = "msg-text";
    body.textContent = text;

    bubble.appendChild(meta);
    bubble.appendChild(body);
    wrap.appendChild(avatar);
    wrap.appendChild(bubble);
    chatMessages.appendChild(wrap);
    scrollToBottom();
    return wrap;
  }

  function appendSystemNotice(text) {
    const wrap = document.createElement("div");
    wrap.className = "msg msg-agent msg-system";
    wrap.innerHTML = `
      <div class="msg-avatar msg-avatar-agent">
        <svg viewBox="0 0 24 24"><path d="M12 9v4m0 4h.01M10.3 3.9L2.6 18a2 2 0 001.7 3h15.4a2 2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0z"/></svg>
      </div>
      <div class="msg-bubble"><div class="msg-text">${text}</div></div>`;
    chatMessages.appendChild(wrap);
    scrollToBottom();
  }

  function appendTypingIndicator() {
    const wrap = document.createElement("div");
    wrap.className = "msg msg-agent";
    wrap.id = "typingIndicator";
    wrap.innerHTML = `
      <div class="msg-avatar msg-avatar-agent">
        <svg viewBox="0 0 24 24"><path d="M12 2l1.5 3.5L17 7l-3.5 1.5L12 12l-1.5-3.5L7 7l3.5-1.5L12 2z"/></svg>
      </div>
      <div class="msg-bubble">
        <div class="typing-dots"><span></span><span></span><span></span></div>
      </div>`;
    chatMessages.appendChild(wrap);
    scrollToBottom();
  }

  function removeTypingIndicator() {
    document.getElementById("typingIndicator")?.remove();
  }

  function autoGrow() {
    chatInput.style.height = "auto";
    chatInput.style.height = Math.min(chatInput.scrollHeight, 140) + "px";
  }

  async function sendMessage(text) {
    if (!text.trim() || sending) return;
    sending = true;
    sendBtn.disabled = true;

    appendMessage({ role: "user", text });
    history.push({ role: "user", content: text });

    chatInput.value = "";
    charCount.textContent = `0/${MAX_LEN}`;
    autoGrow();

    appendTypingIndicator();

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, history }),
      });
      const data = await res.json();
      removeTypingIndicator();

      if (!res.ok) {
        appendSystemNotice(data.error || "Failed to fetch");
        window.KynOpsShell.refreshStatus();
        return;
      }

      appendMessage({ role: "agent", text: data.reply });
      history.push({ role: "assistant", content: data.reply });
      window.KynOpsShell.refreshStatus();
    } catch {
      removeTypingIndicator();
      appendSystemNotice("Failed to fetch");
      window.KynOpsShell.refreshStatus();
    } finally {
      sending = false;
      sendBtn.disabled = false;
    }
  }

  function resetSession() {
    history = [];
    chatMessages.innerHTML = "";
    appendMessage({
      role: "agent",
      text: "New session started. Ask for an incident summary, active P1 incidents, probable cause guidance, or a safe recommended next action.",
    });
  }

  // ---------- events ----------
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    sendMessage(chatInput.value);
  });

  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(chatInput.value);
    }
  });

  chatInput.addEventListener("input", () => {
    charCount.textContent = `${chatInput.value.length}/${MAX_LEN}`;
    autoGrow();
  });

  document.querySelectorAll(".chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      chatInput.value = chip.dataset.prompt;
      charCount.textContent = `${chatInput.value.length}/${MAX_LEN}`;
      autoGrow();
      chatInput.focus();
    });
  });

  integrationStatusBtn.addEventListener("click", () => window.KynOpsShell.refreshStatus());

  // core/shell.js emits this when "New session" is clicked in the topbar
  document.addEventListener("kyn:new-session", resetSession);

  // keep the context panel's mode indicator in sync with the shared status
  window.KynOpsShell.onStatusChange((connected) => {
    modeDot.classList.toggle("online", connected);
    modeDot.classList.toggle("offline", !connected);
    modeText.textContent = connected ? "Connected" : "Failed to fetch";
  });
})();
