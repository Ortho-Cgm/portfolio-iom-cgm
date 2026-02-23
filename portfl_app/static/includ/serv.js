document.addEventListener("DOMContentLoaded", () => {

    const buttons = document.querySelectorAll('.service-detail-btn');
    if (!buttons.length) return;

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {

            const title = btn.dataset.title;
            const icon = btn.dataset.icon;
            const desc = btn.dataset.desc;
            const tips = btn.dataset.tips.split('|');

            const modalTitle = document.getElementById('modalTitle');
            const modalIcon = document.getElementById('modalIcon');
            const modalDesc = document.getElementById('modalDesc');
            const tipsList = document.getElementById('modalTips');

            if (!modalTitle || !modalDesc || !tipsList) return;

            modalTitle.textContent = title;
            modalIcon.className = `fa-solid ${icon}`;
            modalDesc.textContent = desc;

            tipsList.innerHTML = '';
            tips.forEach(tip => {
                const li = document.createElement('li');
                li.textContent = tip;
                tipsList.appendChild(li);
            });
        });
    });
});


document.addEventListener("DOMContentLoaded", () => {
    if (window.location.hash === "#reviews") {
        const section = document.querySelector("#reviews");
        if (section) {
            section.scrollIntoView({ behavior: "smooth" });
        }
    }
});

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
        {
            threshold: 0.15,
            rootMargin: "0px 0px -80px 0px"
        }
    );

    reveals.forEach(el => observer.observe(el));
});

