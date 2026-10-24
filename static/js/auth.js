document.querySelectorAll("[data-password-toggle]").forEach((button) => {
  const input = document.getElementById(button.dataset.passwordToggle);
  if (!input) return;

  button.addEventListener("click", () => {
    const visible = input.type === "password";
    input.type = visible ? "text" : "password";
    button.classList.toggle("is-on", visible);
    button.setAttribute("aria-label", visible ? "Приховати пароль" : "Показати пароль");
  });
});
