const SELECTED_WATER_STYLE = {
  fillColor: "#16a34a",
  fillOpacity: 0.65,
  strokeColor: "#15803d",
  strokeWeight: 2,
};

function initJournalMap() {
  const mapElement = document.querySelector("#trip-map");
  const map = createWaterMap(mapElement);

  const region = document.querySelector("#trip-region");
  const button = document.querySelector("#trip-layer-btn");
  const status = document.querySelector("#trip-layer-status");
  const input = document.querySelector("#trip-water-id");
  const label = document.querySelector("#trip-water-name");
  const focusButton = document.querySelector("#trip-show-on-map");

  const savedWaterUrl = mapElement.dataset.waterUrl || "";
  const savedWaterId = mapElement.dataset.waterId || "";

  let pickedFeature = null;


  function showFeature(feature) {
    map.fitBounds(featureBounds(feature));
    map.data.revertStyle();
    map.data.overrideStyle(feature, SELECTED_WATER_STYLE);
    pickedFeature = feature;
  }

  async function showSavedWater() {
    if (!savedWaterUrl) {
      return;
    }

    try {
      const response = await fetch(savedWaterUrl);
      if (!response.ok) {
        return;
      }

      const geojson = await response.json();
      if (!geojson.features.length) {
        return;
      }

      map.data.forEach((feature) => map.data.remove(feature));
      map.data.addGeoJson(geojson);
      map.fitBounds(boundsOf(geojson));

      map.data.forEach((feature) => {
        if (String(feature.getProperty("water_body_id")) === savedWaterId) {
          map.data.overrideStyle(feature, SELECTED_WATER_STYLE);
          pickedFeature = feature;
        }
      });
    } catch (error) {
      status.textContent = "Не вдалося показати збережену водойму.";
    }
  }

  const startLat = parseFloat(mapElement.dataset.lat);
  const startLon = parseFloat(mapElement.dataset.lon);

  if (!Number.isNaN(startLat) && !Number.isNaN(startLon)) {
    map.setCenter({ lat: startLat, lng: startLon });
    map.setZoom(11);
  }

  map.data.addListener("click", (event) => {
    const feature = event.feature;

    showFeature(feature);

    const id = feature.getProperty("water_body_id") || "";
    const name = feature.getProperty("name") || "Без назви";
    const type = feature.getProperty("type") || "";
    const area = feature.getProperty("area_km2");

    input.value = id;
    label.textContent =
      "Обрано: " +
      name +
      (type ? " · " + type : "") +
      (area ? " · " + area + " км²" : "");
    label.classList.add("is-set");

    if (focusButton && id) {
      focusButton.hidden = false;
    }
  });

  if (focusButton) {
    focusButton.addEventListener("click", () => {
      if (pickedFeature) {
        showFeature(pickedFeature);
      } else {
        showSavedWater();
      }
    });
  }

  button.addEventListener("click", async () => {
    const geojson = await loadRegionLayer(map, region, button, status);

    if (geojson) {
      status.textContent += " Клікни по воді, щоб обрати.";
    }
  });

  if (savedWaterUrl) {
    showSavedWater();
  }
}
