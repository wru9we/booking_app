const output = document.getElementById("output");
const hotelsTable = document.getElementById("hotels-table");
const bookingsTable = document.getElementById("bookings-table");

function setDefaultDates() {
  const from = document.getElementById("date-from");
  const to = document.getElementById("date-to");
  const today = new Date();
  const later = new Date(today);
  later.setDate(today.getDate() + 3);
  from.value = today.toISOString().slice(0, 10);
  to.value = later.toISOString().slice(0, 10);
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    credentials: "include",
    ...options,
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...options.headers,
    },
  });

  const text = await response.text();
  let data = null;
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
  }

  showResult(response.status, data, response.ok);
  return { ok: response.ok, status: response.status, data };
}

function showResult(status, data, ok) {
  output.className = ok ? "ok" : "error";
  output.textContent = `HTTP ${status}\n\n${formatData(data)}`;
}

function formatData(data) {
  if (data == null || data === "") return "(пустое тело)";
  if (typeof data === "string") return data;
  return JSON.stringify(data, null, 2);
}

function renderTable(container, rows) {
  if (!Array.isArray(rows) || rows.length === 0) {
    container.innerHTML = "<p>Нет данных</p>";
    return;
  }

  const keys = Object.keys(rows[0]);
  const head = keys.map((key) => `<th>${escapeHtml(key)}</th>`).join("");
  const body = rows
    .map(
      (row) =>
        `<tr>${keys
          .map((key) => `<td>${escapeHtml(formatCell(row[key]))}</td>`)
          .join("")}</tr>`
    )
    .join("");

  container.innerHTML = `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
}

function formatCell(value) {
  if (value == null) return "";
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function authBody() {
  return JSON.stringify({
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
  });
}

const actions = {
  async register() {
    await api("/auth/register", { method: "POST", body: authBody() });
  },
  async login() {
    await api("/auth/login", { method: "POST", body: authBody() });
  },
  async logout() {
    await api("/auth/logout", { method: "POST" });
  },
  async me() {
    await api("/auth/me");
  },
  async hotels() {
    const { ok, data } = await api("/hotels");
    if (ok) renderTable(hotelsTable, Array.isArray(data) ? data : [data]);
  },
  async "my-bookings"() {
    const { ok, data } = await api("/bookings");
    if (ok) renderTable(bookingsTable, Array.isArray(data) ? data : [data]);
  },
  async "booking-one"() {
    const { ok, data } = await api("/bookings/one");
    if (ok) renderTable(bookingsTable, data ? [data] : []);
  },
  async "booking-by-id"() {
    const id = document.getElementById("booking-id").value;
    const { ok, data } = await api(`/bookings/${id}`);
    if (ok) renderTable(bookingsTable, data ? [data] : []);
  },
  async "add-booking"() {
    const params = new URLSearchParams({
      room_id: document.getElementById("room-id").value,
      date_from: document.getElementById("date-from").value,
      date_to: document.getElementById("date-to").value,
    });
    await api(`/bookings?${params}`, { method: "POST" });
  },
};

document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-action]");
  if (!button) return;
  const action = actions[button.dataset.action];
  if (!action) return;
  action().catch((error) => {
    showResult(0, String(error), false);
  });
});

setDefaultDates();
