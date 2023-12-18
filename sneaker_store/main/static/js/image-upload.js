document.addEventListener('DOMContentLoaded', function() {
    const inputFile = document.getElementById('id_images'); // Предполагая, что у вас есть поле с id 'id_images'

    if (inputFile) {
        inputFile.setAttribute('multiple', 'multiple');
    }
    inputFile.setAttribute();

    inputFile.addEventListener('change', function(event) {
        const files = event.target.files;
    });
});