document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.size-box').forEach(function(sizeBox) {
        sizeBox.addEventListener('click', function() {
            // Очистить предыдущее выделение
            document.querySelectorAll('.size-box').forEach(function(otherBox) {
                otherBox.classList.remove('size-selected');
            });

            // Добавить класс для визуального выделения к текущему элементу
            this.classList.add('size-selected');

            // Получить и обновить размер
            var selectedSize = this.innerText.trim();
            console.log("Selected size:", selectedSize);  // Отладочный вывод
            document.getElementById('selected_size').value = selectedSize;
        });
    });
});
