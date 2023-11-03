document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();

    var videoLink = document.querySelector('input[name="videoLink"]').value;
    var loadingDiv = document.getElementById('loading');
    var downloadButtonDiv = document.getElementById('downloadButton');
    var videoPlayerDiv = document.getElementById('videoPlayer');
    var downloadLink = document.getElementById('downloadLink');

    loadingDiv.style.display = 'block';

    // Отправка данных на сервер
    fetch('/process_video', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'videoLink=' + encodeURIComponent(videoLink)
    })
    .then(response => response.text())
    .then(videoUrl => {
        loadingDiv.style.display = 'none';
        downloadButtonDiv.style.display = 'block';
        downloadLink.href = videoUrl;
    });

    // Здесь может быть плеер
});
