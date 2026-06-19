import random

import streamlit as st

from logic_utils import (
    check_guess,
    get_outcome_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

ATTEMPT_LIMITS = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}


def reset_game(low: int, high: int, difficulty: str) -> None:
    """Start a fresh game for the selected difficulty."""
    st.session_state.game_id = st.session_state.get("game_id", 0) + 1
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.active_difficulty = difficulty


st.set_page_config(page_title="Game Glitch Investigator", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("Debugged, tested, and ready to play.")

st.sidebar.header("Game Settings")
difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

low, high = get_range_for_difficulty(difficulty)
attempt_limit = ATTEMPT_LIMITS[difficulty]

if (
    "secret" not in st.session_state
    or st.session_state.get("active_difficulty") != difficulty
):
    reset_game(low, high, difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

st.subheader("Make a guess")
st.info(f"Guess a whole number between {low} and {high}.")

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.game_id}",
    disabled=st.session_state.status != "playing",
)

submit_col, new_game_col, hint_col = st.columns(3)
with submit_col:
    submit = st.button(
        "Submit Guess",
        type="primary",
        disabled=st.session_state.status != "playing",
    )
with new_game_col:
    new_game = st.button("New Game")
with hint_col:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    reset_game(low, high, difficulty)
    st.rerun()

if submit:
    ok, guess, error = parse_guess(raw_guess)

    if not ok:
        st.error(error)
    elif guess < low or guess > high:
        st.error(f"Enter a number between {low} and {high}.")
    else:
        st.session_state.attempts += 1
        outcome = check_guess(guess, st.session_state.secret)
        st.session_state.history.append(
            {
                "Attempt": st.session_state.attempts,
                "Guess": guess,
                "Result": outcome,
            }
        )
        st.session_state.score = update_score(
            st.session_state.score,
            outcome,
            st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.balloons()
            st.rerun()
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.rerun()
        elif show_hint:
            st.warning(get_outcome_message(outcome))

if st.session_state.status == "won":
    attempt_word = "attempt" if st.session_state.attempts == 1 else "attempts"
    st.success(
        f"You won in {st.session_state.attempts} valid {attempt_word}! "
        f"Final score: {st.session_state.score}. "
        "Start a new game to play again."
    )
elif st.session_state.status == "lost":
    st.error(
        f"Out of attempts. The secret was {st.session_state.secret}. "
        "Start a new game to try again."
    )

attempts_left = max(0, attempt_limit - st.session_state.attempts)
metric_attempts, metric_score, metric_range = st.columns(3)
metric_attempts.metric("Attempts left", attempts_left)
metric_score.metric("Score", st.session_state.score)
metric_range.metric("Number range", f"{low}-{high}")
st.progress(st.session_state.attempts / attempt_limit)

if st.session_state.history:
    st.subheader("Guess History")
    st.dataframe(
        st.session_state.history,
        hide_index=True,
        width="stretch",
    )

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Valid attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption(
    "Built with AI assistance, then verified with tests and manual play."
)
