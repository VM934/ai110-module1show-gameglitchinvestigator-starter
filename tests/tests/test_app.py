from streamlit.testing.v1 import AppTest


def load_app():
    return AppTest.from_file("app.py").run()


def test_initial_game_state():
    app = load_app()

    assert not app.exception
    assert app.title[0].value == "🎮 Game Glitch Investigator"
    assert [(metric.label, metric.value) for metric in app.metric] == [
        ("Attempts left", "8"),
        ("Score", "0"),
        ("Number range", "1-100"),
    ]


def test_invalid_guess_does_not_use_an_attempt():
    app = load_app()
    app.text_input[0].set_value("not a number")
    app.button[0].click().run()

    assert app.session_state.attempts == 0
    assert app.error[0].value == "Enter a whole number."
    assert app.metric[0].value == "8"


def test_out_of_range_guess_does_not_use_an_attempt():
    app = load_app()
    app.text_input[0].set_value("101")
    app.button[0].click().run()

    assert app.session_state.attempts == 0
    assert app.error[0].value == "Enter a number between 1 and 100."
    assert app.metric[0].value == "8"


def test_too_high_guess_shows_correct_hint_and_history():
    app = load_app()
    app.session_state.secret = 50
    app.text_input[0].set_value("60")
    app.button[0].click().run()

    assert app.session_state.attempts == 1
    assert app.warning[0].value == "Go lower."
    assert app.session_state.history == [
        {"Attempt": 1, "Guess": 60, "Result": "Too High"}
    ]
    assert app.metric[0].value == "7"


def test_winning_guess_finishes_game_and_awards_score():
    app = load_app()
    app.session_state.secret = 50
    app.text_input[0].set_value("50")
    app.button[0].click().run()

    assert app.session_state.status == "won"
    assert app.session_state.score == 100
    assert any(
        "You won in 1 valid attempt!" in item.value
        for item in app.success
    )
    assert app.metric[1].value == "100"
    assert app.button[0].disabled
    assert app.text_input[0].disabled


def test_final_incorrect_guess_finishes_and_locks_game():
    app = load_app()
    app.session_state.secret = 50
    app.session_state.attempts = 7
    app.text_input[0].set_value("60")
    app.button[0].click().run()

    assert app.session_state.status == "lost"
    assert app.session_state.attempts == 8
    assert any("Out of attempts." in item.value for item in app.error)
    assert app.button[0].disabled
    assert app.text_input[0].disabled


def test_new_game_resets_all_player_state():
    app = load_app()
    app.text_input[0].set_value("50")
    app.session_state.status = "won"
    app.session_state.attempts = 3
    app.session_state.score = 80
    app.session_state.history = [
        {"Attempt": 1, "Guess": 50, "Result": "Too Low"}
    ]
    app.button[1].click().run()

    assert app.session_state.status == "playing"
    assert app.session_state.attempts == 0
    assert app.session_state.score == 0
    assert app.session_state.history == []
    assert 1 <= app.session_state.secret <= 100
    assert app.text_input[0].value == ""


def test_changing_difficulty_starts_a_fresh_game_in_the_new_range():
    app = load_app()
    app.session_state.attempts = 3
    app.session_state.score = 40
    app.selectbox[0].set_value("Hard").run()

    assert app.session_state.active_difficulty == "Hard"
    assert app.session_state.attempts == 0
    assert app.session_state.score == 0
    assert 1 <= app.session_state.secret <= 500
    assert app.metric[2].value == "1-500"
