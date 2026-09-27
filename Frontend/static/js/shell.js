/**
 * core/shell.js — app-shell behavior shared across every feature panel:
 * connection-status polling (sidebar dot, topbar pill) and the
 * "New session" action. Feature-specific behavior (e.g. sending chat
 * messages) lives in each feature's own static/js file.
 */

window.KynOpsShell = (() => {
  const statusDot = document.getElementById("statusDot");
  const statusText = document.getElementById("statusText");
  const onlinePill = document.getElementById("onlinePill");

  let connected = false;
  const listeners = [];

  function setConnected(isConnected) {
    connected = isConnected;

    statusDot.classList.toggle("online", isConnected);
    statusDot.classList.toggle("offline", !isConnected);
    statusText.textContent = isConnected ? "Connected" : "Disconnected";

    onlinePill.classList.toggle("offline", !isConnected);
    onlinePill.lastChild.textContent = isConnected ? " Agent Online" : " Agent Offline";

    listeners.forEach((fn) => fn(isConnected));
  }

  async function refreshStatus() {
    try {
      const res = await fetch("/api/status");
      const data = await res.json();
      setConnected(Boolean(data.connected));
    } catch {
      setConnected(false);
    }
  }

  function onStatusChange(fn) {
    listeners.push(fn);
    fn(connected); // sync immediately with current state
  }

  document.getElementById("newSessionBtn").addEventListener("click", () => {
    document.dispatchEvent(new CustomEvent("kyn:new-session"));
  });

  refreshStatus();
  setInterval(refreshStatus, 30000);

  return { refreshStatus, onStatusChange, isConnected: () => connected };
})();
