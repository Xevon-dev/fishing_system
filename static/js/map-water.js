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
