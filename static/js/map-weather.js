function setWeatherTabsVisible(visible) {
  const tabs = document.querySelector("#weather-tabs");

  if (tabs) {
    tabs.hidden = !visible;
  }
}

function selectWeatherDay(key) {
  const tabs = document.querySelector("#weather-tabs");
  const box = document.querySelector("#weather-info");

  if (!tabs || !box) {
    return;
  }

  const all = key === "all";

  for (const tab of tabs.querySelectorAll("[data-weather-tab]")) {
    tab.classList.toggle("is-active", tab.dataset.weatherTab === key);
  }

  box.classList.toggle("is-multi", all);

  for (const panel of box.querySelectorAll("[data-weather-panel]")) {
    panel.hidden = !all && panel.dataset.weatherPanel !== key;
  }
}

function initWeatherTabs() {
  const tabs = document.querySelector("#weather-tabs");

  if (!tabs) {
    return;
  }

  tabs.addEventListener("click", (event) => {
    const tab = event.target.closest("[data-weather-tab]");

    if (tab) {
      selectWeatherDay(tab.dataset.weatherTab);
    }
  });
}

async function loadWeather(box, latLng) {
  const url =
    box.dataset.weatherUrl + "?lat=" + latLng.lat() + "&lon=" + latLng.lng();

  setWeatherTabsVisible(false);
  box.textContent = "Дізнаюся погоду…";

  try {
    const response = await fetch(url);

    if (!response.ok) {
      const data = await response.json();
      box.textContent = data.error || "Не вдалося отримати погоду.";
      return;
    }

    box.innerHTML = await response.text();
    setWeatherTabsVisible(true);
    selectWeatherDay("0");
  } catch (error) {
    box.textContent = "Не вдалося отримати погоду.";
  }
}

initWeatherTabs();
