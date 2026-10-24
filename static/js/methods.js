function resetMethodVideos() {
  document.querySelectorAll('.method-card__video.is-playing').forEach(function (preview) {
    var videoId = preview.dataset.video;
    var cover = document.createElement('img');
    cover.src = 'https://i.ytimg.com/vi/' + videoId + '/maxresdefault.jpg';
    cover.alt = preview.dataset.videoAlt || '';
    cover.loading = 'lazy';
    cover.addEventListener('error', function () {
      cover.src = 'https://i.ytimg.com/vi/' + videoId + '/hqdefault.jpg';
    }, { once: true });
    preview.classList.remove('is-playing');
    preview.replaceChildren(cover);
  });
}

document.querySelectorAll('.method-card__head').forEach(function (head) {
  head.addEventListener('click', function () {
    resetMethodVideos();
    var card = head.closest('.method-card');
    var wasOpen = card.classList.contains('is-open');
    var sidebar = document.querySelector('.methods-sidebar');

    document.querySelectorAll('.method-card.is-open').forEach(function (open) {
      open.classList.remove('is-open');
      var openBody = sidebar && sidebar.querySelector('.method-card__body');
      if (openBody) {
        open.appendChild(openBody);
      }
    });

    if (!wasOpen) {
      card.classList.add('is-open');
      var body = card.querySelector('.method-card__body');
      if (body && sidebar) {
        sidebar.appendChild(body);
      }
    }

    if (sidebar) sidebar.classList.toggle('has-techniques', !wasOpen);
  });
});

document.querySelectorAll('.method-card__video').forEach(function (preview) {
  var cover = preview.querySelector('img');
  var videoId = preview.dataset.video;
  if (cover) preview.dataset.videoAlt = cover.alt;

  cover.addEventListener('error', function () {
    cover.src = 'https://i.ytimg.com/vi/' + videoId + '/hqdefault.jpg';
  });

  preview.addEventListener('click', function () {
    resetMethodVideos();
    preview.classList.add('is-playing');
    preview.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + videoId +
      '?autoplay=1" referrerpolicy="origin" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe>';
  });
});

document.querySelectorAll('[data-method-filter]').forEach(function (filter) {
  filter.addEventListener('click', function () {
    resetMethodVideos();
    var category = filter.dataset.methodFilter;
    var sidebar = document.querySelector('.methods-sidebar');

    document.querySelectorAll('.method-card.is-open').forEach(function (open) {
      open.classList.remove('is-open');
      var body = sidebar && sidebar.querySelector('.method-card__body');
      if (body) open.appendChild(body);
    });
    if (sidebar) sidebar.classList.remove('has-techniques');

    document.querySelectorAll('[data-method-filter]').forEach(function (item) {
      item.classList.toggle('is-active', item === filter);
    });

    document.querySelectorAll('.method-card[data-method-category]').forEach(function (card) {
      card.hidden = category !== 'all' && card.dataset.methodCategory !== category;
    });
  });
});

var firstMethodFilter = document.querySelector('[data-method-filter]');
if (firstMethodFilter) firstMethodFilter.click();
