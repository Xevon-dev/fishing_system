document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#trip-form");
  const summary = document.querySelector("#trip-validation-summary");
  if (!form || !summary) return;

  const waterId = form.querySelector("#trip-water-id");
  const waterError = form.querySelector("#trip-water-error");
  const region = form.querySelector("#trip-region");
  const type = form.querySelector("#trip-type");

  form.addEventListener("submit", (event) => {
    const errors = [];
    let firstInvalid = null;

    summary.hidden = true;
    summary.textContent = "";
    if (waterError) waterError.hidden = true;

    if (!waterId?.value) {
      const message = "Обери водойму на карті перед збереженням.";
      errors.push(message);
      if (waterError) {
        waterError.textContent = message;
        waterError.hidden = false;
      }
      firstInvalid = form.querySelector("#trip-layer-btn") || region;
    }

    if (!type?.value) {
      errors.push("Обери тип риболовлі.");
      firstInvalid ||= type;
    }

    form.querySelectorAll(".catch-editor").forEach((row, index) => {
      if (row.querySelector('input[name$="-DELETE"]')?.value === "on") return;

      const fish = row.querySelector('select[name$="-fish"]');
      const weight = row.querySelector('input[name$="-weight_kg"]');
      const quantity = row.querySelector('input[name$="-quantity"]');
      const caughtAt = row.querySelector('input[name$="-caught_at"]');
      const hasAnyValue = [fish, weight, quantity, caughtAt].some((field) => field?.value);
      if (!hasAnyValue) return;

      if (!fish?.value) {
        errors.push(`Улов ${index + 1}: обери вид риби.`);
        firstInvalid ||= fish;
      }
      if (!quantity?.value || !Number.isInteger(Number(quantity.value)) || Number(quantity.value) < 1) {
        errors.push(`Улов ${index + 1}: кількість має бути цілим числом від 1.`);
        firstInvalid ||= quantity;
      }
      if (!caughtAt?.value) {
        errors.push(`Улов ${index + 1}: вкажи дату й час, коли зловив рибу.`);
        firstInvalid ||= caughtAt;
      } else if (Number.isNaN(new Date(caughtAt.value).getTime())) {
        errors.push(`Улов ${index + 1}: перевір дату й час улову.`);
        firstInvalid ||= caughtAt;
      }
      if (weight?.value && (!Number.isFinite(Number(weight.value)) || Number(weight.value) <= 0)) {
        errors.push(`Улов ${index + 1}: вага має бути більшою за 0 кг.`);
        firstInvalid ||= weight;
      }
    });

    if (errors.length) {
      event.preventDefault();
      summary.textContent = errors.join(" ");
      summary.hidden = false;
      summary.scrollIntoView({ behavior: "smooth", block: "center" });
      firstInvalid?.focus({ preventScroll: true });
    }
  });

});
