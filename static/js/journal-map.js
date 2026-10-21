/**
 * Міні-карта у формі сесії: вибір водойми кліком по контуру.
 * Спільне зі сторінкою карти — у map-core.js
 */
function initJournalMap() {
  const map = createWaterMap(document.querySelector("#trip-map"));

  const region = document.querySelector("#trip-region");
  const button = document.querySelector("#trip-layer-btn");
  const status = document.querySelector("#trip-layer-status");
  const input = document.querySelector("#trip-water-id");
  const label = document.querySelector("#trip-water-name");

  map.data.addListener("click", (event) => {
    const feature = event.feature;

    map.data.revertStyle();
    map.data.overrideStyle(feature, {
      fillColor: "#16a34a",
      fillOpacity: 0.65,
      strokeColor: "#15803d",
      strokeWeight: 2,
    });

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
  });

  button.addEventListener("click", async () => {
    const geojson = await loadRegionLayer(map, region, button, status);

    if (geojson) {
      status.textContent += " Клікни по воді, щоб обрати.";
    }
  });
}
