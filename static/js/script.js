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
		if(elem.classList.contains('active')) {
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
const add2cart = document.querySelector('.add2cart_btn');

if (add2cart) {
	add2cart.addEventListener('click', (evt) => {
		add2cart.classList.add('incart');
		add2cart.textContent = 'В корзине';
	});
}

//modal cart
const modalCart = document.querySelector('.cart_block');

modalCart.addEventListener('click', (event) => {
	event.preventDefault();
	event.stopPropagation();

	modalCart.classList.add('open');
	
	document.addEventListener( 'click', hideCart)	;
});

function hideCart(e) {
	const cartPopup = document.querySelector('.cart_menu');

	if ( !cartPopup.contains(e.target) ) {
		modalCart.classList.remove('open');
		document.removeEventListener('click', hideCart);
	}	
}