function login(event) {
  event.preventDefault();
  const email = document.querySelector('input[placeholder="Email"]').value;
  const password = document.querySelector('input[placeholder="Password"]').value;

  // Dummy check – You can replace with real auth later
  if (email === "user@gmail.com" && password === "123456") {
    alert("Login successful!");
    window.location.href = "dashboard.html"; // dashboard.html will be created later
  } else {
    alert("Invalid email or password.");
  }
}

function signup(event) {
  event.preventDefault();
  const name = document.querySelector('input[placeholder="Name"]').value;
  const email = document.querySelector('input[placeholder="Email"]').value;
  const password = document.querySelector('input[placeholder="Password"]').value;

  // Save to localStorage (simulated signup)
  localStorage.setItem("user", JSON.stringify({ name, email, password }));
  alert("Signup successful! Please login now.");
  window.location.href = "login.html";
}
