function prepareAdvice(box, latLng, water) {
  box.replaceChildren();

  const hint = document.createElement("p");
  hint.className = "advice-text";
  hint.textContent =
    "Прогноз кльову формується за запитом і займає 5–10 секунд.";

  const button = document.createElement("button");
  button.type = "button";
  button.className = "advice-button";
  button.textContent = "Дізнатися прогноз";
  button.addEventListener("click", () => loadAdvice(box, latLng, water));

  box.append(hint, button);
}

async function loadAdvice(box, latLng, water) {
  const params = new URLSearchParams({
    lat: latLng.lat(),
    lon: latLng.lng(),
    name: water ? water.name : "",
    type: water ? water.type : "",
    area: water ? water.area : "",
    depth: water ? water.depth : "",
    fish: water ? water.fish : "",
  });

  box.textContent = "Формую прогноз кльову… (5–10 с)";

  try {
    const response = await fetch(box.dataset.adviceUrl + "?" + params);
    const text = await response.text();

    try {
      const data = JSON.parse(text);
      box.textContent = data.error || "Не вдалося отримати прогноз кльову.";
    } catch (notJson) {
      box.innerHTML = text;
    }
  } catch (error) {
    box.textContent = "Не вдалося отримати прогноз кльову.";
  }
}
