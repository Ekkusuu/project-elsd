let currentData = null;
let editor = null;

function setupEditor() {
    // Initialize Ace editor
    editor = ace.edit("code-editor");
    editor.setTheme("ace/theme/xcode");
    
    // Configure editor settings
    editor.setOptions({
        fontSize: "14px",
        showPrintMargin: false,
        highlightActiveLine: true,
        enableLiveAutocompletion: true,
        enableSnippets: true,
        tabSize: 4,
        useSoftTabs: true,
        printMarginColumn: 80,
        displayIndentGuides: true,
        showFoldWidgets: true
    });

    // Set our custom Timeline mode
    editor.session.setMode("ace/mode/timeline");
}

function showError(message, errors = null, errorType = null) {
    const errorDiv = document.getElementById('error-message');
    let errorHtml = '';

    if (errorType === 'lexer_error' || errorType === 'parser_error') {
        errorHtml = `<h3>${message}</h3>`;
        if (errors && errors.length > 0) {
            errorHtml += '<ul>';
            errors.forEach(error => {
                errorHtml += `<li>Line ${error.line}, Column ${error.column}: ${error.message}</li>`;
            });
            errorHtml += '</ul>';
        }
    } else if (errorType === 'validation_error') {
        errorHtml = `<h3>${message}</h3>`;
        if (errors && errors.length > 0) {
            errorHtml += '<ul>';
            errors.forEach(error => {
                const location = error.line ? ` at line ${error.line}${error.column ? `, column ${error.column}` : ''}` : '';
                errorHtml += `<li>${error.message}${location}</li>`;
            });
            errorHtml += '</ul>';
        }
    } else if (errorType === 'runtime_error') {
        errorHtml = `<h3>${message}</h3>`;
        if (errors && errors.message) {
            errorHtml += `<p>${errors.message}</p>`;
            if (errors.traceback) {
                errorHtml += `<pre class="error-traceback">${errors.traceback}</pre>`;
            }
        }
    } else {
        // For other error types (like export_missing)
        errorHtml = `<p>${message}</p>`;
    }

    errorDiv.innerHTML = errorHtml;
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
        button.textContent = component.id;
        button.title = `${component.type}: ${component.title}`; // Show type and title on hover
        button.onclick = () => showComponent(component);
        selector.appendChild(button);
    });

    // Show the first component by default
    if (components.length > 0) {
        showComponent(components[0]);
    }
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

    // Show/hide appropriate buttons
    document.getElementById('copy-json').style.display = tabName === 'json' ? 'block' : 'none';
    document.getElementById('download-json').style.display = tabName === 'json' ? 'block' : 'none';
    document.getElementById('copy-png').style.display = tabName === 'image' ? 'block' : 'none';
    document.getElementById('download-png').style.display = tabName === 'image' ? 'block' : 'none';
}

function showComponent(component) {
    // Update active state of buttons
    document.querySelectorAll('.component-button').forEach(button => {
        if (button.textContent === component.id) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });

    // Show visualization content
    document.getElementById('visualization-content').style.display = 'block';

    // Update tabs visibility and content
    const imageTabBtn = document.getElementById('image-tab-btn');
    const jsonTabBtn = document.getElementById('json-tab-btn');
    
    if (component.type === 'timeline') {
        // Show image tab and switch to it
        imageTabBtn.style.display = 'block';
        document.getElementById('timeline-image').src = 'data:image/png;base64,' + component.image;
        document.getElementById('timeline-image').style.display = 'block';
        switchTab('image');
    } else {
        imageTabBtn.style.display = 'none';
        // Hide image download button if switching from timeline to non-timeline
        document.getElementById('download-png').style.display = 'none';
        // Switch to JSON tab if we're on image tab
        if (document.getElementById('image-tab').classList.contains('active')) {
            switchTab('json');
        }
    }
    
    // Update JSON view
    const jsonData = typeof component.json === 'string' ? JSON.parse(component.json) : component.json;
    document.getElementById('json-view').innerHTML = formatJSON(jsonData);
    
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

async function copyJSON() {
    if (!currentData) return;
    
    const jsonData = typeof currentData.json === 'string' ? currentData.json : JSON.stringify(currentData.json, null, 2);
    try {
        await navigator.clipboard.writeText(jsonData);
        showCopyFeedback('copy-json');
    } catch (err) {
        console.error('Failed to copy JSON:', err);
    }
}

async function copyImage() {
    if (!currentData || currentData.type !== 'timeline') return;
    
    try {
        // Create a canvas element
        const img = document.getElementById('timeline-image');
        const canvas = document.createElement('canvas');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        
        // Draw the image onto the canvas
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);
        
        // Get the blob from the canvas
        const blob = await new Promise(resolve => canvas.toBlob(resolve));
        
        // Copy the image to clipboard
        await navigator.clipboard.write([
            new ClipboardItem({
                'image/png': blob
            })
        ]);
        
        showCopyFeedback('copy-png');
    } catch (err) {
        console.error('Failed to copy image:', err);
    }
}

function showCopyFeedback(buttonId) {
    const button = document.getElementById(buttonId);
    const originalText = button.textContent;
    button.textContent = 'Copied!';
    button.disabled = true;
    
    setTimeout(() => {
        button.textContent = originalText;
        button.disabled = false;
    }, 1500);
}

async function visualize() {
    clearError();
    
    const code = editor.getValue();
    
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