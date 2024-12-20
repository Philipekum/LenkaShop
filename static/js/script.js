//подсказки у иконок
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

//Options	

const selectSingle_title = document.querySelector('.select_head');
const selectSingle_labels = document.querySelectorAll('.select_item');
if (selectSingle_title) {
    // Toggle option

    selectSingle_title.addEventListener('click', (evt) => {
        const elem = evt.target;
        if (elem.classList.contains('active')) {
            elem.classList.remove('active');
        } else {
            elem.classList.add('active');
        }
    });

    // Close when click to option
    for (let i = 0; i < selectSingle_labels.length; i++) {
        selectSingle_labels[i].addEventListener('click', (evt) => {
            selectSingle_title.textContent = evt.target.textContent;
            selectSingle_title.classList.remove('active');
        });
    }
}
//add2cart button	
// const add2cart = document.querySelector('.add2cart_btn');

// if (add2cart) {
// 	add2cart.addEventListener('click', (evt) => {
// 		add2cart.classList.add('incart');
// 		add2cart.textContent = 'В корзине';
// 	});
// }

// modal cart
const modalCart = document.querySelector('.cart_block');

if (modalCart) {
    modalCart.addEventListener('click', (event) => {
        // Игнорируем клики по интерактивным элементам (например, кнопки, ссылки)
        const target = event.target;
        const tagName = target.tagName;

        // Список тегов, которые не блокируем
        const allowedTags = ['A', 'BUTTON', 'IMG'];

        if (!allowedTags.includes(tagName)) {
            event.preventDefault();
            event.stopPropagation();
        }

        modalCart.classList.add('open');

        document.addEventListener('click', hideCart);
    });

    function hideCart(e) {
        const cartPopup = document.querySelector('.cart_menu');

        if (!cartPopup.contains(e.target)) {
            modalCart.classList.remove('open');
            document.removeEventListener('click', hideCart);
        }
    }
}



// Когда html документ готов (прорисован)
$(document).ready(function () {
    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id товара из атрибута data-product-id
        var product_id = $(this).data("product-id");

        // Из атрибута href берем ссылку на контроллер django
        var add_to_cart_url = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
                cartCount++;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });
    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();
    
        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);
    
        // Получаем id корзины из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_cart = $(this).attr("href");
    
        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
    
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Уменьшаем количество товаров в корзине (отрисовка)
                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);

                // Удаляем товар из DOM
                $("#cart-item-" + cart_id).remove();
                $("#modal-cart-item-" + cart_id).remove();

                // Обновляем общую стоимость
                $(".cart_total_block .row:first-child .col-auto").text(data.total_price);
                $("#modal-cart-total-price").text(data.total_price);

                // Если корзина пуста, обновляем содержимое в обоих контейнерах
                if (cartCount === 0) {
                    // $("#cart-items-container").html(data.cart_items_html);  // Основной контейнер
                    // $("#modal-cart-items-container").html(data.cart_items_html);  // Модальная корзина

                    // Проверяем, если текущая страница — order.html, перезагружаем страницу
                    if (window.location.pathname.includes("/order/")) {
                        location.reload();
                    }

                } else {
                    // Обновляем только содержимое корзины
                    // $("#cart-items-container").html(data.cart_items_html);
                    // $("#modal-cart-items-container").html(data.cart_items_html);
                }
            },
    
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });

        // Теперь + - количества товара 
    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        // Если количества больше одного, то только тогда делаем -1
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Запускаем функцию определенную ниже
        // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                // Изменяем количество товаров в корзине
                var goodsInCartCount = $("#goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                $("#goods-in-cart-count-modal").val(cartCount);

                $(".cart_total_block .row:first-child .col-auto").text(data.total_price);


                // Обновляем только количество и цену конкретного элемента
                $("#cart-item-" + cartID + " .number").val(quantity);
                $("#modal-cart-total-price").text(data.total_price);

                // Если товар удален, скрываем его
                if (quantity === 0) {
                    $("#cart-item-" + cartID).remove();
                    $("#modal-cart-item-" + cartID).remove();
                }

                // Если корзина пуста, обновляем ее содержимое
                if (cartCount === 0) {
                    // $("#cart-items-container").html(data.cart_items_html);
                        // Проверяем, если текущая страница — order.html
                    if (window.location.pathname.includes("/order/")) {
                        location.reload();
                    }
                }


                // Меняем содержимое корзины
                // $("#cart-items-container").html(data.cart_items_html);
                // $("#modal-cart-items-container").html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    }


});


