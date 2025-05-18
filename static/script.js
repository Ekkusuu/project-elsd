let currentData = null;

function calculateLineNumberWidth(numLines) {
    // Create a temporary span to measure text width
    const span = document.createElement('span');
    span.style.visibility = 'hidden';
    span.style.position = 'absolute';
    span.style.whiteSpace = 'pre';
    span.style.font = window.getComputedStyle(document.querySelector('.line-numbers')).font;
    
    // Get width of largest line number
    span.textContent = numLines.toString();
    document.body.appendChild(span);
    const width = span.getBoundingClientRect().width;
    document.body.removeChild(span);
    
    // Add padding for better appearance
    return width; // 20px for padding + 10px extra space
}

function updateLineNumbers() {
    const textarea = document.getElementById('code-editor');
    const lineNumbers = document.getElementById('line-numbers');
    const lines = textarea.value.split('\n');
    
    // Update line numbers content
    lineNumbers.innerHTML = lines.map((_, i) => i + 1).join('\n');
    
    // Update line numbers width
    const width = calculateLineNumberWidth(lines.length);
    lineNumbers.style.width = `${width}px`;
    lineNumbers.style.minWidth = `${width}px`;
    
    // Synchronize scroll position
    lineNumbers.scrollTop = textarea.scrollTop;
}

function setupEditor() {
    const textarea = document.getElementById('code-editor');
    const lineNumbers = document.getElementById('line-numbers');
    
    // Update line numbers on input
    textarea.addEventListener('input', updateLineNumbers);
    
    // Synchronize scrolling
    textarea.addEventListener('scroll', () => {
        lineNumbers.scrollTop = textarea.scrollTop;
    });
    
    // Initial setup
    updateLineNumbers();
}

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // Hide visualization elements
    document.getElementById('component-selector').style.display = 'none';
    document.getElementById('visualization-content').style.display = 'none';
}

function clearError() {
    document.getElementById('error-message').style.display = 'none';
}

function createComponentSelector(components) {
    const selector = document.getElementById('component-selector');
    selector.innerHTML = '';
    selector.style.display = 'flex';

    components.forEach(component => {
        const button = document.createElement('button');
        button.className = 'component-button';
        button.innerHTML = `
            <div class="component-type">${component.type}</div>
            <div class="component-title">${component.title}</div>
            <div class="component-id">${component.id}</div>
        `;
        button.onclick = () => showComponent(component);
        selector.appendChild(button);
    });

    // Show the first component by default
    if (components.length > 0) {
        showComponent(components[0]);
    }
}

function showComponent(component) {
    // Update active state of buttons
    document.querySelectorAll('.component-button').forEach(button => {
        if (button.querySelector('.component-id').textContent === component.id) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });

    // Show visualization content
    document.getElementById('visualization-content').style.display = 'block';

    // Update tabs visibility
    const imageTabBtn = document.getElementById('image-tab-btn');
    const jsonTabBtn = document.getElementById('json-tab-btn');
    
    if (component.type === 'timeline') {
        imageTabBtn.style.display = 'block';
        document.getElementById('download-png').style.display = 'block';
    } else {
        imageTabBtn.style.display = 'none';
        document.getElementById('download-png').style.display = 'none';
        // Switch to JSON tab if we're on image tab
        if (document.getElementById('image-tab').classList.contains('active')) {
            switchTab('json');
        }
    }

    // Update content
    if (component.type === 'timeline') {
        document.getElementById('timeline-image').src = 'data:image/png;base64,' + component.image;
        document.getElementById('timeline-image').style.display = 'block';
    }
    
    // Update JSON view
    const jsonData = typeof component.json === 'string' ? JSON.parse(component.json) : component.json;
    document.getElementById('json-view').innerHTML = formatJSON(jsonData);
    document.getElementById('download-json').style.display = 'block';
    
    // Store current data for downloads
    currentData = component;
}

function formatJSON(obj) {
    return JSON.stringify(obj, null, 2)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
            let cls = 'number';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'key';
                } else {
                    cls = 'string';
                }
            } else if (/true|false/.test(match)) {
                cls = 'boolean';
            } else if (/null/.test(match)) {
                cls = 'null';
            }
            return '<span class="' + cls + '">' + match + '</span>';
        })
        .replace(/\n/g, '<br>')
        .replace(/\s{2}/g, '&nbsp;&nbsp;');
}

function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    document.getElementById(tabName + '-tab-btn').classList.add('active');

    // Update tab content
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    document.getElementById(tabName + '-tab').classList.add('active');
}

function downloadJSON() {
    if (!currentData) return;
    
    const jsonData = typeof currentData.json === 'string' ? currentData.json : JSON.stringify(currentData.json, null, 2);
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentData.id}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function downloadImage() {
    if (!currentData || currentData.type !== 'timeline') return;
    
    const a = document.createElement('a');
    a.href = 'data:image/png;base64,' + currentData.image;
    a.download = `${currentData.id}.png`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

async function visualize() {
    clearError();
    
    const code = document.getElementById('code-editor').value;
    
    try {
        const response = await fetch('/visualize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        });
        
        const data = await response.json();
        
        if (!data.success) {
            showError(data.error || 'An error occurred during visualization');
            return;
        }
        
        createComponentSelector(data.components);
        
    } catch (error) {
        showError('An error occurred while communicating with the server');
    }
}

// Initialize the editor when the page loads
document.addEventListener('DOMContentLoaded', setupEditor); 