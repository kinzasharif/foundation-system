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

// Flash message auto-dismiss with cool animations
document.addEventListener("DOMContentLoaded", function() {
    const flashMessages = document.querySelectorAll(".alert");
    
    flashMessages.forEach(function(message) {
        // Add close button functionality
        const closeBtn = message.querySelector(".close");
        if (closeBtn) {
            closeBtn.addEventListener("click", function() {
                dismissMessage(message);
            });
        }
        
        // Auto dismiss after 5 seconds
        setTimeout(function() {
            dismissMessage(message);
        }, 5000);
    });
    
    function dismissMessage(message) {
        // Add slide-out animation
        message.style.animation = "slideOut 0.5s ease forwards";
        
        // Remove from DOM after animation
        setTimeout(function() {
            if (message.parentNode) {
                message.remove();
                
                // Remove the container if it's empty
                const container = document.querySelector(".container");
                if (container && container.children.length === 0) {
                    container.remove();
                }
            }
        }, 500);
    }
});