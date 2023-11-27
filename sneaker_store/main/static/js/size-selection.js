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
            var selectedSize = this.innerText.trim().split('\n')[0];
            console.log("Selected size:", selectedSize);  // Отладочный вывод
            document.getElementById('selected_size').value = selectedSize;
        });
    });
});


// Обработка клика по кнопке "в корзину" для перенаправления в корзину
document.addEventListener('DOMContentLoaded', function() {
    var addToCartButton = document.getElementById('add-to-cart-btn');
    var form = document.getElementById('size-form'); // Убедитесь, что у вашей формы есть id="size-form"

    if (!addToCartButton || !form) {
        console.log("Кнопка или форма не найдены!");
        return;
    }

    addToCartButton.addEventListener('click', function(event) {
        event.preventDefault(); // Предотвращаем стандартное поведение кнопки

        var formData = new FormData(form); // Собираем данные из формы

        // Отправляем данные формы асинхронно
        fetch(form.action, {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                console.log("Товар добавлен в корзину");
                // Изменяем текст и стиль кнопки
                addToCartButton.textContent = 'Перейти в корзину';
                addToCartButton.classList.remove('btn-dark');
                addToCartButton.classList.add('btn-danger');
                addToCartButton.onclick = function() {
                    window.location.href = '/cart/';
                };
            } else {
                console.error("Ошибка при добавлении товара в корзину");
            }
        }).catch(error => {
            console.error('Ошибка:', error);
        });
    });
});



