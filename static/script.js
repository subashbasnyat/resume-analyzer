// JavaScript to display selected file name
const fileInput = document.getElementById('resumeFile');
const fileLabel = document.querySelector('.custom-file-label');

fileInput.addEventListener('change', function() {
    if (fileInput.files.length > 0) {
        fileLabel.textContent = fileInput.files[0].name;
    } else {
        fileLabel.textContent = 'Choose file';
    }
});