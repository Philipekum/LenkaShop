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

modalCart.addEventListener('click', (event) => {
    if (event.target.tagName !== 'A') { // предотвращаем только для элементов, не являющихся ссылками
        event.preventDefault();
    }
    event.stopPropagation();

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

        console.log($("[name=csrfmiddlewaretoken]").val())
    
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
    
                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
    
            },
    
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });
});


