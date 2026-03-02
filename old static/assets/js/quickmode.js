const funFacts = [
  "💡 1 in 8 women will be diagnosed with breast cancer in their lifetime.",
  "🧬 Early detection of cancer improves survival rates significantly.",
  "🍎 A healthy diet and regular exercise reduce the risk of many cancers.",
  "📊 Breast cancer is the most common cancer in women worldwide.",
  "🔬 AI tools can assist doctors with early and accurate diagnoses.",
  "🧪 Mammograms can detect breast cancer before a lump is felt.",
  "❤️ Regular self-exams can help catch changes early.",
  "🧠 Knowledge and awareness are key to early cancer detection.",
];

let factIndex = 0;
let factInterval;

function startRotation() {
  const factEl = document.getElementById("fun-fact");
  if (!factEl) return;

  factIndex = Math.floor(Math.random() * funFacts.length);
  factEl.textContent = funFacts[factIndex];

  factInterval = setInterval(() => {
    factIndex = (factIndex + 1) % funFacts.length;
    factEl.textContent = funFacts[factIndex];
  }, 2000);
}

function stopRotation() {
  clearInterval(factInterval);
}

document.addEventListener("DOMContentLoaded", function () {
  const forms = document.querySelectorAll("form[action='/predict_quick']");
  const spinner = document.getElementById("spinner-overlay");

  if (forms.length && spinner) {
    forms.forEach((form) => {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        spinner.style.display = "flex";
        startRotation();

        setTimeout(() => {
          stopRotation();
          spinner.classList.add("fade-out");
          form.submit();
        }, 7000);
      });
    });
  }

  document
    .getElementById("sliderModeBtn")
    .addEventListener("click", function () {
      document.getElementById("sliderform").classList.add("active");
      document.getElementById("manualform").classList.remove("active");
      this.classList.add("active");
      document.getElementById("manualModeBtn").classList.remove("active");
    });

  document
    .getElementById("manualModeBtn")
    .addEventListener("click", function () {
      document.getElementById("manualform").classList.add("active");
      document.getElementById("sliderform").classList.remove("active");
      this.classList.add("active");
      document.getElementById("sliderModeBtn").classList.remove("active");
    });
});

function syncInput(feature) {
  const slider = document.getElementById(`${feature}_slider`);
  const number = document.getElementById(`${feature}_number`);
  number.value = slider.value;
}

function syncSlider(feature) {
  const slider = document.getElementById(`${feature}_slider`);
  const number = document.getElementById(`${feature}_number`);
  slider.value = number.value;
}
