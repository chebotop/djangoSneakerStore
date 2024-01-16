document.addEventListener('DOMContentLoaded', function() {
    var addToCartButton = document.getElementById('add-to-cart-btn');
    var form = document.getElementById('size-form');

    // Функция для сброса стиля кнопки "в корзину"
    function resetAddToCartButton() {
        if (addToCartButton) {
            addToCartButton.textContent = 'Добавить в корзину';
            addToCartButton.classList.remove('btn-danger');
            addToCartButton.classList.add('btn-dark');
        }
    }

    // Обработчик кликов для размеров
    document.querySelectorAll('.size-box').forEach(function(sizeBox) {
        sizeBox.addEventListener('click', function() {
            // Очистить предыдущее выделение
            document.querySelectorAll('.size-box').forEach(function(otherBox) {
                otherBox.classList.remove('size-selected');
            });

            // Добавить класс для визуального выделения к текущему элементу
            this.classList.add('size-selected');

            // Сбросить стиль кнопки "в корзину" на первоначальный
            resetAddToCartButton();

            // Получить и обновить размер
            var selectedSize = this.innerText.trim().split('\n')[0];
            console.log("Selected size:", this.innerText.trim());  // Отладочный вывод
            document.getElementById('selected_size').value = selectedSize;
        });
    });

    // Обработка клика по кнопке "в корзину"
    addToCartButton.addEventListener('click', function(event) {
        event.preventDefault(); // Предотвращаем стандартное поведение кнопки

        // Если товар добавлен в корзину, перенаправляем в нее
        if (this.textContent.trim() === 'Перейти в корзину') {
            window.location.href = '/cart';
            return;
        }

        var formData = new FormData(form); // Собираем данные из формы

        fetch(form.action, {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                addToCartButton.textContent = 'Перейти в корзину';
                addToCartButton.classList.remove('btn-dark');
                addToCartButton.classList.add('btn-danger');
            } else {
                response.text().then(text => console.error(text));
                console.error("Ошибка при добавлении товара в корзину");

            }
        }).catch(error => {
            console.error('Ошибка:', error);
        });
    });
})
