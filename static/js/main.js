document.addEventListener('DOMContentLoaded', () => {
	// Navbar elements
	const menu_icon = document.querySelector('.menu-icon');
	const menu = document.querySelector('.menu');

	// Event Handlers
	menu_icon.addEventListener('click', () => {
		menu_icon.classList.toggle('active-menu');
		menu.classList.toggle('hidden');
	});
});
