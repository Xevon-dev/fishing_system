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

document.querySelectorAll('.method-card__video').forEach(function (preview) {
  var cover = preview.querySelector('img');
  var videoId = preview.dataset.video;

  cover.addEventListener('error', function () {
    cover.src = 'https://i.ytimg.com/vi/' + videoId + '/hqdefault.jpg';
  });

  preview.addEventListener('click', function () {
    preview.classList.add('is-playing');
    preview.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + videoId +
      '?autoplay=1" referrerpolicy="origin" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe>';
  });
});
