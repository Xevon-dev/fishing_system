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

    loadWeather(weatherBox, event.latLng);
  });


  map.addListener("click", (event) => {
    // якщо це був клік по водоймі — її дані вже показано, погоду теж
    if (Date.now() - waterClickTime < 300) {
      return;
    }

    info.textContent =
      "Координати кліку: " +
      event.latLng.lat().toFixed(5) +
      ", " +
      event.latLng.lng().toFixed(5);

    loadWeather(weatherBox, event.latLng);
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


function showWater(box, props) {
  const get = (key) => props[key] || "";

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


async function loadWeather(box, latLng) {
  const url = box.dataset.weatherUrl + "?lat=" + latLng.lat() + "&lon=" + latLng.lng();

  box.textContent = "Дізнаюся погоду…";

  try {
    const response = await fetch(url);

    if (!response.ok) {
      const data = await response.json();
      box.textContent = data.error || "Не вдалося отримати погоду.";
      return;
    }

    box.innerHTML = await response.text();
  } catch (error) {
    box.textContent = "Не вдалося отримати погоду.";
  }
}
