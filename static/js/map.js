function initMap() {
  const map = createWaterMap(document.querySelector("#map"));

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
    const geojson = await loadRegionLayer(map, region, button, status);

    if (geojson) {
      history.replaceState(null, "", "/map/?region=" + region.value);
    }
  });
}
