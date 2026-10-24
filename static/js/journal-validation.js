document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#trip-form");
  if (!form) return;

  const waterId = form.querySelector("#trip-water-id");
  const waterError = form.querySelector("#trip-water-error");
  const region = form.querySelector("#trip-region");
  const type = form.querySelector("#trip-type");

  const showError = (field, message) => {
    if (!field) return;
    field.classList.add("input-error");
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
  };

  form.addEventListener("submit", (event) => {
    form.querySelectorAll("[data-client-error]").forEach((error) => error.remove());
    form.querySelectorAll(".input-error").forEach((field) => field.classList.remove("input-error"));
    if (waterError) {
      waterError.hidden = true;
      waterError.textContent = "";
    }

    let firstInvalid = null;
    let invalid = false;
    const invalidate = (field, message) => {
      showError(field, message);
      firstInvalid ||= field;
      invalid = true;
    };

    if (!waterId?.value) {
      if (waterError) {
        waterError.textContent = "Обери водойму на карті перед збереженням.";
        waterError.hidden = false;
      }
      firstInvalid = form.querySelector("#trip-layer-btn") || region;
      invalid = true;
    }

    if (!type?.value) invalidate(type, "Обери тип риболовлі.");

    const technique = form.querySelector("#trip-method-note");
    const note = form.querySelector("#trip-note");
    const photo = form.querySelector("#trip-photo");
    const photoError = form.querySelector("#trip-photo-error");
    if (technique?.value.length > 255) invalidate(technique, "Максимум 255 символів.");
    if (note?.value.length > 3000) invalidate(note, "Нотатка має містити не більше 3 000 символів.");
    if (photoError) {
      photoError.hidden = true;
      photoError.textContent = "";
    }
    if (photo?.files?.[0]) {
      const file = photo.files[0];
      if (file.type && !file.type.startsWith("image/")) {
        photoError.textContent = "Вибери файл зображення.";
        photoError.hidden = false;
        firstInvalid ||= photo;
        invalid = true;
      }
    }

    form.querySelectorAll(".catch-editor").forEach((row) => {
      if (row.querySelector('input[name$="-DELETE"]')?.value === "on") return;

      const fish = row.querySelector('input[name$="-fish_name"]');
      const customTackle = row.querySelector('input[name$="-custom_tackle"]');
      const weight = row.querySelector('input[name$="-weight_kg"]');
      const quantity = row.querySelector('input[name$="-quantity"]');
      const caughtAt = row.querySelector('input[name$="-caught_at"]');
      const bait = row.querySelector('[name$="-bait_note"]');
      const fields = [fish, customTackle, weight, quantity, caughtAt, bait];
      if (!fields.some((field) => field?.value?.trim())) return;

      if (!fish?.value.trim()) invalidate(fish, "Введи або обери вид риби.");
      else if (fish.value.trim().length > 100 || !/[\p{L}]/u.test(fish.value) || /[^\p{L}\p{N}\s'’().-]/u.test(fish.value)) {
        invalidate(fish, "Вкажи коректну назву риби (до 100 символів).");
      }
      if (customTackle?.value.trim() && !/[\p{L}]/u.test(customTackle.value)) {
        invalidate(customTackle, "Вкажи назву оснастки текстом.");
      }
      if (!quantity?.value || !Number.isInteger(Number(quantity.value)) || Number(quantity.value) < 1) {
        invalidate(quantity, "Вкажи цілу кількість від 1.");
      } else if (Number(quantity.value) > 10000) {
        invalidate(quantity, "Максимум 10 000 риб в одному записі.");
      }
      if (!caughtAt?.value) {
        invalidate(caughtAt, "Вкажи дату й час улову.");
      } else if (Number.isNaN(new Date(caughtAt.value).getTime())) {
        invalidate(caughtAt, "Перевір дату й час улову.");
      }
      if (weight?.value && (!Number.isFinite(Number(weight.value)) || Number(weight.value) <= 0)) {
        invalidate(weight, "Вага має бути більшою за 0 кг.");
      } else if (weight?.value && Number(weight.value) > 500) {
        invalidate(weight, "Вага однієї риби не може перевищувати 500 кг.");
      }
      if (bait?.value.length > 500) invalidate(bait, "Максимум 500 символів.");
    });

    if (invalid) {
      event.preventDefault();
      firstInvalid?.scrollIntoView({ behavior: "smooth", block: "center" });
      firstInvalid?.focus({ preventScroll: true });
    }
  });
});
