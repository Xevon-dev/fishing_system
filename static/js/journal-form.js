document.addEventListener("DOMContentLoaded", () => {
  const type = document.querySelector("#trip-type");
  const method = document.querySelector("#trip-method");

  if (!type || !method) {
    return;
  }

  const placeholder = method.querySelector('option[value=""]');
  const options = Array.from(method.querySelectorAll("option")).filter(
    (option) => option.value !== "",
  );

  function applyFilter() {
    const hasType = Boolean(type.value);

    options.forEach((option) => {
      const match = hasType && option.dataset.type === type.value;
      option.hidden = !match;
      option.disabled = !match;
    });

    if (placeholder) {
      placeholder.textContent = hasType
        ? "— не вказано —"
        : "— спочатку обери тип —";
    }

    const selected = method.options[method.selectedIndex];
    if (selected && selected.disabled) {
      method.value = "";
    }
  }

  type.addEventListener("change", applyFilter);
  applyFilter();
});
