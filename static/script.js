// Handle Resume Uploads
const resumeInput = document.getElementById('resumeFiles');
const resumeList = document.getElementById('resumeList');

resumeInput.addEventListener('change', () => {
    resumeList.innerHTML = '';
    Array.from(resumeInput.files).forEach((file, index) => {
        const listItem = document.createElement('div');
        listItem.className = 'd-flex justify-content-between align-items-center mb-2';
        listItem.innerHTML = `
            <span>${file.name}</span>
            <button type="button" class="btn btn-sm btn-danger" onclick="removeFile('resumeFiles', ${index})">
                <i class="fas fa-times"></i>
            </button>`;
        resumeList.appendChild(listItem);
    });
});

// Handle Job Description Upload
const jobDescriptionInput = document.getElementById('jobDescriptionFile');
const jobDescriptionList = document.getElementById('jobDescriptionList');

jobDescriptionInput.addEventListener('change', () => {
    jobDescriptionList.innerHTML = '';
    Array.from(jobDescriptionInput.files).forEach((file, index) => {
        const listItem = document.createElement('div');
        listItem.className = 'd-flex justify-content-between align-items-center mb-2';
        listItem.innerHTML = `
            <span>${file.name}</span>
            <button type="button" class="btn btn-sm btn-danger" onclick="removeFile('jobDescriptionFile', ${index})">
                <i class="fas fa-times"></i>
            </button>`;
        jobDescriptionList.appendChild(listItem);
    });
});

// Remove a File from the Input
function removeFile(inputId, index) {
    const inputElement = document.getElementById(inputId);
    const fileList = Array.from(inputElement.files);
    fileList.splice(index, 1);

    const dataTransfer = new DataTransfer();
    fileList.forEach(file => dataTransfer.items.add(file));

    inputElement.files = dataTransfer.files;
    inputElement.dispatchEvent(new Event('change'));
}

// Handle form submission and loading state
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('uploadForm');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const uploadButtons = document.querySelectorAll('.upload-btn');
    const submitButton = document.querySelector('button[type="submit"]');
    
    // Prevent upload buttons from submitting the form
    uploadButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission

        // Validate files are selected
        const resumes = resumeInput.files;
        const jobDescription = jobDescriptionInput.files;

        if (resumes.length === 0 || jobDescription.length === 0) {
            alert('Please select both resumes and a job description.');
            return;
        }

        try {
            // Show loading indicator and disable submit button
            loadingIndicator.classList.remove('d-none');
            submitButton.disabled = true;

            // Create FormData and submit
            const formData = new FormData(form);
            const response = await fetch('/parsing-result', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Get the response data
            const result = await response.text();
            
            // Insert the response into the page content
            const contentDiv = document.querySelector('.container');
            contentDiv.innerHTML = result;
            
            // Update the URL without triggering a page reload
            history.pushState({}, '', '/parsing-result');

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during submission. Please try again.');
        } finally {
            loadingIndicator.classList.add('d-none');
            submitButton.disabled = false;
        }
    });
});