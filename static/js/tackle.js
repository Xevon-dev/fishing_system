// Прибирає фото товару, якщо воно не завантажилось (захист магазину від гарячих посилань).
document.querySelectorAll('.tackle-card__image').forEach(function (image) {
    image.addEventListener('error', function () {
        const placeholder = document.createElement('span');
        placeholder.className = 'tackle-card__image-placeholder';
        placeholder.setAttribute('aria-hidden', 'true');
        placeholder.textContent = '✳';
        image.replaceWith(placeholder);
    });
});
