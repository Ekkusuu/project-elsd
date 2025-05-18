const textarea = document.getElementById('code-editor');
const lineNumbers = document.getElementById('line-numbers');

// Store the current visualization data
let currentData = {
    image: null,
    json: null
};

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

function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    document.querySelector(`.tab-button[onclick="switchTab('${tabName}')"]`).classList.add('active');

    // Update tab panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

function downloadImage() {
    if (!currentData.image) return;
    
    // Create a temporary link
    const link = document.createElement('a');
    link.href = 'data:image/png;base64,' + currentData.image;
    link.download = 'timeline.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function downloadJSON() {
    if (!currentData.json) return;
    
    // Create a temporary link
    const link = document.createElement('a');
    const blob = new Blob([JSON.stringify(JSON.parse(currentData.json), null, 2)], { type: 'application/json' });
    link.href = URL.createObjectURL(blob);
    
    // Get the object type and ID from the JSON for the filename
    const jsonData = JSON.parse(currentData.json);
    const objectType = jsonData.type || 'timeline'; // Default to 'timeline' if type not present
    const objectId = jsonData.id || 'export';
    link.download = `${objectId}.json`;
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
}

function resetVisualization() {
    const timelineImage = document.getElementById('timeline-image');
    const errorMessage = document.getElementById('error-message');
    const jsonView = document.getElementById('json-view');
    const downloadPngBtn = document.getElementById('download-png');
    const downloadJsonBtn = document.getElementById('download-json');
    const imageTabBtn = document.getElementById('image-tab-btn');
    const jsonTabBtn = document.getElementById('json-tab-btn');

    // Reset display
    timelineImage.style.display = 'none';
    errorMessage.style.display = 'none';
    jsonView.textContent = '';
    downloadPngBtn.style.display = 'none';
    downloadJsonBtn.style.display = 'none';
    imageTabBtn.style.display = 'none';
    currentData = { image: null, json: null };

    // Always show JSON tab button and make it active
    jsonTabBtn.style.display = 'block';
    switchTab('json');
}

function visualize() {
    const code = textarea.value;
    resetVisualization();

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
            // Store the data
            currentData.json = data.json;
            currentData.image = data.image;
            
            // Parse JSON to determine if we're dealing with a timeline
            const jsonData = JSON.parse(data.json);
            const isTimeline = data.type === 'timeline';

            // Show JSON content first
            const jsonView = document.getElementById('json-view');
            const downloadJsonBtn = document.getElementById('download-json');
            jsonView.textContent = JSON.stringify(jsonData, null, 2);
            downloadJsonBtn.style.display = 'block';

            // Handle timeline-specific UI elements
            const timelineImage = document.getElementById('timeline-image');
            const downloadPngBtn = document.getElementById('download-png');
            const imageTabBtn = document.getElementById('image-tab-btn');

            if (isTimeline) {
                // Show image tab button regardless of whether we have an image
                imageTabBtn.style.display = 'block';
                
                if (data.image) {
                    // We have an image to display
                    timelineImage.src = 'data:image/png;base64,' + data.image;
                    timelineImage.style.display = 'block';
                    downloadPngBtn.style.display = 'block';
                    // Switch to image tab for timelines with images
                    switchTab('image');
                } else {
                    // No image available, but still show the tab (it will be empty)
                    timelineImage.style.display = 'none';
                    downloadPngBtn.style.display = 'none';
                    // Stay on JSON tab
                    switchTab('json');
                }
            } else {
                // Not a timeline, hide image-related elements
                imageTabBtn.style.display = 'none';
                timelineImage.style.display = 'none';
                downloadPngBtn.style.display = 'none';
                // Ensure we're on JSON tab
                switchTab('json');
            }
        } else {
            // Show error message
            const errorMessage = document.getElementById('error-message');
            errorMessage.textContent = data.error;
            if (data.validation_errors) {
                errorMessage.textContent += '\n' + data.validation_errors.join('\n');
            }
            errorMessage.style.display = 'block';
        }
    })
    .catch(error => {
        const errorMessage = document.getElementById('error-message');
        errorMessage.textContent = 'An error occurred: ' + error;
        errorMessage.style.display = 'block';
    });
} 