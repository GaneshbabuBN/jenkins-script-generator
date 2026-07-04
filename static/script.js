// =============================================
// Jenkins Script Generator UI Enhancements
// =============================================

// Wait until page loads

document.addEventListener("DOMContentLoaded", function () {

    // -----------------------------------------
    // Generate Button Loading State
    // -----------------------------------------

    const form = document.getElementById("generatorForm");

    if (form) {

        form.addEventListener("submit", function () {

            const button = form.querySelector("button[type='submit']");

            if (button) {

                button.disabled = true;

                button.innerHTML =
                    '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';

            }

            const overlay = document.getElementById("loadingOverlay");

            if (overlay) {

                overlay.style.display = "flex";

            }

        });

    }

    // -----------------------------------------
    // Auto Scroll to Generated Script
    // -----------------------------------------

    const generated = document.getElementById("generated_script");

    if (generated) {

        generated.scrollIntoView({

            behavior: "smooth",

            block: "start"

        });

    }

    // -----------------------------------------
    // Fade Animation
    // -----------------------------------------

    document.querySelectorAll(".card").forEach(function (card) {

        card.classList.add("fade-up");

    });

});

// =============================================
// Copy Script
// =============================================

function copyScript() {

    const textarea = document.getElementById("generated_script");

    if (!textarea) {

        return;

    }

    navigator.clipboard.writeText(textarea.value)

        .then(function () {

            const button = event.target.closest("button");

            if (button) {

                const original = button.innerHTML;

                button.innerHTML =
                    '<i class="bi bi-check-circle-fill me-2"></i>Copied';

                button.classList.remove("btn-success");

                button.classList.add("btn-primary");

                setTimeout(function () {

                    button.innerHTML = original;

                    button.classList.remove("btn-primary");

                    button.classList.add("btn-success");

                }, 1800);

            }

        })

        .catch(function () {

            textarea.select();

            document.execCommand("copy");

        });

}

// =============================================
// Keyboard Shortcut
// Ctrl + Shift + C
// =============================================

document.addEventListener("keydown", function (e) {

    if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === "c") {

        const textarea = document.getElementById("generated_script");

        if (textarea) {

            copyScript();

        }

    }

});