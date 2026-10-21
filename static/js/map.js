/**
 * Карта водойм: ініціалізація, вибір області, кліки по карті.
 * Картки винесені окремо: map-water.js, map-weather.js, map-advice.js
 */
function initMap() {
  const map = new google.maps.Map(document.querySelector("#map"), {
    center: { lat: 48.3794, lng: 31.1656 }, // центр України
    zoom: 6,
    mapId: "DEMO_MAP_ID",
  });

  const region = document.querySelector("#water-region");
  const button = document.querySelector("#water-layer-btn");
  const status = document.querySelector("#water-layer-status");
  const info = document.querySelector("#water-info");
  const weatherBox = document.querySelector("#weather-info");
  const adviceBox = document.querySelector("#advice-info");

  const fromUrl = new URLSearchParams(location.search).get("region");
  if (fromUrl && region.querySelector(`option[value="${fromUrl}"]`)) {
    region.value = fromUrl;
  }

  let waterClickTime = 0;
  let lastWater = null;

  map.data.setStyle({
    fillColor: "#3b82f6",
    fillOpacity: 0.45,
    strokeColor: "#1d4ed8",
    strokeWeight: 1,
  });

  map.data.addListener("click", (event) => {
    waterClickTime = Date.now();
    const feature = event.feature;

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

    loadWeather(weatherBox, event.latLng);
    loadAdvice(adviceBox, event.latLng, lastWater);
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
    loadAdvice(adviceBox, event.latLng, lastWater);
  });

  button.addEventListener("click", async () => {
    const name = region.selectedOptions[0].textContent;
    const url = button.dataset.geojsonUrl.replace("__REGION__", region.value);

    history.replaceState(null, "", "/map/?region=" + region.value);

    button.disabled = true;
    status.textContent = "Завантажую водойми…";

    try {
      const response = await fetch(url);

      if (!response.ok) {
        status.textContent = "Дані для «" + name + "» ще не зібрані.";
        return;
      }

      const geojson = await response.json();

      map.data.forEach((feature) => map.data.remove(feature));
      map.data.addGeoJson(geojson);
      map.fitBounds(boundsOf(geojson));

      status.textContent =
        "Водойм на карті: " + geojson.features.length + " (" + name + ")";
    } catch (error) {
      status.textContent = "Не вдалося завантажити водойми.";
    } finally {
      button.disabled = false;
    }
  });
}
