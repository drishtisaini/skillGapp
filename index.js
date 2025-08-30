document.addEventListener('DOMContentLoaded', () => {

  // Smooth scrolling
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      const target = document.querySelector(link.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
  });

  // Theme toggle
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      document.body.classList.toggle('dark-mode');
      themeToggle.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
    });
  }

  // Modal handling
  const signinBtn = document.querySelector('.btn-link');
  const getStartedBtn = document.querySelector('.btn-primary');
  const signinModal = document.getElementById('signin-modal');
  const getStartedModal = document.getElementById('getstarted-modal');
  const closes = document.querySelectorAll('[data-close]');

  if (signinBtn && signinModal) {
    signinBtn.addEventListener('click', () => signinModal.style.display = 'flex');
  }
  if (getStartedBtn && getStartedModal) {
    getStartedBtn.addEventListener('click', () => getStartedModal.style.display = 'flex');
  }

  closes.forEach(btn => {
    btn.addEventListener('click', () => {
      if (signinModal) signinModal.style.display = 'none';
      if (getStartedModal) getStartedModal.style.display = 'none';
    });
  });

  window.addEventListener('click', e => {
    if (e.target === signinModal) signinModal.style.display = 'none';
    if (e.target === getStartedModal) getStartedModal.style.display = 'none';
  });

  const signinSubmit = document.getElementById('signin-submit');
  if (signinSubmit) {
    signinSubmit.addEventListener('click', () => {
      if (signinModal) signinModal.style.display = 'none';
      window.location.href = 'dashboard.html';
    });
  }

  const getStartedSubmit = document.getElementById('getstarted-submit');
  if (getStartedSubmit) {
    getStartedSubmit.addEventListener('click', () => {
      if (getStartedModal) getStartedModal.style.display = 'none';
      window.location.href = 'dashboard.html';
    });
  }

  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => window.location.href = 'index.html');
  }

  // Notifications
  const notificationBtn = document.getElementById('notification-btn');
  const notificationDropdown = document.getElementById('notification-dropdown');
  const notificationCount = document.getElementById('notification-count');

  function updateNotificationCount() {
    if (!notificationDropdown || !notificationCount) return;
    const unreadItems = notificationDropdown.querySelectorAll('.notification-item.unread').length;
    if (unreadItems > 0) {
      notificationCount.textContent = unreadItems;
      notificationCount.style.display = 'inline';
    } else {
      notificationCount.style.display = 'none';
    }
  }

  updateNotificationCount();

  if (notificationBtn && notificationDropdown) {
    notificationBtn.addEventListener('click', () => {
      const isVisible = notificationDropdown.style.display === 'block';
      notificationDropdown.style.display = isVisible ? 'none' : 'block';
    });
  }

  if (notificationDropdown) {
    notificationDropdown.addEventListener('click', e => {
      const item = e.target.closest('.notification-item');
      if (!item) return;
      if (e.target.classList.contains('mark-read')) {
        item.classList.remove('unread');
        e.target.remove();
      } else if (e.target.classList.contains('delete')) {
        item.remove();
      }
      updateNotificationCount();
    });
  }

  document.addEventListener('click', e => {
    if (notificationDropdown && !notificationDropdown.contains(e.target) && e.target !== notificationBtn) {
      notificationDropdown.style.display = 'none';
    }
  });

  // Drag & Drop
  document.querySelectorAll('.draggable').forEach(item => {
    item.addEventListener('dragstart', e => {
      e.dataTransfer.setData('text/plain', e.target.id);
    });
  });

  document.querySelectorAll('.dropzone').forEach(zone => {
    zone.addEventListener('dragover', e => e.preventDefault());
    zone.addEventListener('drop', e => {
      e.preventDefault();
      const id = e.dataTransfer.getData('text/plain');
      const dragged = document.getElementById(id);
      if (dragged) zone.appendChild(dragged);
    });
  });

  // Wizard / onboarding steps (if present on page)
  const steps = document.querySelectorAll('.step');
  const nextBtn = document.getElementById('nextBtn');
  const prevBtn = document.getElementById('prevBtn');
  const progress = document.getElementById('progress');
  let currentStep = 0;

  function showStep(n) {
    if (!steps.length) return;
    steps.forEach((step, index) => {
      step.classList.toggle('active', index === n);
    });
    if (prevBtn) prevBtn.style.display = n === 0 ? 'none' : 'inline-block';
    if (nextBtn) nextBtn.innerHTML = n === steps.length - 1 ? 'Finish' : 'Next';
    if (progress) progress.style.width = ((n + 1) / steps.length) * 100 + '%';
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (currentStep < steps.length - 1) {
        currentStep++;
        showStep(currentStep);
      } 
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (currentStep > 0) {
        currentStep--;
        showStep(currentStep);
      }
    });
  }

  showStep(currentStep);

  // Profile setup button
  const profileBtn = document.getElementById('profileSetupBtn');
  if (profileBtn) {
    profileBtn.addEventListener('click', () => {
      window.location.href = 'onboarding.html';
    });
  }

});



const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");
const steps = document.querySelectorAll(".step");
let currentStep = 0;

nextBtn.addEventListener("click", () => {
  // Hide current step
  steps[currentStep].classList.remove("active");

  // Move to next step
  currentStep++;

  // If it's the last step, redirect to dashboard.html
  if (currentStep >= steps.length) {
    window.location.href = "dashboard.html";
    return;
  }

  // Show next step
  steps[currentStep].classList.add("active");

  // Optional: update progress bar here
});

prevBtn.addEventListener("click", () => {
  if (currentStep > 0) {
    steps[currentStep].classList.remove("active");
    currentStep--;
    steps[currentStep].classList.add("active");
  }
});
