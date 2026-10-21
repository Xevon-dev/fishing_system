/**
 * Підтвердження дій: форми та посилання з data-confirm.
 */
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(form.dataset.confirm)) {
        event.preventDefault();
      }
    });
  });

  document.querySelectorAll("a[data-confirm]").forEach((link) => {
    link.addEventListener("click", (event) => {
      if (!window.confirm(link.dataset.confirm)) {
        event.preventDefault();
      }
    });
  });
});
