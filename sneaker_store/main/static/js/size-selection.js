document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.size-box').forEach(function(sizeBox) {
      sizeBox.addEventListener('click', function() {
          // Получить значение размера из содержимого .size-box
          var selectedSize = this.textContent.trim();

          // Установить выбранный размер в скрытое поле формы
          document.getElementById('selected_size').value = selectedSize;

          // Опционально: добавить логику для визуального выделения выбранной кнопки
          document.querySelectorAll('.size-box').forEach(function(otherBox) {
              otherBox.classList.remove('size-selected'); // Убрать класс с предыдущих выбранных кнопок
          });
          this.classList.add('size-selected'); // Добавить класс к выбранной кнопке
      });
  });
    var selectElement = document.getElementById('mobile-size-select');
    if (selectElement) {
        selectElement.addEventListener('change', function() {
            var selectedSize = this.value;
            document.getElementById('selected_size').value = selectedSize;
            // Очищаем визуальное выделение с .size-box
            document.querySelectorAll('.size-box').forEach(function(sizeBox) {
                sizeBox.classList.remove('size-selected');
});