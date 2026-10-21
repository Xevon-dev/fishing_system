/**
 * Карта водойм: ініціалізація, вибір області, кліки по карті.
 * Спільне з формою сесії — у map-core.js,
 * картки — у map-water.js, map-weather.js, map-advice.js
 */
function initMap() {
  const mapElement = document.querySelector("#map");
  const map = createWaterMap(mapElement);

  const region = document.querySelector("#water-region");
  const button = document.querySelector("#water-layer-btn");
  const status = document.querySelector("#water-layer-status");
  const info = document.querySelector("#water-info");
  const weatherBox = document.querySelector("#weather-info");
  const adviceBox = document.querySelector("#advice-info");

  let waterClickTime = 0;
  let lastWater = null;


  function selectWater(feature, position) {
    showWater(info, {
      name: feature.getProperty("name"),
      type: feature.getProperty("type"),
      area_km2: feature.getProperty("area_km2"),
      depth: feature.getProperty("depth"),
      fish: feature.getProperty("fish"),
      description: feature.getProperty("description"),
      wikipedia: feature.getProperty("wikipedia"),
      source: feature.getProperty("source"),
    });

    lastWater = {
      name: feature.getProperty("name") || "",
      type: feature.getProperty("type") || "",
      area: feature.getProperty("area_km2") || "",
      depth: feature.getProperty("depth") || "",
      fish: feature.getProperty("fish") || "",
    };

    loadWeather(weatherBox, position);
    prepareAdvice(adviceBox, position, lastWater);
  }

  function findWater(waterId) {
    let found = null;

    map.data.forEach((feature) => {
      if (String(feature.getProperty("water_body_id")) === String(waterId)) {
        found = feature;
      }
    });

    return found;
  }

  async function focusWater(waterId, regionSlug) {
    if (regionSlug && region.querySelector(`option[value="${regionSlug}"]`)) {
      region.value = regionSlug;
    }

    const geojson = await loadRegionLayer(map, region, button, status);
    if (!geojson) {
      return;
    }

    const feature = findWater(waterId);
    if (!feature) {
      return;
    }

    const bounds = featureBounds(feature);

    map.fitBounds(bounds);
    map.data.overrideStyle(feature, {
      fillColor: "#16a34a",
      fillOpacity: 0.65,
      strokeColor: "#15803d",
      strokeWeight: 2,
    });

    selectWater(feature, bounds.getCenter());
    status.textContent = "Показано водойму: " + feature.getProperty("name");
    history.replaceState(null, "", "/map/?region=" + region.value + "&water=" + waterId);
  }

  const fromUrl = new URLSearchParams(location.search).get("region");
  if (fromUrl && region.querySelector(`option[value="${fromUrl}"]`)) {
    region.value = fromUrl;
  }

  map.data.addListener("click", (event) => {
    waterClickTime = Date.now();
    selectWater(event.feature, event.latLng);
  });

  map.addListener("click", (event) => {
    if (Date.now() - waterClickTime < 300) {
      return;
    }

    info.textContent =
      "Координати кліку: " +
      event.latLng.lat().toFixed(5) +
      ", " +
      event.latLng.lng().toFixed(5);

    lastWater = null;
    loadWeather(weatherBox, event.latLng);
    prepareAdvice(adviceBox, event.latLng, lastWater);
  });

  button.addEventListener("click", async () => {
    const geojson = await loadRegionLayer(map, region, button, status);

    if (geojson) {
      history.replaceState(null, "", "/map/?region=" + region.value);
    }
  });

  if (mapElement.dataset.focusId) {
    focusWater(mapElement.dataset.focusId, mapElement.dataset.focusRegion);
  }
}
