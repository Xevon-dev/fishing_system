document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector(".home-page");
  if (!page) return;

  const calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!calm) {
    const visual = page.querySelector(".home-visual");
    const shift = page.querySelector(".home-visual__shift");

    if (visual && shift) {
      visual.addEventListener("pointermove", (event) => {
        const box = visual.getBoundingClientRect();
        const x = (event.clientX - box.left) / box.width - 0.5;
        const y = (event.clientY - box.top) / box.height - 0.5;
        shift.style.transform = `scale(1.02) translate(${(x * -12).toFixed(1)}px, ${(y * -9).toFixed(1)}px)`;
      });
      visual.addEventListener("pointerleave", () => {
        shift.style.transform = "";
      });
    }

    page.querySelectorAll(".home-feature-card").forEach((card) => {
      card.addEventListener("pointermove", (event) => {
        const box = card.getBoundingClientRect();
        const x = (event.clientX - box.left) / box.width - 0.5;
        const y = (event.clientY - box.top) / box.height - 0.5;
        card.style.transform = `translateY(-6px) rotateX(${(y * -3).toFixed(2)}deg) rotateY(${(x * 3).toFixed(2)}deg)`;
      });
      card.addEventListener("pointerleave", () => {
        card.style.transform = "";
      });
    });
  }

  if (!("IntersectionObserver" in window)) return;

  const targets = page.querySelectorAll(
    ".home-section-heading, .home-feature-card, .home-level-cta__panel, .home-footer__inner",
  );
  if (!targets.length) return;

  page.classList.add("home-motion-ready");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -35px 0px" },
  );

  targets.forEach((target) => observer.observe(target));
});
