// static/scripts.js

// Handles button image update for remove button on videos
function toggleButton(videoId) {
    fetch('/toggle_button', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ videoId: videoId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.exists) {
            document.getElementById('buttonImage-' + videoId).src = "static/images/remove_selected.png";
        } else {
            document.getElementById('buttonImage-' + videoId).src = "static/images/remove_unselected.png";
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
