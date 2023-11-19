document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();

    var videoLink = document.querySelector('input[name="videoLink"]').value;
    var loadingDiv = document.getElementById('loading');
    var downloadButtonDiv = document.getElementById('downloadButton');
    var videoPlayerDiv = document.getElementById('videoPlayer');
    var downloadLink = document.getElementById('downloadLink');

    loadingDiv.style.display = 'block';

    // Sending data to server
    fetch('/process_video', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'videoLink=' + encodeURIComponent(videoLink)
    })
    .then(response => response.blob())
    .then(blob => {
        loadingDiv.style.display = 'none';
        downloadButtonDiv.style.display = 'block';
        
        // Create a link to download a video
        var videoUrl = URL.createObjectURL(blob);
        downloadLink.href = '/download';  // Update the download link
        downloadLink.onclick = function() { location.href = videoUrl; };  // Add a download event handler
        videoPlayerElement.src = videoUrl;
        videoPlayerElement.pause(); // Pause video
        videoPlayerDiv.style.display = 'block';
    });
});
