document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".cert-detail-btn").forEach(btn => {
        btn.addEventListener("click", () => {

            const title = btn.dataset.title || "";
            const provider = btn.dataset.provider || "";
            const desc = btn.dataset.desc || "";
            const techs = btn.dataset.tech ? btn.dataset.tech.split(",") : [];
            const date = btn.dataset.date || "";

            // Titre
            document.getElementById("certModalTitle").textContent = title;

            // Fournisseur
            document.getElementById("certModalProvider").innerHTML =
                `<strong>Organisme :</strong> ${provider}`;

            // Description
            document.getElementById("certModalDesc").textContent = desc;

            // Technologies / compétences
            const techList = document.getElementById("certModalTech");
            techList.innerHTML = "";

            if (techs.length > 0) {
                techs.forEach(t => {
                    const li = document.createElement("li");
                    li.textContent = t.trim();
                    techList.appendChild(li);
                });
            } else {
                techList.innerHTML = "<li>Aucune technologie spécifiée</li>";
            }

            // Date
            const dateEl = document.getElementById("certModalDate");
            if (date) {
                dateEl.textContent = `Certification obtenue le : ${date}`;
                dateEl.classList.remove("d-none");
            } else {
                dateEl.classList.add("d-none");
            }

        });
    });

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
