document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector("#add-catch");
  const rows = document.querySelector("#catch-rows");
  const template = document.querySelector("#catch-template");
  const total = document.querySelector("#id_catches-TOTAL_FORMS");
  if (!button || !rows || !template || !total) return;
  const max = Number(document.querySelector("#id_catches-MAX_NUM_FORMS").value);
  button.addEventListener("click", () => {
    const index = Number(total.value);
    if (index >= max) return;
    const wrapper = document.createElement("div");
    wrapper.innerHTML = template.innerHTML.replaceAll("__prefix__", String(index));
    const row = wrapper.firstElementChild;
    rows.append(row);
    total.value = String(index + 1);
    button.disabled = index + 1 >= max;
    row.querySelector('input[name$="-fish_name"]')?.focus();
  });

  rows.addEventListener("click", async (event) => {
    const fishToggle = event.target.closest("[data-fish-toggle]");
    if (fishToggle) {
      const picker = fishToggle.closest("[data-fish-autocomplete]");
      const input = picker?.querySelector('input[name$="-fish_name"]');
      const list = picker?.querySelector(".map-select__list");
      if (input && list) {
        input.focus();
        renderFishOptions(picker, input.value);
      }
      return;
    }

    const fishOption = event.target.closest("[data-fish-option]");
    if (fishOption) {
      const picker = fishOption.closest("[data-fish-autocomplete]");
      const input = picker?.querySelector('input[name$="-fish_name"]');
      if (input) {
        input.value = fishOption.dataset.value;
        input.dispatchEvent(new Event("input", { bubbles: true }));
        input.dispatchEvent(new Event("change", { bubbles: true }));
        closeFishOptions(picker);
      }
      return;
    }

    const removeButton = event.target.closest("[data-catch-remove]");
    if (!removeButton) return;
    if (window.fishwiseConfirm && !(await window.fishwiseConfirm("Прибрати цей улов? Зміна збережеться після збереження сесії."))) return;

    const row = removeButton.closest(".catch-editor");
    const deleteField = row?.querySelector('input[name$="-DELETE"]');
    if (!row || !deleteField) return;
    deleteField.value = "on";
    row.hidden = true;
  });

  function closeFishOptions(picker) {
    const list = picker?.querySelector(".map-select__list");
    const input = picker?.querySelector('input[name$="-fish_name"]');
    if (list) list.hidden = true;
    if (input) input.setAttribute("aria-expanded", "false");
    picker?.classList.remove("is-open");
  }

  function renderFishOptions(picker, query) {
    const list = picker?.querySelector(".map-select__list");
    const input = picker?.querySelector('input[name$="-fish_name"]');
    if (!list || !input) return;
    const needle = query.trim().toLocaleLowerCase("uk");
    const options = [...list.querySelectorAll("[data-fish-option]")];
    let visibleCount = 0;
    options.forEach((option) => {
      const alwaysVisible = option.classList.contains("map-select__option--none");
      const visible = alwaysVisible || !needle || option.textContent.trim().toLocaleLowerCase("uk").includes(needle);
      option.hidden = !visible;
      option.classList.remove("is-active");
      visibleCount += Number(visible);
    });
    list.querySelector(".map-select__empty")?.remove();
    if (!visibleCount) {
      const empty = document.createElement("li");
      empty.className = "map-select__empty";
      empty.textContent = "Немає збігів — можна залишити власну назву риби";
      list.append(empty);
    }
    list.hidden = false;
    picker.classList.add("is-open");
    input.setAttribute("aria-expanded", "true");
  }

  rows.addEventListener("focusin", (event) => {
    const input = event.target.closest('input[name$="-fish_name"]');
    if (input) renderFishOptions(input.closest("[data-fish-autocomplete]"), input.value);
  });

  rows.addEventListener("input", (event) => {
    const input = event.target.closest('input[name$="-fish_name"]');
    if (input) renderFishOptions(input.closest("[data-fish-autocomplete]"), input.value);
  });

  rows.addEventListener("keydown", (event) => {
    const input = event.target.closest('input[name$="-fish_name"]');
    if (!input) return;
    const picker = input.closest("[data-fish-autocomplete]");
    const list = picker?.querySelector(".map-select__list");
    const visible = [...(list?.querySelectorAll("[data-fish-option]:not([hidden])") || [])];
    if (event.key === "Escape") {
      closeFishOptions(picker);
    } else if (event.key === "ArrowDown" && visible.length) {
      event.preventDefault();
      const current = visible.findIndex((option) => option.classList.contains("is-active"));
      visible.forEach((option) => option.classList.remove("is-active"));
      visible[(current + 1) % visible.length].classList.add("is-active");
    } else if (event.key === "ArrowUp" && visible.length) {
      event.preventDefault();
      const current = visible.findIndex((option) => option.classList.contains("is-active"));
      visible.forEach((option) => option.classList.remove("is-active"));
      visible[(current <= 0 ? visible.length : current) - 1].classList.add("is-active");
    } else if (event.key === "Enter" && !list?.hidden) {
      const active = list.querySelector("[data-fish-option].is-active") || (visible.length === 1 ? visible[0] : null);
      if (active) {
        event.preventDefault();
        input.value = active.dataset.value;
        input.dispatchEvent(new Event("input", { bubbles: true }));
        input.dispatchEvent(new Event("change", { bubbles: true }));
        closeFishOptions(picker);
      }
    }
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest("[data-fish-autocomplete]")) {
      rows.querySelectorAll("[data-fish-autocomplete]").forEach(closeFishOptions);
    }
  });
});
