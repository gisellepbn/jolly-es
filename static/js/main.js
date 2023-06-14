document.addEventListener('DOMContentLoaded', () => {
	// Navbar elements
	const menu_icon = document.querySelector('.menu-icon');
	const menu = document.querySelector('.menu');

	// Quiz search options
	const quiz_search_select = document.querySelector('#quiz-search-options');
	const search_query = document.querySelector('#search_query');

	// Live quiz
	const live_quiz = document.querySelector('#live-quiz');
	const message = document.querySelector('.message');
	const live_question = document.querySelector('.live-question');
	const timer = document.querySelector('#question-timer');
	const choice_a = document.querySelector('#a');
	const choice_b = document.querySelector('#b');
	const choice_c = document.querySelector('#c');
	const choice_d = document.querySelector('#d');
	const next_btn = document.querySelector('#next-btn');

	// Edit quiz section
	const questions = document.querySelectorAll('.question');
	const question_text = document.querySelector('#question');
	const option_a = document.querySelector('#choice_a');
	const option_b = document.querySelector('#choice_b');
	const option_c = document.querySelector('#choice_c');
	const option_d = document.querySelector('#choice_d');
	const answer_key = document.querySelector('#answer_key');
	const points = document.querySelector('#points');
	const seconds = document.querySelector('#seconds');
	const reset_question_icon = document.querySelector('#reset-question-form');
	const question_form = document.querySelector('.question-form');
	const add_question_btn = document.querySelector('#add-question');
	const edit_question_btn = document.querySelector('#edit-question');
	const delete_question_btn = document.querySelector('#delete-question');
	const delete_quiz_btn = document.querySelector('#delete-quiz');
	const modal = document.querySelector('.modal');
	const confirm = document.querySelector('#confirm');
	const cancel = document.querySelector('#cancel');

	// Start quiz section
	const start_questions = document.querySelectorAll('.start-question');
	const start_question_text = document.querySelector('#start-q-text');
	const start_text_a = document.querySelector('#start-text-a');
	const start_text_b = document.querySelector('#start-text-b');
	const start_text_c = document.querySelector('#start-text-c');
	const start_text_d = document.querySelector('#start-text-d');
	const time_limit = document.querySelector('#time-limit');
	const question_num = document.querySelector('#question-number');
	const question_points = document.querySelector('#question-points');
	const send_question_btn = document.querySelector('#send-question');
	const choice_texts = document.querySelectorAll('.choice-text');
	const start_quiz = document.querySelector('#start-quiz');
	const end_quiz_btn = document.querySelector('#end-quiz');
	const scoreboard_btn = document.querySelector('#scoreboard');
	const refresh_icon = document.querySelector('#refresh-icon');

	// Scoreboard elements
	const participant_box = document.querySelectorAll('.participant');
	const expand_btn = document.querySelector('#expand-btn');
	const scoreboard_container = document.querySelector('#scoreboard-container');
	const back_btn = document.querySelector('.back-btn');
	const image_div = document.querySelector('.image');

	// Input fields
	const input_set = document.querySelectorAll('input');

	if (live_question) {
		const question = live_question.dataset.question;
		const pin = live_question.dataset.pin;

		// check if there is an active question and it has not been answered by the participant yet
		if (
			question !== '' &&
			sessionStorage.getItem(`question_${pin}_${question}`) === null
		) {
			live_question.classList.remove('hidden');
			message.classList.add('message-hidden');
			live_quiz.style.background = '#f9f7f7';

			window.addEventListener('load', () => {
				if (!sessionStorage.getItem('countdown')) {
					countdown(timer.dataset.time, timer);
					sessionStorage.setItem('countdown', 'true');
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

	participant_box.forEach((participant) => {
		participant.querySelector(
			'.place-circle'
		).style.backgroundColor = `#${participant.dataset.color}`;
	});

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

	questions.forEach((selected_question) => {
		selected_question.addEventListener('click', () => {
			const question_id = selected_question.dataset.question;

			questions.forEach((question) => {
				question.style.backgroundColor = 'transparent';
			});
			selected_question.style.backgroundColor = '#dbe2ef';

			question_details(question_id);
			edit_question_btn.dataset.question = question_id;
			delete_question_btn.dataset.question = question_id;

			add_question_btn.classList.add('hidden');
			edit_question_btn.classList.remove('hidden');
			delete_question_btn.classList.remove('hidden');
		});
	});

	if (edit_question_btn) {
		edit_question_btn.addEventListener('click', (e) => {
			e.preventDefault();
			const question_id = edit_question_btn.dataset.question;
			edit_question(question_id);
		});
	}

	if (delete_question_btn) {
		delete_question_btn.addEventListener('click', (e) => {
			e.preventDefault();
			const question_id = delete_question_btn.dataset.question;
			delete_question(question_id);
		});
	}

	if (reset_question_icon) {
		reset_question_icon.addEventListener('click', () => {
			this.preventDefault;
			question_form.reset();
			add_question_btn.classList.remove('hidden');
			edit_question_btn.classList.add('hidden');
			delete_question_btn.classList.add('hidden');
		});
	}

	if (delete_question_btn) {
		delete_quiz_btn.addEventListener('click', (e) => {
			e.preventDefault();
			modal.showModal();
		});
	}

	if (cancel) {
		cancel.addEventListener('click', () => {
			modal.close();
		});
	}

	if (confirm) {
		confirm.addEventListener('click', () => delete_quiz(modal.dataset.quiz));
	}

	if (start_questions) {
		start_questions.forEach((question) => {
			const question_id = question.dataset.question;
			const text_div = document.querySelectorAll('.choice-text');

			if (sessionStorage.getItem(`sent_question_${question_id}`)) {
				const question_div = document.querySelector(
					`[data-question='${question_id}']`
				);
				question_div.disabled = true;
				question_div.classList.add('disabled');
			}

			// Set active question with page reload
			if (sessionStorage.getItem('active_question') === question_id) {
				send_question(question_id);
			}

			question.addEventListener('click', () => {
				start_questions.forEach((question) => {
					question.style.backgroundColor = 'transparent';
				});
				question.style.backgroundColor = '#dbe2ef';

				// Change border of div with correct answer
				text_div.forEach((div) => {
					div.style.border = 'none';
				});

				if (!sessionStorage.getItem('question_counter')) {
					sessionStorage.setItem('question_counter', 1);
				}
				start_question_details(question_id);
				send_question_btn.dataset.question = question_id;
				send_question_btn.disabled = false;
				send_question_btn.classList.remove('disabled-btn');
			});
		});
	}

	if (send_question_btn) {
		send_question_btn.addEventListener('click', () => {
			let counter = parseInt(sessionStorage.getItem('question_counter'));
			sessionStorage.setItem('question_counter', ++counter);

			const question_id = send_question_btn.dataset.question;
			send_question(question_id);

			// add sent question to list of host sent questions
			sessionStorage.setItem(`sent_question_${question_id}`, 'true');
		});
	}

	if (end_quiz_btn) {
		end_quiz_btn.addEventListener('click', () => {
			end_quiz(start_quiz.dataset.quiz);
		});
	}

	if (next_btn) {
		next_btn.addEventListener('click', () => reloadPage());
	}

	if (scoreboard_btn) {
		scoreboard_btn.addEventListener('click', () => {
			scoreboard(start_quiz.dataset.quiz);
		});
	}

	if (expand_btn) {
		expand_btn.addEventListener('click', (e) => {
			e.preventDefault();

			if (scoreboard_container.requestFullscreen) {
				scoreboard_container.requestFullscreen();
			} else if (scoreboard_container.webkitRequestFullscreen) {
				/* Safari */
				scoreboard_container.webkitRequestFullscreen();
			} else if (container_container.msRequestFullscreen) {
				/* IE11 */
				scoreboard_container.msRequestFullscreen();
			}
		});
	}

	if (scoreboard_container) {
		scoreboard_container.addEventListener('fullscreenchange', () => {
			expand_btn.classList.toggle('hidden');
			back_btn.classList.toggle('hidden');
			// image_div.querySelector('img').classList.toggle('hidden');
		});
	}

	window.addEventListener('load', () => {
		const loader = document.querySelector('.loader-container');
		loader.style.display = 'none';
	});

	if (refresh_icon) {
		refresh_icon.addEventListener('click', reloadPage);
	}

	input_set.forEach((input) => {
		input.addEventListener('invalid', () => {
			this.setCustomValidity('Por favor, complete la información');
		});
	});

	// Functions

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
		fetch(`/live-quiz/${pin}/${participant}`, {
			method: 'POST',
			body: JSON.stringify({
				answer: key,
				seconds: seconds,
			}),
			headers: { 'X-CSRFToken': getCookie('csrftoken') },
		}).then(() => {
			// clear countdown from sessionStorage
			sessionStorage.removeItem('countdown');

			// add answered question to list of answered questions
			sessionStorage.setItem(
				`question_${pin}_${live_question.dataset.question}`,
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

	function question_details(question) {
		fetch(`/question/${question}`)
			.then((response) => response.json())
			.then((question) => {
				question_text.value = question.question;
				option_a.value = question.choice_A;
				option_b.value = question.choice_B;
				option_c.value = question.choice_C;
				option_d.value = question.choice_D;
				answer_key.value = question.answer_key;
				points.value = question.points;
				seconds.value = question.seconds;
			});
	}

	function edit_question(question) {
		fetch(`/question/${question}`, {
			method: 'PUT',
			body: JSON.stringify({
				question_text: question_text.value,
				option_a: option_a.value,
				option_b: option_b.value,
				option_c: option_c.value,
				option_d: option_d.value,
				answer_key: answer_key.value,
				points: points.value,
				seconds: seconds.value,
			}),
			headers: { 'X-CSRFToken': getCookie('csrftoken') },
		}).then(() => {
			location.reload();
		});
	}

	function delete_question(question) {
		fetch(`/question/${question}`, {
			method: 'DELETE',
			headers: { 'X-CSRFToken': getCookie('csrftoken') },
		}).then(() => {
			location.reload();
		});
	}

	function delete_quiz(quiz) {
		modal.close();
		fetch(`/delete-quiz/${quiz}`, {
			method: 'DELETE',
			headers: { 'X-CSRFToken': getCookie('csrftoken') },
		}).then(() => {
			document.location.href = '/account/host';
		});
	}

	function start_question_details(question) {
		fetch(`/question/${question}`)
			.then((response) => response.json())
			.then((question) => {
				start_question_text.textContent = question.question;
				start_text_a.textContent = question.choice_A;
				start_text_b.textContent = question.choice_B;
				start_text_c.textContent = question.choice_C;
				start_text_d.textContent = question.choice_D;
				time_limit.textContent = question.seconds + ' sec';

				question_num.textContent = sessionStorage.getItem('question_counter');

				const correct_answer = question.answer_key.toLowerCase();

				const correct_answer_div = document.querySelector(
					`#text-${correct_answer}`
				);

				correct_answer_div.style.border = `1px solid ${correct_answer_div.dataset.color}`;
				question_points.textContent = question.points + ' ptos';
			});
	}

	function send_question(question) {
		fetch(`/question/${question}`, {
			method: 'PUT',
			body: JSON.stringify({
				is_active: true,
				number: sessionStorage.getItem('question_counter') - 1,
			}),
			headers: { 'X-CSRFToken': getCookie('csrftoken') },
		}).then(() => {
			sessionStorage.setItem('active_question', question);

			const question_div = document.querySelector(
				`[data-question='${question}']`
			);

			question_div.disabled = true;
			question_div.classList.add('disabled');

			start_question_text.textContent = '';
			start_text_a.textContent = '';
			start_text_b.textContent = '';
			start_text_c.textContent = '';
			start_text_d.textContent = '';
			question_points.textContent = 'Puntos';
			question_num.textContent = '';
			time_limit.textContent = 'Tiempo';

			// Remove border from correct answer div
			choice_texts.forEach((choice) => {
				choice.style.border = '1px solid #dbe2ef';
			});

			send_question_btn.disabled = true;
			send_question_btn.classList.add('disabled-btn');
		});
	}

	function end_quiz(quiz) {
		fetch(`/start-quiz/${quiz}`, {
			method: 'PUT',
			body: JSON.stringify({
				is_active: false,
			}),
			headers: { 'X-CSRFToken': getCookie('csrftoken') },
		}).then(() => {
			sessionStorage.clear();
			document.location.href = '/account/all';
		});
	}

	function reloadPage() {
		window.location.reload();
	}

	function scoreboard(quiz) {
		document.location.href = `/scoreboard/${quiz}`;
	}
});
