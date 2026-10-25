function initRegionPicker({ pickerId, selectId, inputId, toggleId, listId }) {
  const picker = document.querySelector(pickerId);

  if (!picker) {
    return;
  }

  const select = picker.querySelector(selectId);
  const input = picker.querySelector(inputId);
  const toggle = picker.querySelector(toggleId);
  const list = picker.querySelector(listId);

  let activeIndex = -1;

  function syncInput() {
    const option = select.selectedOptions[0];
    input.value = option && option.value ? option.textContent : "";
  }

  function close() {
    list.hidden = true;
    picker.classList.remove("is-open");
    input.setAttribute("aria-expanded", "false");
    activeIndex = -1;
  }

  function render(query) {
    const needle = query.trim().toLowerCase();

    activeIndex = -1;
    list.replaceChildren();

    for (const option of select.options) {
      if (needle && !option.textContent.toLowerCase().includes(needle)) {
        continue;
      }

      const item = document.createElement("li");
      item.className = "map-select__option";
      item.setAttribute("role", "option");
      item.dataset.value = option.value;
      item.textContent = option.textContent;
      item.classList.toggle("is-selected", option.value === select.value);
      list.append(item);
    }

    if (!list.children.length) {
      const empty = document.createElement("li");
      empty.className = "map-select__empty";
      empty.textContent = "Нічого не знайдено";
      list.append(empty);
    }

    list.hidden = false;
    picker.classList.add("is-open");
    input.setAttribute("aria-expanded", "true");
  }

  function choose(value) {
    const option = [...select.options].find((item) => item.value === value);

    if (!option) {
      return;
    }

    select.value = value;
    input.value = value ? option.textContent : "";
    select.dispatchEvent(new Event("change"));
    close();
  }

  function moveActive(step) {
    const items = [...list.querySelectorAll(".map-select__option")];

    if (!items.length) {
      return;
    }

    activeIndex = (activeIndex + step + items.length) % items.length;

    items.forEach((item, index) => {
      item.classList.toggle("is-active", index === activeIndex);
    });

    items[activeIndex].scrollIntoView({ block: "nearest" });
  }

  input.addEventListener("focus", () => {
    if (list.hidden) {
      render("");
    }
  });

  input.addEventListener("click", () => {
    if (list.hidden) {
      render("");
    }
  });

  input.addEventListener("input", () => {
    select.value = "";
    render(input.value);
  });

  input.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown") {
      event.preventDefault();

      if (list.hidden) {
        render(input.value);
      } else {
        moveActive(1);
      }
    } else if (event.key === "ArrowUp") {
      event.preventDefault();

      if (!list.hidden) {
        moveActive(-1);
      }
    } else if (event.key === "Enter") {
      const items = [...list.querySelectorAll(".map-select__option")];
      const target = items[activeIndex] || (items.length === 1 ? items[0] : null);

      if (!list.hidden && target) {
        event.preventDefault();
        choose(target.dataset.value);
      }
    } else if (event.key === "Escape") {
      close();
    }
  });

  toggle.addEventListener("click", () => {
    if (list.hidden) {
      input.focus();
    } else {
      close();
    }
  });

  list.addEventListener("mousedown", (event) => {
    event.preventDefault();
  });

  list.addEventListener("click", (event) => {
    const item = event.target.closest(".map-select__option");

    if (item) {
      choose(item.dataset.value);
    }
  });

  document.addEventListener("click", (event) => {
    if (!picker.contains(event.target)) {
      close();
    }
  });

  select.addEventListener("change", syncInput);
  select.addEventListener("change", () => {
    input.dispatchEvent(new Event("change", { bubbles: true }));
  });

  syncInput();
}

initRegionPicker({
  pickerId: "#region-picker",
  selectId: "#water-region",
  inputId: "#region-input",
  toggleId: "#region-toggle",
  listId: "#region-list",
});
initRegionPicker({
  pickerId: "#trip-region-picker",
  selectId: "#trip-region",
  inputId: "#trip-region-input",
  toggleId: "#trip-region-toggle",
  listId: "#trip-region-list",
});
initRegionPicker({
  pickerId: "#trip-type-picker",
  selectId: "#trip-type",
  inputId: "#trip-type-input",
  toggleId: "#trip-type-toggle",
  listId: "#trip-type-list",
});
initRegionPicker({
  pickerId: "#tips-sort-picker",
  selectId: "#tips-sort-select",
  inputId: "#tips-sort-input",
  toggleId: "#tips-sort-toggle",
  listId: "#tips-sort-list",
});
