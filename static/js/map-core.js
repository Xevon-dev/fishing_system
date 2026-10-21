
const UKRAINE_CENTER = { lat: 48.3794, lng: 31.1656 };

function createWaterMap(selectorOrElement) {
  const map = new google.maps.Map(selectorOrElement, {
    center: UKRAINE_CENTER,
    zoom: 6,
    mapId: "DEMO_MAP_ID",
  });

  map.data.setStyle({
    fillColor: "#3b82f6",
    fillOpacity: 0.45,
    strokeColor: "#1d4ed8",
    strokeWeight: 1,
  });

  return map;
}

/**
 * Межі однієї водойми на карті — щоб наблизити до неї.
 */
function featureBounds(feature) {
  const bounds = new google.maps.LatLngBounds();
  feature.getGeometry().forEachLatLng((latLng) => bounds.extend(latLng));
  return bounds;
}

/**
 * Вантажить водойми обраної області на карту.
 * Повертає geojson або null, якщо нічого не завантажено.
 */
async function loadRegionLayer(map, region, button, status) {
  if (!region.value) {
    status.textContent = "Обери область зі списку.";
    return null;
  }

  const name = region.selectedOptions[0].textContent;
  const url = button.dataset.geojsonUrl.replace("__REGION__", region.value);

  button.disabled = true;
  status.textContent = "Завантажую водойми…";

  try {
    const response = await fetch(url);

    if (!response.ok) {
      status.textContent = "Дані для «" + name + "» ще не зібрані.";
      return null;
    }

    const geojson = await response.json();

    map.data.forEach((feature) => map.data.remove(feature));
    map.data.addGeoJson(geojson);
    map.fitBounds(boundsOf(geojson));

    status.textContent =
      "Водойм на карті: " +
      geojson.features.length +
      " (" +
      name +
      ").";

    return geojson;
  } catch (error) {
    status.textContent = "Не вдалося завантажити водойми.";
    return null;
  } finally {
    button.disabled = false;
  }
}
