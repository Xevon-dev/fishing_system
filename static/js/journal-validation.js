document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#trip-form");
  if (!form) return;

  const waterId = form.querySelector("#trip-water-id");
  const waterError = form.querySelector("#trip-water-error");
  const waterSection = form.querySelector(".trip-water-section");
  const regionPicker = form.querySelector("#trip-region-picker");
  const regionInput = form.querySelector("#trip-region-input");
  const type = form.querySelector("#trip-type");
  const typePicker = form.querySelector("#trip-type-picker");
  const typeInput = form.querySelector("#trip-type-input");

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

  const clearWaterError = () => {
    if (waterId?.value) {
      waterSection?.classList.remove("has-error");
      regionPicker?.classList.remove("has-error");
      regionInput?.classList.remove("input-error");
      regionInput?.removeAttribute("aria-invalid");
      if (waterError) {
        waterError.hidden = true;
        waterError.textContent = "";
      }
    }
  };
  waterId?.addEventListener("change", clearWaterError);
  typeInput?.addEventListener("change", () => {
    if (!type?.value) return;
    typePicker?.classList.remove("has-error");
    typeInput.classList.remove("input-error");
    typeInput.removeAttribute("aria-invalid");
    typePicker?.querySelectorAll("[data-client-error]").forEach((error) => error.remove());
  });

  const setDateTimeLimits = () => {
    const maxLocalDateTime = new Date(Date.now() - new Date().getTimezoneOffset() * 60_000)
      .toISOString()
      .slice(0, 16);
    form.querySelectorAll('input[type="datetime-local"]').forEach((input) => {
      input.max = maxLocalDateTime;
    });
  };
  setDateTimeLimits();
  form.addEventListener("focusin", (event) => {
    if (event.target.matches('input[type="datetime-local"]')) setDateTimeLimits();
  });

  form.addEventListener("submit", (event) => {
    form.querySelectorAll("[data-client-error]").forEach((error) => error.remove());
    form.querySelectorAll(".input-error").forEach((field) => field.classList.remove("input-error"));
    clearWaterError();
    setDateTimeLimits();

    let firstInvalid = null;
    let invalid = false;
    const invalidate = (field, message) => {
      showError(field, message);
      firstInvalid ||= field;
      invalid = true;
    };

    if (!waterId?.value) {
      waterSection?.classList.add("has-error");
      regionPicker?.classList.add("has-error");
      regionInput?.classList.add("input-error");
      regionInput?.setAttribute("aria-invalid", "true");
      if (waterError) {
        waterError.textContent = "Оберіть водойму на карті.";
        waterError.hidden = false;
      }
      firstInvalid = regionInput || form.querySelector("#trip-layer-btn");
      invalid = true;
    }

    if (!type?.value) {
      typePicker?.classList.add("has-error");
      typeInput?.setAttribute("aria-invalid", "true");
      invalidate(typeInput, "Оберіть тип риболовлі зі списку.");
    }

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
    for (const file of Array.from(photo?.files || [])) {
      if (file.type && !file.type.startsWith("image/")) {
        photoError.textContent = "Вибери файли зображень.";
        photoError.hidden = false;
        firstInvalid ||= photo;
        invalid = true;
        break;
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
      } else if (new Date(caughtAt.value).getTime() > Date.now()) {
        invalidate(caughtAt, "Не можна вказати час улову з майбутнього.");
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
