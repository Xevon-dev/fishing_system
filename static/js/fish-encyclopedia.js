var fishFilters = document.querySelectorAll('[data-fish-filter]');
var fishCards = document.querySelectorAll('.fish-card[data-fish-categories]');
var fishSearch = document.querySelector('#fish-search');
var noFishResults = document.querySelector('.fish-encyclopedia__no-results');
var activeFishType = 'all';

function updateFishCards() {
  var query = fishSearch ? fishSearch.value.trim().toLocaleLowerCase('uk') : '';
  var visibleCount = 0;

  fishCards.forEach(function (card) {
    var matchesType = activeFishType === 'all' || card.dataset.fishCategories.split(',').includes(activeFishType);
    var matchesName = !query || card.dataset.fishName.includes(query);
    var visible = matchesType && matchesName;
    card.hidden = !visible;
    if (visible) {
      card.classList.toggle('fish-card--image-right', visibleCount % 2 === 0);
      card.classList.toggle('fish-card--image-left', visibleCount % 2 !== 0);
      visibleCount += 1;
    }
  });

  if (noFishResults) noFishResults.hidden = visibleCount !== 0;
}

fishFilters.forEach(function (filter) {
  filter.addEventListener('click', function () {
    activeFishType = filter.dataset.fishFilter;
    fishFilters.forEach(function (item) {
      item.classList.toggle('is-active', item === filter);
    });
    updateFishCards();
  });
});

if (fishSearch) fishSearch.addEventListener('input', updateFishCards);
