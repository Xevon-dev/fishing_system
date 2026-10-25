document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".tip-compose-form");
  if (!form) return;

  const title = form.querySelector("#tip-title");
  const content = form.querySelector("#tip-content");
  const count = form.querySelector("#tip-content-count");
  const photo = form.querySelector("#tip-photo");
  const drop = form.querySelector(".tip-photo-drop");
  const preview = form.querySelector("#tip-photo-preview");
  const filename = form.querySelector("#tip-photo-filename");
  const selectedPhoto = form.querySelector("#tip-selected-photo");
  const clearPhoto = form.querySelector("#tip-photo-clear");
  const photoError = form.querySelector("#tip-photo-error");
  const button = form.querySelector(".tip-publish-button");
  const fishPicker = form.querySelector(".tip-fish-picker");
  const fishInputs = Array.from(form.querySelectorAll('input[name="fishes"]'));
  const fishCount = form.querySelector("#tip-fish-count");
  const allFishInput = form.querySelector("#tip-applies-all-fish");
  const allFishButton = form.querySelector("#tip-select-all-fish");

  const updateFishCount = () => {
    const selectedCount = fishInputs.filter((input) => input.checked).length;
    if (fishCount) fishCount.textContent = String(selectedCount);
    form.querySelectorAll(".tip-fish-field [data-client-error]").forEach((error) => error.remove());
    fishInputs.forEach((input) => input.classList.remove("input-error"));
  };
  const syncAllFishButton = () => {
    allFishButton?.setAttribute("aria-pressed", allFishInput?.value === "1" ? "true" : "false");
  };
  fishInputs.forEach((input) => input.addEventListener("change", () => {
    if (allFishInput) allFishInput.value = "0";
    syncAllFishButton();
    updateFishCount();
  }));
  allFishButton?.addEventListener("click", () => {
    const selectAll = allFishInput?.value !== "1";
    if (allFishInput) allFishInput.value = selectAll ? "1" : "0";
    fishInputs.forEach((input) => { input.checked = selectAll; });
    syncAllFishButton();
    updateFishCount();
  });
  syncAllFishButton();

  const inlineError = (field, message) => {
    const group = field.closest(".form-group");
    if (!group) return;
    let error = group.querySelector("[data-client-error]");
    if (!error) {
      error = document.createElement("span");
      error.className = "field-error";
      error.dataset.clientError = "true";
      error.setAttribute("role", "alert");
      group.append(error);
    }
    error.textContent = message;
    field.classList.add("input-error");
  };

  content?.addEventListener("input", () => {
    if (count) count.textContent = String(content.value.length);
  });

  form.querySelectorAll("[data-insert]").forEach((tool) => {
    tool.addEventListener("click", () => {
      if (!content) return;
      const prefix = tool.dataset.insert === "number" ? "1. " : "• ";
      const start = content.selectionStart;
      const lineStart = content.value.lastIndexOf("\n", Math.max(0, start - 1)) + 1;
      content.setRangeText(prefix, lineStart, lineStart, "end");
      content.focus();
      content.dispatchEvent(new Event("input", { bubbles: true }));
    });
  });

  let previewUrl = null;
  const updatePhoto = (file) => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    previewUrl = null;
    if (photoError) {
      photoError.hidden = true;
      photoError.textContent = "";
    }
    if (filename) filename.textContent = file ? file.name : "";
    if (preview && file?.type.startsWith("image/")) {
      previewUrl = URL.createObjectURL(file);
      preview.src = previewUrl;
      preview.hidden = false;
    } else if (preview) {
      preview.hidden = true;
      preview.removeAttribute("src");
    }
    if (selectedPhoto) selectedPhoto.hidden = !file;
  };

  photo?.addEventListener("change", () => updatePhoto(photo.files[0]));
  clearPhoto?.addEventListener("click", () => {
    if (photo) photo.value = "";
    updatePhoto(null);
  });
  if (drop && photo) {
    ["dragenter", "dragover"].forEach((name) => drop.addEventListener(name, (event) => {
      event.preventDefault();
      drop.classList.add("is-dragging");
    }));
    ["dragleave", "drop"].forEach((name) => drop.addEventListener(name, (event) => {
      event.preventDefault();
      drop.classList.remove("is-dragging");
    }));
    drop.addEventListener("drop", (event) => {
      if (!event.dataTransfer.files.length) return;
      const transfer = new DataTransfer();
      transfer.items.add(event.dataTransfer.files[0]);
      photo.files = transfer.files;
      photo.dispatchEvent(new Event("change", { bubbles: true }));
    });
  }

  form.addEventListener("submit", (event) => {
    form.querySelectorAll("[data-client-error]").forEach((error) => error.remove());
    form.querySelectorAll(".input-error").forEach((field) => field.classList.remove("input-error"));
    if (photoError) {
      photoError.hidden = true;
      photoError.textContent = "";
    }

    let invalid = false;
    let firstInvalid = null;
    const fail = (field, message) => {
      inlineError(field, message);
      firstInvalid ||= field;
      invalid = true;
    };

    const titleValue = title?.value.trim() || "";
    const contentValue = content?.value.trim() || "";
    const selectedFish = fishInputs.filter((input) => input.checked);
    if (titleValue.length < 10) fail(title, "Назва має містити щонайменше 10 символів.");
    else if (titleValue.length > 200) fail(title, "Максимум 200 символів.");
    if (contentValue.length < 20) fail(content, "Додай трохи більше деталей — щонайменше 20 символів.");
    else if (contentValue.length > 2000) fail(content, "Максимум 2 000 символів.");
    if (selectedFish.length < 1) {
      const firstFish = selectedFish[0] || fishInputs[0];
      if (firstFish) fail(firstFish, "Виберіть хоча б одну рибу зі списку.");
      else invalid = true;
    }

    const file = photo?.files?.[0];
    if (file && file.type && !file.type.startsWith("image/")) {
      if (photoError) {
        photoError.textContent = "Вибери файл зображення.";
        photoError.hidden = false;
      }
      firstInvalid ||= photo;
      invalid = true;
    }

    if (invalid) {
      event.preventDefault();
      firstInvalid?.scrollIntoView({ behavior: "smooth", block: "center" });
      firstInvalid?.focus({ preventScroll: true });
      return;
    }

    if (button) {
      button.disabled = true;
      button.querySelector("span")?.remove();
      button.append("Перевіряю пораду…");
    }
  });
});
