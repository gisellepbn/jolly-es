document.addEventListener('DOMContentLoaded', () => {
	// Navbar elements
	const menu_icon = document.querySelector('.menu-icon');
	const menu = document.querySelector('.menu');

	// Quiz search options
	const quiz_search_select = document.querySelector('#quiz-search-options');
	const search_query = document.querySelector('#search_query');

	// Event Handlers
	menu_icon.addEventListener('click', () => {
		menu_icon.classList.toggle('active-menu');
		menu.classList.toggle('hidden');
	});

	quiz_search_select.addEventListener('change', () => {
		document.location.href = quiz_search_select.value;
	});
});
