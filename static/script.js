const textarea = document.getElementById('code-editor');
const lineNumbers = document.getElementById('line-numbers');

function updateLineNumbers() {
    const lines = textarea.value.split('\n');
    const numbers = lines.map((_, i) => (i + 1).toString().padStart(2, ' ')).join('\n');
    lineNumbers.textContent = numbers;
    
    // Update line numbers position to match textarea scroll
    lineNumbers.style.top = -textarea.scrollTop + 'px';
}

// Initialize line numbers
updateLineNumbers();

// Update line numbers on input
textarea.addEventListener('input', updateLineNumbers);

// Update line numbers position on scroll
textarea.addEventListener('scroll', updateLineNumbers);

function visualize() {
    const code = textarea.value;
    const timelineImage = document.getElementById('timeline-image');
    const errorMessage = document.getElementById('error-message');
    const jsonView = document.getElementById('json-view');

    // Reset display
    timelineImage.style.display = 'none';
    errorMessage.style.display = 'none';
    jsonView.textContent = '';

    fetch('/visualize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show the image
            timelineImage.src = 'data:image/png;base64,' + data.image;
            timelineImage.style.display = 'block';
            
            // Show the JSON
            jsonView.textContent = JSON.stringify(JSON.parse(data.json), null, 2);
        } else {
            // Show error message
            errorMessage.textContent = data.error;
            if (data.validation_errors) {
                errorMessage.textContent += '\n' + data.validation_errors.join('\n');
            }
            errorMessage.style.display = 'block';
        }
    })
    .catch(error => {
        errorMessage.textContent = 'An error occurred: ' + error;
        errorMessage.style.display = 'block';
    });
} 