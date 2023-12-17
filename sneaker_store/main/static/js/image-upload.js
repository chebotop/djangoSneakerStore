document.addEventListener('DOMContentLoaded', function() {
    const inputField = document.getElementById('id_images'); // Предполагая, что у вас есть поле с id 'id_images'

    inputField.setAttribute('multiple', 'multiple');

    inputField.addEventListener('change', function(event) {
        const files = event.target.files;
    });
});