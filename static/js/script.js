// //подсказки у иконок
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

// //Options	

// const selectSingle_title = document.querySelector('.select_head');
// const selectSingle_labels = document.querySelectorAll('.select_item');
// if (selectSingle_title) {
//     // Toggle option

//     selectSingle_title.addEventListener('click', (evt) => {
//         const elem = evt.target;
//         if (elem.classList.contains('active')) {
//             elem.classList.remove('active');
//         } else {
//             elem.classList.add('active');
//         }
//     });

//     // Close when click to option
//     for (let i = 0; i < selectSingle_labels.length; i++) {
//         selectSingle_labels[i].addEventListener('click', (evt) => {
//             selectSingle_title.textContent = evt.target.textContent;
//             selectSingle_title.classList.remove('active');
//         });
//     }
// }

// // modal cart
// const modalCart = document.querySelector('.cart_block');

// if (modalCart) {
//     modalCart.addEventListener('click', (event) => {
//         // Игнорируем клики по интерактивным элементам (например, кнопки, ссылки)
//         const target = event.target;
//         const tagName = target.tagName;

//         // Список тегов, которые не блокируем
//         const allowedTags = ['A', 'BUTTON', 'IMG'];

//         if (!allowedTags.includes(tagName)) {
//             event.preventDefault();
//             event.stopPropagation();
//         }

//         modalCart.classList.add('open');

//         document.addEventListener('click', hideCart);
//     });

//     function hideCart(e) {
//         const cartPopup = document.querySelector('.cart_menu');

//         if (!cartPopup.contains(e.target)) {
//             modalCart.classList.remove('open');
//             document.removeEventListener('click', hideCart);
//         }
//     }
// }


// // Функция прокрутки наверх
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

// // Показываем/скрываем кнопку в зависимости от прокрутки
window.addEventListener('scroll', function () {
    const scrollToTopButton = document.getElementById('scroll-to-top');
    if (window.scrollY > 300) {
      scrollToTopButton.style.display = 'flex'; // Показываем кнопку
    } else {
      scrollToTopButton.style.display = 'none'; // Скрываем кнопку
    }
  });

