document.addEventListener("DOMContentLoaded", () => {
  if (typeof window.flatpickr !== "function") return;

  const options = {
    enableTime: true,
    time_24hr: true,
    minuteIncrement: 1,
    dateFormat: "Y-m-d\\TH:i",
    altInput: true,
    altFormat: "d.m.Y H:i",
    altInputPlaceholder: "ДД.ММ.РРРР --:--",
    altInputClass: "catch-datetime-display",
    locale: window.flatpickr.l10ns?.uk || "default",
    maxDate: new Date(),
    onOpen: (_selectedDates, _dateString, instance) => {
      instance.set("maxDate", new Date());
    },
    disableMobile: true,
    allowInput: true,
  };

  const initializePickers = (root) => {
    if (root.matches?.('input[type="datetime-local"]') && !root._flatpickr) {
      window.flatpickr(root, options);
    }
    root.querySelectorAll?.('input[type="datetime-local"]').forEach((input) => {
      if (!input._flatpickr) window.flatpickr(input, options);
    });
  };

  initializePickers(document);

  const rows = document.querySelector("#catch-rows");
  if (rows) {
    new MutationObserver((changes) => {
      changes.forEach((change) => {
        change.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) initializePickers(node);
        });
      });
    }).observe(rows, { childList: true, subtree: true });
  }
});
