function login(event) {
  event.preventDefault();
  const email = document.querySelector('input[placeholder="Email"]').value;
  const password = document.querySelector('input[placeholder="Password"]').value;

  const storedUser = JSON.parse(localStorage.getItem("user"));

  if (storedUser && storedUser.email === email && storedUser.password === password) {
    alert("Login successful!");
    localStorage.setItem("loggedIn", "true");
    window.location.href = "dashboard.html";
  } else {
    alert("Invalid email or password.");
  }
}

function signup(event) {
  event.preventDefault();
  const name = document.querySelector('input[placeholder="Name"]').value;
  const email = document.querySelector('input[placeholder="Email"]').value;
  const password = document.querySelector('input[placeholder="Password"]').value;

  localStorage.setItem("user", JSON.stringify({ name, email, password }));
  alert("Signup successful! Please login now.");
  window.location.href = "login.html";
}

// Dashboard access control
if (window.location.pathname.includes("dashboard.html")) {
  const isLoggedIn = localStorage.getItem("loggedIn");
  if (isLoggedIn !== "true") {
    alert("Please log in first.");
    window.location.href = "login.html";
  }

  // Logout button
  const logoutBtn = document.querySelector(".logout");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      localStorage.removeItem("loggedIn");
      window.location.href = "login.html";
    });
  }
}

if (window.location.pathname.includes("dashboard.html")) {
  const isLoggedIn = localStorage.getItem("loggedIn");
  if (isLoggedIn !== "true") {
    alert("Please log in first.");
    window.location.href = "login.html";
  }

  const user = JSON.parse(localStorage.getItem("user"));
  if (user && user.name) {
    const welcomeEl = document.getElementById("welcome-message");
    if (welcomeEl) {
      welcomeEl.textContent = `Welcome, ${user.name}! 👋`;
    }
  }

  const logoutBtn = document.querySelector(".logout");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      localStorage.removeItem("loggedIn");
      window.location.href = "login.html";
    });
  }
}