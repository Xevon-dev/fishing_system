document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".tip-reaction-form").forEach((form) => {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const button = form.querySelector("button[type='submit']");
      if (!button || button.disabled) return;

      button.disabled = true;
      try {
        const response = await fetch(form.action, {
          method: "POST",
          body: new FormData(form),
          credentials: "same-origin",
          headers: { "X-Requested-With": "XMLHttpRequest", Accept: "application/json" },
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || "Не вдалося зберегти оцінку.");

        const card = form.closest(".tip-card");
        const likeForm = card?.querySelector(".tip-reaction-form input[name='reaction'][value='like']")?.closest(".tip-reaction-form");
        const dislikeForm = card?.querySelector(".tip-reaction-form input[name='reaction'][value='dislike']")?.closest(".tip-reaction-form");
        const likeButton = likeForm?.querySelector("button");
        const dislikeButton = dislikeForm?.querySelector("button");

        if (likeButton) {
          likeButton.querySelector("[data-reaction-count]").textContent = result.likes;
          likeButton.classList.toggle("is-liked", result.reaction === "like");
          likeButton.setAttribute("aria-pressed", String(result.reaction === "like"));
        }
        if (dislikeButton) {
          dislikeButton.querySelector("[data-reaction-count]").textContent = result.dislikes;
          dislikeButton.classList.toggle("is-disliked", result.reaction === "dislike");
          dislikeButton.setAttribute("aria-pressed", String(result.reaction === "dislike"));
        }
      } catch (error) {
        const card = form.closest(".tip-card");
        let notice = card?.querySelector(".tip-reaction-error");
        if (card && !notice) {
          notice = document.createElement("p");
          notice.className = "tip-reaction-error";
          notice.setAttribute("role", "status");
          card.querySelector(".tip-card-actions")?.append(notice);
        }
        if (notice) notice.textContent = error.message;
      } finally {
        button.disabled = false;
      }
    });
  });
});
