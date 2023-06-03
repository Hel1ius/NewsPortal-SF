window.addEventListener('load', function () {
    var randomImage = document.getElementById('random-image');
    var images = [
        '/static/images/1.jpeg',
    ];

    function getRandomImage() {
        var randomIndex = Math.floor(Math.random() * images.length);
        var randomImageUrl = images[randomIndex];
        return randomImageUrl
    }

    function loadRandomImage() {
        var randomImageUrl = getRandomImage();
        randomImage.style.backgroundImage = 'url(' + randomImageUrl + ')';
        randomImage.style.opacity = '0.3';
    }

    loadRandomImage();

    randomImage.addEventListener('click', function () {
        loadRandomImage();
    });
});