document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const uploadButton = document.getElementById('uploadButton');
    const messageDiv = document.getElementById('message');
    const uploadedImage = document.getElementById('uploadedImage');

    uploadButton.addEventListener('click', () => {
        const file = fileInput.files[0];
        if (!file) {
            messageDiv.textContent = 'Please select a file.';
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    messageDiv.textContent = `Upload successful: ${data.filename}`;
                    uploadedImage.src = data.url; // Set the src attribute to the image URL
                } else {
                    messageDiv.textContent = `Error: ${data.error}`;
                    uploadedImage.src = ''; // Clear the image if there's an error
                }
            })
            .catch(error => {
                messageDiv.textContent = `Upload failed: ${error.message}`;
                uploadedImage.src = ''; // Clear the image if there's an error
            });
    });
});

let videoStream;
document.addEventListener('DOMContentLoaded', () => {
    const startCameraButton = document.getElementById('start-camera');
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture');
    const context = canvas.getContext('2d');

    startCameraButton.addEventListener('click', () => {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({
                video: true
            }).then(stream => {
                video.srcObject = stream;
                video.style.display = 'block';
                captureButton.style.display = 'block';
                startCameraButton.style.display = 'none';
                video.play();
            });
        }
    });

    // Capture the image when the button is clicked
    captureButton.addEventListener('click', () => {
        context.drawImage(video, 0, 0, 640, 480);
        const dataURL = canvas.toDataURL('image/jpeg');

        fetch('/upload_image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: 'image=' + encodeURIComponent(dataURL)
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
    // Stop the webcam stream
    document.getElementById('stop').addEventListener('click', function() {
        if (videoStream) {
            videoStream.getTracks().forEach(track => track.stop());
            }
        });
});

document.getElementById('search-form').submit = function() {
    // Allow form to submit
    setTimeout(function() {
        // Clear the input field after form submission
        document.getElementById('query').value = '';
    }, 0);
};

document.querySelector('input[type="file"]').addEventListener('change', function() {
    const fileName = this.files[0].name;
    const label = this.nextElementSibling;
    label.textContent = fileName;
});


document.addEventListener("DOMContentLoaded", function() {
    const preElements = document.querySelectorAll(".results-container pre");

    if (preElements.length === 0) {
        console.error("No elements found with the selector '.results-container pre'");
        return;
    }

    preElements.forEach(pre => {
        let content = pre.innerHTML;
        // Convert **bold** to <strong>bold</strong>
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Convert *bullet* to <li>bullet</li>
        content = content.replace(/\*(.*?)\*/g, '<li>$1</li>');
        // Wrap <li> items with <ul> if there are any
        if (content.includes('<li>')) {
            content = '<ul>' + content + '</ul>';
        }
        pre.innerHTML = content;
    });
});

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('img').forEach(function(img) {
        img.addEventListener('click', function() {
            const filename = this.getAttribute('data-filename');
            if (confirm('Are you sure you want to delete this image?')) {
                fetch(`/delete_image/${filename}`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            alert('Image deleted successfully.');
                            location.reload(); // Reload the page to update the list
                        } else {
                            alert('Error deleting image: ' + data.message);
                        }
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    });
});