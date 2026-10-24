function initProfileEdit() {
  const dialog = document.querySelector("#profile-edit");

  if (!dialog) {
    return;
  }

  const open = () => {
    if (!dialog.open) {
      dialog.showModal();
    }

    const first = dialog.querySelector("input[name='username']");

    if (first) {
      first.focus();
    }
  };

  for (const trigger of document.querySelectorAll("[data-profile-edit]")) {
    trigger.addEventListener("click", open);
  }

  for (const closer of dialog.querySelectorAll("[data-profile-close]")) {
    closer.addEventListener("click", () => dialog.close());
  }

  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      dialog.close();
    }
  });

  if (dialog.dataset.open) {
    open();
  }
}

initProfileEdit();
