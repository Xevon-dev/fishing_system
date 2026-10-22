// Прибирає фото товару, якщо воно не завантажилось (захист магазину від гарячих посилань).
document.querySelectorAll('.tackle-card__image').forEach(function (image) {
    image.addEventListener('error', function () {
        image.remove();
    });
});
