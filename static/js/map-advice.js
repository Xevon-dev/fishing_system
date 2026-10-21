/**
 * Порада від ШІ генерується лише на вимогу — щоб не витрачати запити даремно.
 */
function prepareAdvice(box, latLng, water) {
  box.replaceChildren();

  const hint = document.createElement("p");
  hint.className = "advice-text";
  hint.textContent =
    "Порада від ШІ генерується за запитом і займає 5–10 секунд.";

  const button = document.createElement("button");
  button.type = "button";
  button.className = "advice-button";
  button.textContent = "✨ Дізнатися пораду";
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

  box.textContent = "Думаю над рекомендацією… (5–10 с)";

  try {
    const response = await fetch(box.dataset.adviceUrl + "?" + params);
    const text = await response.text();

    try {
      const data = JSON.parse(text);
      box.textContent = data.error || "Не вдалося отримати рекомендацію.";
    } catch (notJson) {
      box.innerHTML = text;
    }
  } catch (error) {
    box.textContent = "Не вдалося отримати рекомендацію.";
  }
}
