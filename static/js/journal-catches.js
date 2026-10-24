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
    row.querySelector('input[list="fish-options"]')?.focus();
  });

  rows.addEventListener("click", (event) => {
    const removeButton = event.target.closest("[data-catch-remove]");
    if (!removeButton) return;
    if (!window.confirm("Прибрати цей улов? Зміна збережеться після збереження сесії.")) return;

    const row = removeButton.closest(".catch-editor");
    const deleteField = row?.querySelector('input[name$="-DELETE"]');
    if (!row || !deleteField) return;
    deleteField.value = "on";
    row.hidden = true;
  });
});
