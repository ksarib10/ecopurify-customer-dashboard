console.log("dashboard.js loaded");

document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("overlay");
  const hamburger = document.getElementById("hamburger");

  console.log("sidebar:", sidebar);
  console.log("overlay:", overlay);
  console.log("hamburger:", hamburger);

  if (!sidebar || !overlay || !hamburger) {
    alert("Sidebar elements missing. Check IDs.");
    return;
  }

  hamburger.onclick = () => {
    sidebar.classList.toggle("open");
    overlay.classList.toggle("show");
  };

  overlay.onclick = () => {
    sidebar.classList.remove("open");
    overlay.classList.remove("show");
  };
});


document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".plant-item").forEach(item => {
    item.addEventListener("click", async () => {
      const plantId = item.dataset.plantId;

      await fetch("/set-active-plant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plant_id: plantId })
      });

      window.location.reload();
    });
  });
});

function updateClock() {
  const clockEl = document.getElementById("clock");
  if (!clockEl) return;

  const now = new Date();

  let hours = now.getHours();
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const seconds = String(now.getSeconds()).padStart(2, "0");

  const ampm = hours >= 12 ? "PM" : "AM";
  hours = hours % 12 || 12;

  clockEl.textContent = `${hours}:${minutes}:${seconds} ${ampm}`;
}

updateClock();
setInterval(updateClock, 1000);


// Refresh button UX protection
document.addEventListener("DOMContentLoaded", () => {
  const refreshBtn = document.getElementById("refreshBtn");

  if (refreshBtn) {
    refreshBtn.addEventListener("click", () => {
      refreshBtn.disabled = true;
      refreshBtn.textContent = "Refreshing…";
      refreshBtn.classList.add("disabled");

      // let backend handle redirect
      window.location.href = "/refresh";
    });
  }
});


