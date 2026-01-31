console.log("login.js loaded");


const form = document.getElementById("loginForm");
const errorMsg = document.getElementById("errorMsg");
const button = document.getElementById("loginBtn");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorMsg.textContent = "";

  const customer_id = document.getElementById("customer_id").value.trim();
  const password = document.getElementById("password").value.trim();

  button.textContent = "Logging in...";
  button.disabled = true;

  try {
    const response = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify({ customer_id, password })
    });


    let result = {};
    try {
      result = await response.json();
    } catch (e) {
      // ignore JSON parse errors
    }
    if (response.ok) {
      window.location.href = "/dashboard";
    }

    if (!response.ok) {
      errorMsg.textContent = result.message || "Invalid credentials";
      button.textContent = "Login";
      button.disabled = false;
      return;
    }


  } catch (error) {
    errorMsg.textContent = "Server error. Please try again.";
    button.textContent = "Login";
    button.disabled = false;
  }
});

const passwordInput = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");

if (togglePassword && passwordInput) {
  togglePassword.addEventListener("click", () => {
    const isHidden = passwordInput.type === "password";

    passwordInput.type = isHidden ? "text" : "password";
    togglePassword.textContent = isHidden ? "🙈" : "👁️";
  });
}