document.addEventListener("DOMContentLoaded", () => {

    const buttons = document.querySelectorAll(".project-detail-btn");
    if (!buttons.length) return;

    const titleEl = document.getElementById("projectModalTitle");
    const descEl = document.getElementById("projectModalDesc");
    const techEl = document.getElementById("projectModalTech");
    const imgEl = document.getElementById("projectModalImage");

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {

            titleEl.textContent = btn.dataset.title;
            descEl.textContent = btn.dataset.desc;

            // Image
            if (btn.dataset.image) {
                imgEl.src = btn.dataset.image;
                imgEl.classList.remove("d-none");
            } else {
                imgEl.classList.add("d-none");
            }

            // Technologies
            techEl.innerHTML = "";
            if (btn.dataset.tech) {
                btn.dataset.tech.split(",").forEach(t => {
                    const li = document.createElement("li");
                    li.textContent = t.trim();
                    techEl.appendChild(li);
                });
            }
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


document.querySelectorAll(".btn-like").forEach(btn => {
    btn.addEventListener("click", function () {
        const projectId = this.dataset.id;
        const likeCount = this.querySelector(".like-count");

        fetch(`/project/${projectId}/like/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "X-Requested-With": "XMLHttpRequest"
            }
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === "success") {
                    likeCount.textContent = data.likes;
                    btn.classList.add("liked");
                    btn.disabled = true;
                } else {
                    alert("Vous avez déjà liké ce projet.");
                }
            })
            .catch(() => alert("Erreur lors du like."));
    });
});

// CSRF helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        document.cookie.split(";").forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}