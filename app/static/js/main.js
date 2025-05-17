document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const progress = document.getElementById('progress');
    const progressBar = document.querySelector('.progress-bar');
    const status = document.getElementById('status');
    const alertBox = document.getElementById('alert');
    const submitBtn = document.getElementById('submitBtn');
    const spinner = submitBtn.querySelector('.spinner-border');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        alertBox.classList.add('d-none');
        progress.classList.remove('d-none');
        progressBar.style.width = '30%';
        status.textContent = 'Uploading...';
        spinner.classList.remove('d-none');
        submitBtn.disabled = true;

        const formData = new FormData(form);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            progressBar.style.width = '70%';
            status.textContent = 'Processing...';
            if (response.ok) {
                return response.blob();
            } else {
                return response.json().then(data => { throw data; });
            }
        })
        .then(blob => {
            progressBar.style.width = '100%';
            status.textContent = 'Done! Downloading results...';
            spinner.classList.add('d-none');
            submitBtn.disabled = false;
            // Download the file
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'results.csv';
            document.body.appendChild(a);
            a.click();
            a.remove();
            setTimeout(() => {
                progress.classList.add('d-none');
                progressBar.style.width = '0%';
            }, 2000);
        })
        .catch(err => {
            spinner.classList.add('d-none');
            submitBtn.disabled = false;
            progress.classList.add('d-none');
            progressBar.style.width = '0%';
            alertBox.textContent = err.error || 'An error occurred. Please try again.';
            alertBox.classList.remove('d-none');
        });
    });
}); 