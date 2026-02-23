document.addEventListener("DOMContentLoaded", () => {
    const reveals = document.querySelectorAll(".reveal");

    const observer = new IntersectionObserver(
        entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("active");
                }
            });
        },
        { threshold: 0.15 }
    );

    reveals.forEach(el => observer.observe(el));
});


document.addEventListener("DOMContentLoaded", () => {
    const closeBtn = document.querySelector(".close-modal");
    const modal = document.querySelector(".success-modal-overlay");

    if (closeBtn && modal) {
        closeBtn.addEventListener("click", () => {
            modal.style.opacity = "0";

            setTimeout(() => {
                if (document.querySelector(".success-modal-overlay")) {
                    window.location.href = "/onglet/services/";
                }
            }, 300);
        });
    }
});