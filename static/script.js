
function updateToLanguageOptions() {
    var fromLanguage = document.querySelector('input[name="fromLanguageSelect"]:checked').value;
    var toLanguageRadios = document.querySelectorAll('input[name="toLanguageSelect"]');
    
    toLanguageRadios.forEach(function(radio) {
        radio.disabled = (radio.value === fromLanguage);
    });
}

function updateFromLanguageOptions() {
    var toLanguage = document.querySelector('input[name="toLanguageSelect"]:checked').value;
    var fromLanguageRadios = document.querySelectorAll('input[name="fromLanguageSelect"]');
    
    fromLanguageRadios.forEach(function(radio) {
        radio.disabled = (radio.value === toLanguage);
    });
}

document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();

    var videoLink = document.querySelector('input[name="videoLink"]').value;
    var fromLanguage = document.querySelector('input[name="fromLanguageSelect"]:checked').value;
    var toLanguage = document.querySelector('input[name="toLanguageSelect"]:checked').value;
    var loadingDiv = document.getElementById('loading');
    var downloadButtonDiv = document.getElementById('downloadButton');
    var videoPlayerDiv = document.getElementById('videoPlayer');
    var downloadLink = document.getElementById('downloadLink');
    var errorMessageDiv = document.getElementById('error-message');

    loadingDiv.style.display = 'block';
    // Hide Download button and videoplayer on each new request
    downloadButtonDiv.style.display = 'none';
    videoPlayerDiv.style.display = 'none';
    errorMessageDiv.style.display = 'none';

    // Sending data to server
    fetch('/process_video', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'videoLink=' + encodeURIComponent(videoLink) + '&fromLanguageSelect=' + encodeURIComponent(fromLanguage) + '&toLanguageSelect=' + encodeURIComponent(toLanguage)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        loadingDiv.style.display = 'none';

        downloadButtonDiv.style.display = 'block';
        
        // Pass video_path to the /download endpoint
        downloadLink.href = '/download?video_path=' + encodeURIComponent(data.video_path);
        
        //downloadLink.onclick = function() { location.href = downloadLink.href; };  // Add a download event handler
        videoPlayerElement.src = data.video_url;
        videoPlayerElement.pause(); // Pause video
        videoPlayerDiv.style.display = 'block';
    })
    .catch(error => {
        loadingDiv.style.display = 'none';
        errorMessageDiv.style.display = 'block';
        console.error('There was a problem with the fetch operation:', error);
        // Display or log an error message on the page
        errorMessageDiv.textContent = 'An error occurred: ' + error.message;
    });
});