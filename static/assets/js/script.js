document.addEventListener("DOMContentLoaded", function () {

    const dateInput = document.getElementById("date");
    if (dateInput && window.location.pathname === "/add_donation") {
        dateInput.value = new Date().toISOString().split("T")[0];
    }

    const amountInput = document.getElementById("amount");
    if (amountInput) {
        amountInput.addEventListener("input", function () {
            if (this.value < 0) {
                this.value = "";
                alert("Amount cannot be negative.");
            }
        });
    }

    const flashMessage = document.querySelector(".flash-message");
    if (flashMessage) {
        setTimeout(() => {
            flashMessage.style.transition = "opacity 0.8s ease";
            flashMessage.style.opacity = "0";
        }, 3000);
    }

    const deleteButtons = document.querySelectorAll(".delete-btn");
    deleteButtons.forEach(btn => {
        btn.addEventListener("click", function (e) {
            if (!confirm("Are you sure?")) {
                e.preventDefault();
            }
        });
    });

});