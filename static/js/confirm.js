document.addEventListener("DOMContentLoaded", () => {
  const dialog = document.querySelector("#site-confirm");
  if (!dialog) return;

  const message = dialog.querySelector(".site-confirm__message");
  const accept = dialog.querySelector(".site-confirm__accept");
  const cancel = dialog.querySelector(".site-confirm__cancel");
  let resolveConfirmation;

  const ask = (text) => {
    message.textContent = text || "Підтверди, будь ласка, цю дію.";
    dialog.showModal();
    return new Promise((resolve) => { resolveConfirmation = resolve; });
  };

  const finish = (result) => {
    if (dialog.open) dialog.close();
    resolveConfirmation?.(result);
    resolveConfirmation = null;
  };

  accept.addEventListener("click", () => finish(true));
  cancel.addEventListener("click", () => finish(false));
  dialog.addEventListener("cancel", (event) => {
    event.preventDefault();
    finish(false);
  });
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) finish(false);
  });

  const confirmedForms = new WeakSet();
  document.addEventListener("submit", async (event) => {
    const form = event.target.closest?.("form");
    const confirmationText = event.submitter?.dataset.confirm || form?.dataset.confirm;
    if (!form || !confirmationText || confirmedForms.has(form)) return;
    event.preventDefault();
    const okay = await ask(confirmationText);
    if (!okay) return;
    confirmedForms.add(form);
    if (event.submitter?.name) form.requestSubmit(event.submitter);
    else form.requestSubmit();
  }, true);

  document.addEventListener("click", async (event) => {
    const link = event.target.closest?.("a[data-confirm]");
    if (!link) return;
    event.preventDefault();
    if (await ask(link.dataset.confirm)) window.location.assign(link.href);
  }, true);

  window.fishwiseConfirm = ask;
});
