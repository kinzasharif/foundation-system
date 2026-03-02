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
  }, 2500);
}

function stopRotation() {
  clearInterval(factInterval);
}

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector('form[action="/predict"]');
  const spinner = document.getElementById("spinner-overlay");

  if (form && spinner) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      spinner.style.display = "flex";
      startRotation();

      setTimeout(() => {
        spinner.classList.add("fade-out");
        stopRotation();
        form.submit();
      }, 7000);
    });
  }

  //scroll to result logic for template
  const resultWrapper = document.querySelector(".result-wrapper");
  if (resultWrapper) {
    setTimeout(() => {
      resultWrapper.scrollIntoView({ behavior: "smooth", block: "center" });
    }, 300);
  }
});
