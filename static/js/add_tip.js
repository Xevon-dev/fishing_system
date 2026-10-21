/**
 * Форма поради: поки ШІ перевіряє текст, кнопка показує стан очікування.
 */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".auth-form");
  const button = form ? form.querySelector(".auth-submit") : null;

  if (!form || !button) {
    return;
  }

  form.addEventListener("submit", () => {
    button.disabled = true;
    button.textContent = "Перевіряю пораду…";
  });
});
