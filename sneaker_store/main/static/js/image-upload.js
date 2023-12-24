document.addEventListener('DOMContentLoaded', function() {

    const inputFile = document.getElementById('id_images');
    if (inputFile) {
        inputFile.setAttribute('multiple', 'multiple');

        const formRow = inputFile.closest('.form-row');
        const thumbnailsContainer = document.createElement('div');
        thumbnailsContainer.id = 'thumbnails-container';
        formRow.appendChild(thumbnailsContainer);

        const existingImageUrlsElement = document.getElementById('existing-image-urls');
        if (existingImageUrlsElement) {
            const existingImageUrls = JSON.parse(document.getElementById('existing-image-urls').textContent || '[]');
            existingImageUrls.forEach(url => {
                const img = document.createElement('img');
                img.src = url;
                img.style.width = '100px';
                img.style.height = '100px';
                img.style.margin = '10px';
                thumbnailsContainer.appendChild(img);
            });
        }
        inputFile.addEventListener('change', function(event) {
            thumbnailsContainer.innerHTML = '';

            for (let i = 0; i < event.target.files.length; i++) {
                const file = event.target.files[i];
                const reader = new FileReader();

                reader.onload = function(e) {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.style.width = '100px';
                    img.style.height = '100px';
                    img.style.margin = '10px';
                    thumbnailsContainer.appendChild(img);
                };

                reader.readAsDataURL(file);
            }
        });
    } else {
        console.error('Input field with id "id_images" not found');
    }
});
