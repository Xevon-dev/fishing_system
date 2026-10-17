function initMap() {
    const map = new google.maps.Map(document.querySelector("#map"), {
        center: { lat: 48.3794, lng: 31.1656 },
        zoom: 6,
        mapId: "DEMO_MAP_ID",
    });

    map.addListener("click", function (event) {
        const lat = event.latLng.lat().toFixed(5);
        const lng = event.latLng.lng().toFixed(5);
        document.querySelector("#water-info").textContent =
            "Координати кліку: " + lat + ", " + lng;
    });
}
