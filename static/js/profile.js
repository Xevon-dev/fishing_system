function initProfileDialog(dialog, triggerSelector) {
  if (!dialog) return;
  const open = () => {
    if (!dialog.open) {
      dialog.showModal();
    }

    const first = dialog.querySelector(".input-error") || dialog.querySelector("input:not([type='hidden'])");

    if (first) {
      first.focus();
    }
  };

  for (const trigger of document.querySelectorAll(triggerSelector)) {
    trigger.addEventListener("click", open);
  }

  const cancelAndReset = () => {
    if (dialog.dataset.open) {
      window.location.replace(dialog.dataset.cancelUrl);
      return;
    }

    dialog.querySelector("form")?.reset();
    dialog.querySelectorAll("[data-password-toggle]").forEach((button) => {
      button.classList.remove("is-on");
      button.setAttribute("aria-label", "Показати пароль");
      const input = document.getElementById(button.dataset.passwordToggle);
      if (input) input.type = "password";
    });
    dialog.close();
  };

  for (const closer of dialog.querySelectorAll("[data-profile-close]")) {
    closer.addEventListener("click", cancelAndReset);
  }

  dialog.addEventListener("cancel", (event) => {
    event.preventDefault();
    cancelAndReset();
  });

  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      cancelAndReset();
    }
  });

  if (dialog.dataset.open) {
    open();
  }
}

initProfileDialog(document.querySelector("#profile-edit"), "[data-profile-edit]");
const passwordDialog = document.querySelector("#profile-password");
initProfileDialog(passwordDialog, "[data-profile-password]");

const profilePhotoInput = document.querySelector("#profile-photo-input");
const profilePhotoFilename = document.querySelector("#profile-photo-filename");
profilePhotoInput?.addEventListener("change", () => {
  if (profilePhotoFilename) {
    profilePhotoFilename.textContent = profilePhotoInput.files?.[0]?.name || "Файл не вибрано";
  }
});
