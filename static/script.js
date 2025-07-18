

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('elfFile');
    const runButton = document.getElementById('runButton');
    const output = document.getElementById('output');
    
    let selectedFile = null;
    
    fileInput.addEventListener('change', function(event) {
        selectedFile = event.target.files[0];
        if (selectedFile) {
            runButton.disabled = false;
            output.textContent = `File selected: ${selectedFile.name}`;
        } else {
            runButton.disabled = true;
            output.textContent = '';
        }
    });
    
    runButton.addEventListener('click', async function() {
        if (!selectedFile) {
            output.textContent = 'No file selected';
            return;
        }
        
        try {
            output.textContent = 'Uploading and executing...';
            runButton.disabled = true;
            
            const formData = new FormData();
            formData.append('elfFile', selectedFile);
            
            const response = await fetch('/execute', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                output.textContent = '';
                if (result.stdout) {
                    output.textContent += result.stdout + '\n\n';
                }
                if (result.stderr) {
                    output.textContent += `STDERR: ${result.stderr}\n\n`;
                }
            } else {
                output.textContent = `Error: ${result.error}`;
            }
            
        } catch (error) {
            output.textContent = `Network error: ${error.message}`;
        } finally {
            runButton.disabled = false;
        }
    });
});

