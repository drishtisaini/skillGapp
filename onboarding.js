let currentStep = 0;
const steps = document.querySelectorAll(".step");
const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");
const progress = document.getElementById("progress");

showStep(currentStep);

function showStep(n) {
  steps.forEach((step, index) => {
    step.classList.remove("active");
    if (index === n) step.classList.add("active");
  });

  // Handle button visibility
  prevBtn.style.display = n === 0 ? "none" : "inline-block";
  nextBtn.innerHTML = n === steps.length - 1 ? "Finish" : "Next";

  // Update progress bar
  progress.style.width = ((n + 1) / steps.length) * 100 + "%";
}

nextBtn.addEventListener("click", () => {
  if (currentStep < steps.length - 1) {
    currentStep++;
    showStep(currentStep);
  } else {
    alert("🎉 Onboarding Complete! Welcome aboard.");
    document.getElementById("onboardingForm").reset();
    currentStep = 0;
    showStep(currentStep);
  }
});

prevBtn.addEventListener("click", () => {
  if (currentStep > 0) {
    currentStep--;
    showStep(currentStep);
  }
});
