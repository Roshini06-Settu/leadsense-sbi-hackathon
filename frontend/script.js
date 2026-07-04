const API_URL = "http://localhost:5000";

// Generate/persist a simple visitor ID for this session
let visitorId = sessionStorage.getItem("visitor_id");
if (!visitorId) {
  visitorId = "visitor_" + Math.floor(Math.random() * 100000);
  sessionStorage.setItem("visitor_id", visitorId);
}
document.getElementById("visitorIdDisplay").innerText = visitorId;

// Tracking state (in-memory, resets on page reload — fine for a demo)
let state = {
  pages_visited: 0,
  time_on_site_seconds: 0,
  used_calculator: false,
  started_application: false,
  completed_application: false,
  revisits: 0,
  visitedPages: new Set()
};

let startTime = Date.now();

function updateTimeSpent() {
  state.time_on_site_seconds = Math.floor((Date.now() - startTime) / 1000);
}

function visitPage(pageId) {
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  document.getElementById(pageId).classList.add("active");

  if (state.visitedPages.has(pageId)) {
    state.revisits += 1;
  } else {
    state.visitedPages.add(pageId);
    state.pages_visited += 1;
  }

  sendEvent();
}

function useCalculator() {
  const amount = document.getElementById("loanAmount").value;
  const tenure = document.getElementById("tenure").value;
  const rate = 8.5 / 12 / 100;
  const months = tenure * 12;
  const emi = (amount * rate * Math.pow(1 + rate, months)) / (Math.pow(1 + rate, months) - 1);
  document.getElementById("emiResult").innerText = "Estimated EMI: ₹" + emi.toFixed(2);

  state.used_calculator = true;
  sendEvent();
}

function startApplication() {
  state.started_application = true;
  sendEvent();
}

function completeApplication() {
  state.completed_application = true;
  sendEvent();
}

function sendEvent() {
  updateTimeSpent();

  const payload = {
    visitor_id: visitorId,
    pages_visited: state.pages_visited,
    time_on_site_seconds: state.time_on_site_seconds,
    used_calculator: state.used_calculator,
    started_application: state.started_application,
    completed_application: state.completed_application,
    revisits: state.revisits
  };

  fetch(API_URL + "/track", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("liveScore").innerText = data.score;
      document.getElementById("liveLabel").innerText = "(" + data.label + ")";
    })
    .catch(err => console.error("Tracking error:", err));
}

// Send an initial event on page load
window.addEventListener("load", () => {
  state.pages_visited = 1;
  state.visitedPages.add("home");
  sendEvent();
});

// Periodically update time-on-site while user stays on page
setInterval(sendEvent, 15000);
