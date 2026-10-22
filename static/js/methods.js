/* Картки «Техніки лову»: відкрита одна картка за раз. */

document.querySelectorAll('.method-card__head').forEach(function (head) {
  head.addEventListener('click', function () {
    var card = head.closest('.method-card');
    var wasOpen = card.classList.contains('is-open');

    document.querySelectorAll('.method-card.is-open').forEach(function (open) {
      open.classList.remove('is-open');
    });

    if (!wasOpen) {
      card.classList.add('is-open');
    }
  });
});
