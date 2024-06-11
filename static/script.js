document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (!file) {
        return;
    }
    document.getElementById('text-for-ai-processing').innerHTML = '<div class="loader"></div>';
    document.getElementById('full-text-html').innerHTML = '<div class="loader"></div>';
    document.getElementById('run-ai-report-button').classList.add('disabled');
    document.getElementById('run-ai-report-button').style = "margin-bottom: 1rem;"

    document.getElementById('good-summary').innerHTML = '';
    document.getElementById('medium-summary').innerHTML = '';
    document.getElementById('bad-summary').innerHTML = '';

    const formData = new FormData();
    formData.append('file', file);
    
    // checks if it should use the basic or advanced model
    const modelSelection = document.querySelector('input[name="analysis_level"]:checked').value;
    formData.append('model_type', modelSelection);
    
    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log(`PROMPT: ${data.prompt}`)
        if (!data.prompt) {
            document.getElementById('full-text-html').innerHTML = '</div>Error extracting footnotes. File does not contain necessary information.</div>';
            document.getElementById('text-for-ai-processing').innerHTML = 'Could not generate prompt. Error processing footnotes';
        } else {
            document.getElementById('full-text-html').innerHTML = data.html;
            document.getElementById('run-ai-report-button').classList.remove('disabled');
            document.getElementById('text-for-ai-processing').innerHTML = `<strong>Estimated cost to send request: $${data.cost}`;
            // show save as pdf button
            document.getElementById('step-4-right-side').style.display = '';
        }
        
        })
    .catch(error => console.error('Error:', error));
});

document.getElementById('step-4-right-side').addEventListener('click', function() {
    fetch('http://127.0.0.1:5000/save-as-pdf');
});

document.getElementById('run-ai-report-button').addEventListener('click', function() {
    document.getElementById('good-summary').innerHTML = '<div class="loader"></div>';
    document.getElementById('run-ai-report-button').classList.add('disabled');

    var formData = new FormData();

    fetch('http://127.0.0.1:5000/run-report', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('good-summary').innerHTML = data.good;
        document.getElementById('medium-summary').innerHTML = data.medium;
        document.getElementById('bad-summary').innerHTML = data.bad
    })
    .catch(error => console.error('Error:', error));
});


// Used to have a upload button that looks better.
document.querySelector('.upload-file-button').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function() {
    var fileChosenSpan = document.getElementById('file-chosen');
    
    if (this.files && this.files.length > 0) {
        fileChosenSpan.textContent = this.files[0].name;
    } else {
        fileChosenSpan.textContent = 'No file chosen';
    }
});