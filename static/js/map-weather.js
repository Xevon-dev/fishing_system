async function loadWeather(box, latLng) {
  const url =
    box.dataset.weatherUrl + "?lat=" + latLng.lat() + "&lon=" + latLng.lng();

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
