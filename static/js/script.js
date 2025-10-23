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

// Редирект на платежную страницу
// const form = document.getElementById('payment-form');
// if (form) {
//     form.addEventListener('submit', function(e) {
//         e.preventDefault();
//         fetch(form.action, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
//             }
//         }).then(response => response.json())
//           .then(data => {
//               window.location.href = data.redirect_url;
//           });
//     });
// }

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


// Функция прокрутки наверх
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

// Показываем/скрываем кнопку в зависимости от прокрутки
window.addEventListener('scroll', function () {
    const scrollToTopButton = document.getElementById('scroll-to-top');
    if (window.scrollY > 300) {
      scrollToTopButton.style.display = 'flex'; // Показываем кнопку
    } else {
      scrollToTopButton.style.display = 'none'; // Скрываем кнопку
    }
  });

// Включаем строгий режим
'use strict';

// Получаем все формы, к которым нужно применить кастомную валидацию
const forms = document.querySelectorAll('.needs-validation');

// Функция для валидации номера телефона (только российские номера: +7XXXXXXXXXX)
function validatePhoneNumber(phoneInput) {
    const phonePattern = /^\+7\d{10}$/;
    const errorMessage = phoneInput.nextElementSibling;

    if (phoneInput.value.trim() === '') {
        phoneInput.classList.remove('is-valid');
        phoneInput.classList.add('is-invalid');
        phoneInput.setCustomValidity('Пожалуйста, введите ваш номер телефона.');
        errorMessage.textContent = 'Пожалуйста, введите ваш номер телефона.';
        return false;
    } else if (!phonePattern.test(phoneInput.value)) {
        phoneInput.classList.remove('is-valid');
        phoneInput.classList.add('is-invalid');
        phoneInput.setCustomValidity('Введите корректный номер телефона в формате +7XXXXXXXXXX.');
        errorMessage.textContent = 'Введите корректный номер телефона в формате +7XXXXXXXXXX.';
        return false;
    } else {
        phoneInput.classList.remove('is-invalid');
        phoneInput.classList.add('is-valid');
        phoneInput.setCustomValidity('');
        errorMessage.textContent = '';
        return true;
    }
}

// Функция для валидации email (точно такая же, как в Django)
function validateEmail(emailInput) {
    const emailPattern = new RegExp(
        "^(?:[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(?:\\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*|" +
        '"(?:[\\001-\\010\\013\\014\\016-\\037!#-\\[\\]-\\177]|\\\\[\\001-\\011\\013\\014\\016-\\177])*")@' +
        "([A-Z0-9]([A-Z0-9-]*[A-Z0-9])?\\.)+[A-Z0-9]([A-Z0-9-]*[A-Z0-9])?$",
        "i"
    );

    const errorMessage = emailInput.nextElementSibling;

    if (emailInput.value.trim() === '') {
        emailInput.classList.remove('is-valid');
        emailInput.classList.add('is-invalid');
        emailInput.setCustomValidity('Пожалуйста, введите ваш email.');
        errorMessage.textContent = 'Пожалуйста, введите ваш email.';
        return false;
    } else if (!emailPattern.test(emailInput.value)) {
        emailInput.classList.remove('is-valid');
        emailInput.classList.add('is-invalid');
        emailInput.setCustomValidity('Введите корректный email-адрес.');
        errorMessage.textContent = 'Введите корректный email-адрес.';
        return false;
    } else {
        emailInput.classList.remove('is-invalid');
        emailInput.classList.add('is-valid');
        emailInput.setCustomValidity('');
        errorMessage.textContent = '';
        return true;
    }
}

// Перебираем все формы
forms.forEach(function(form) {
    form.addEventListener('submit', function(event) {
        let isValid = true;

        // Получаем поля email и телефона
        const phoneInput = form.querySelector('input[name="phone_number"]');
        const emailInput = form.querySelector('input[name="email"]');

        // Валидируем телефон и email
        if (phoneInput) isValid = validatePhoneNumber(phoneInput) && isValid;
        if (emailInput) isValid = validateEmail(emailInput) && isValid;

        // Если форма невалидна, предотвращаем её отправку
        if (!form.checkValidity() || !isValid) {
            event.preventDefault();
            event.stopPropagation();
        }

        // Добавляем класс 'was-validated' для отображения стилей Bootstrap
        form.classList.add('was-validated');
    }, false);
});

// Автоматическая валидация при вводе (чтобы ошибки обновлялись в реальном времени)
document.addEventListener('DOMContentLoaded', function () {
    const phoneInput = document.querySelector('input[name="phone_number"]');
    const emailInput = document.querySelector('input[name="email"]');

    if (phoneInput) {
        phoneInput.addEventListener('input', () => validatePhoneNumber(phoneInput));
    }

    if (emailInput) {
        emailInput.addEventListener('input', () => validateEmail(emailInput));
    }
});

// Редирект на платежную страницу
const form = document.getElementById('payment-form');
if (form) {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        }).then(response => response.json())
          .then(data => {
              window.location.href = data.redirect_url;
          });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.classList.remove('show');
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 500); // Удаляем элемент после завершения анимации
        });
    }, 5000);
});
