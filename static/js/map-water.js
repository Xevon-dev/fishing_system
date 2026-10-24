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

  const type = get("type") || "водойма";

  const meta = document.createElement("div");
  meta.className = "water-meta";
  meta.textContent = [
    type.charAt(0).toUpperCase() + type.slice(1),
    get("area_km2") ? get("area_km2") + " км²" : "",
  ]
    .filter(Boolean)
    .join(" · ");
  box.append(meta);

  const rows = document.createElement("dl");
  rows.className = "water-rows";

  for (const [label, key] of [
    ["Глибина", "depth"],
    ["Риба", "fish"],
    ["Опис", "description"],
  ]) {
    if (!get(key)) {
      continue;
    }

    const row = document.createElement("div");
    row.className = "water-row";

    const term = document.createElement("dt");
    term.textContent = label;

    const value = document.createElement("dd");
    value.textContent = get(key);

    row.append(term, value);
    rows.append(row);
  }

  if (rows.children.length) {
    box.append(rows);
  }

  const links = document.createElement("div");
  links.className = "water-links";

  for (const [label, key] of [
    ["Вікіпедія", "wikipedia"],
    ["Джерело", "source"],
  ]) {
    if (!get(key)) {
      continue;
    }

    const link = document.createElement("a");
    link.className = "water-link";
    link.href = get(key);
    link.target = "_blank";
    link.rel = "noopener";
    link.textContent = label;
    links.append(link);
  }

  if (links.children.length) {
    box.append(links);
  }
}
