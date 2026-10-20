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

  // область з адресного рядка (?region=lviv) — щоб посилання можна було переслати
  const fromUrl = new URLSearchParams(location.search).get("region");
  if (fromUrl && region.querySelector(`option[value="${fromUrl}"]`)) {
    region.value = fromUrl;
  }

  
  let waterClickTime = 0;

  map.data.setStyle({
    fillColor: "#3b82f6",
    fillOpacity: 0.45,
    strokeColor: "#1d4ed8",
    strokeWeight: 1,
  });

  map.data.addListener("click", (event) => {
    waterClickTime = Date.now();
    showWater(info, event.feature);
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
  });


  button.addEventListener("click", async () => {
    const name = region.selectedOptions[0].textContent;
    const url = button.dataset.geojsonUrl.replace("__REGION__", region.value);

    // щоб у адресному рядку було видно, яку область завантажено
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


function boundsOf(geojson) {
  const bounds = new google.maps.LatLngBounds();

  for (const feature of geojson.features) {
    const geometry = feature.geometry;
    const rings =
      geometry.type === "Polygon"
        ? geometry.coordinates
        : geometry.coordinates[0];

    for (const point of rings[0]) {
      bounds.extend(new google.maps.LatLng(point[1], point[0]));
    }
  }

  return bounds;
}


function showWater(box, feature) {
  const get = (key) => feature.getProperty(key) || "";

  box.replaceChildren();

  const title = document.createElement("strong");
  title.className = "water-title";
  title.textContent = get("name") || "Водойма без назви";
  box.append(title);

  const meta = document.createElement("div");
  meta.className = "water-meta";
  meta.textContent =
    (get("type") || "водойма") +
    (get("area_km2") ? " · " + get("area_km2") + " км²" : "");
  box.append(meta);


  for (const [label, key, className] of [
    ["Глибина", "depth", ""],
    ["Риба", "fish", "water-fish"],
    ["Опис", "description", "water-desc"],
  ]) {
    if (!get(key)) {
      continue;
    }
    const line = document.createElement("div");
    line.className = className;
    line.textContent = label + ": " + get(key);
    box.append(line);
  }

  for (const [label, key] of [
    ["Детальніше у Вікіпедії", "wikipedia"],
    ["Джерело", "source"],
  ]) {
    if (!get(key)) {
      continue;
    }
    const link = document.createElement("a");
    link.href = get(key);
    link.target = "_blank";
    link.rel = "noopener";
    link.textContent = label;
    box.append(link);
  }
}
