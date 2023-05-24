document.addEventListener('DOMContentLoaded', () => {
	// Navbar elements
	const menu_icon = document.querySelector('.menu-icon');
	const menu = document.querySelector('.menu');

	// Quiz search options
	const quiz_search_select = document.querySelector('#quiz-search-options');
	const search_query = document.querySelector('#search_query');

	// Live quiz
	const message = document.querySelector('.message');
	const participant_name = document.querySelector('#participant-name');
	const live_question = document.querySelector('.live-question');
	const timer = document.querySelector('#question-timer');
	const choice_a = document.querySelector('#a');
	const choice_b = document.querySelector('#b');
	const choice_c = document.querySelector('#c');
	const choice_d = document.querySelector('#d');

	if (live_question) {
		const question = live_question.dataset.question;

		// check there is an active question and it has not been answered by the participant yet
		if (
			question !== '' &&
			localStorage.getItem(`question-${question}`) === null
		) {
			message.classList.toggle('message-hidden');
			live_question.classList.toggle('hidden');
			const live_quiz = document.querySelector('#live-quiz');
			live_quiz.style.background = '#f9f7f7';

			window.addEventListener('load', () => {
				if (!localStorage.getItem('countdown')) {
					countdown(timer.dataset.time, timer);
					localStorage.setItem('countdown', 'true');
				} else {
					// submit answer with score 0
					submit_answer(
						'',
						parseInt(timer.textContent),
						parseInt(live_question.dataset.pin),
						live_question.dataset.participant
					);
				}
			});
		} else {
			live_question.style.display = 'none';
		}
	}

	// Event Handlers
	menu_icon.addEventListener('click', () => {
		menu_icon.classList.toggle('active-menu');
		menu.classList.toggle('hidden');
	});

	if (quiz_search_select) {
		quiz_search_select.addEventListener('change', () => {
			document.location.href = quiz_search_select.value;
		});
	}

	if (choice_a) {
		choice_a.addEventListener('click', () =>
			submit_answer(
				'A',
				parseInt(timer.textContent),
				parseInt(live_question.dataset.pin),
				live_question.dataset.participant
			)
		);
	}

	if (choice_b) {
		choice_b.addEventListener('click', () =>
			submit_answer(
				'B',
				parseInt(timer.textContent),
				parseInt(live_question.dataset.pin),
				live_question.dataset.participant
			)
		);
	}

	if (choice_c) {
		choice_c.addEventListener('click', () =>
			submit_answer(
				'C',
				parseInt(timer.textContent),
				parseInt(live_question.dataset.pin),
				live_question.dataset.participant
			)
		);
	}

	if (choice_d) {
		choice_d.addEventListener('click', () =>
			submit_answer(
				'D',
				parseInt(timer.textContent),
				parseInt(live_question.dataset.pin),
				live_question.dataset.participant
			)
		);
	}

	function countdown(sec, display) {
		let countdown = setInterval(() => {
			if (sec > 0) {
				display.textContent = --sec + ' sec';
			} else {
				// submit answer with score 0
				clearInterval(countdown);
				submit_answer(
					'',
					parseInt(timer.textContent),
					parseInt(live_question.dataset.pin),
					live_question.dataset.participant
				);
			}
		}, 1000);
	}

	function submit_answer(key, seconds, pin, participant) {
		console.log('key', key);
		console.log('seconds', seconds);
		console.log('pin', pin);
		console.log('participant', participant);

		fetch(`/live-quiz/${pin}/${participant}`, {
			method: 'POST',
			body: JSON.stringify({
				answer: key,
				seconds: seconds,
			}),
			headers: { 'X-CSRFToken': getCookie('csrftoken') },
		}).then(() => {
			// clear countdown from localstorage
			localStorage.removeItem('countdown');

			// add answered question to list of answered questions
			localStorage.setItem(
				`question-${live_question.dataset.question}`,
				'true'
			);

			document.location.href = `/live-quiz/${pin}/${participant}`;
		});
	}

	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			const cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === name + '=') {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
});
