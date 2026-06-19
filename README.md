# Game Glitch Investigator: The Impossible Guesser

## Project Purpose

Game Glitch Investigator is a Streamlit number-guessing game that began as
broken AI-generated code. The project demonstrates how to investigate,
refactor, test, and verify AI-generated code instead of assuming that code is
correct because it runs.

## Mission Coverage

- **Find the bugs:** documented nine concrete starter-code defects and four
  reproducible examples.
- **Explain why the logic failed:** separated comparison rules, player-facing
  messages, parsing, scoring, and Streamlit state so each failure is clear.
- **Fix the code and prove it:** added pure-logic and full Streamlit interaction
  tests, then manually verified the running game.
- **Reflect on AI-assisted debugging:** recorded the agent workflow, accepted
  and rejected suggestions, verification process, and lessons learned.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py
```

Run the test suite with:

```bash
python -m pytest -q
```

## Bugs Found

1. Higher and lower hints pointed in the wrong direction.
2. The app and provided tests disagreed about the return value of
   `check_guess`.
3. Invalid input consumed an attempt and was saved in guess history.
4. Attempts started at one before the player made a guess.
5. Starting a new game did not reset status, score, or history.
6. Starting a new game always generated a number from 1 to 100 instead of the
   selected difficulty range.
7. Changing difficulty did not reliably reset the active game.
8. The displayed range was hard-coded as 1 to 100.
9. Score changed after incorrect guesses and could reward a wrong answer.

## Fixes Applied

- Moved all reusable game rules into `logic_utils.py`.
- Standardized `check_guess` to return `Win`, `Too High`, or `Too Low`.
- Added a separate player-facing message helper with correct directions.
- Added strict whole-number parsing and validation.
- Rebuilt game reset and difficulty-change handling around Streamlit session
  state.
- Counted only valid guesses as attempts.
- Cleared the previous guess whenever a fresh game starts.
- Made the selected range visible and accurate throughout the interface.
- Made scoring deterministic and awarded points only after a win.
- Added guess history, progress, metrics, and clearer game-over states.
- Expanded the test suite to cover comparison logic, parsing, difficulty
  ranges, messages, scoring, and complete Streamlit interaction flows.

## Demo Walkthrough

1. Start the Streamlit app and choose Easy, Normal, or Hard in the sidebar.
2. Confirm that the number range, attempts allowed, and status metrics match
   the selected difficulty.
3. Enter a non-number or an out-of-range number and verify that the app shows
   an error without consuming an attempt.
4. Enter a valid incorrect guess and verify that the hint points in the correct
   direction and the guess appears in history.
5. Open Developer Debug Info, enter the secret number, and verify that the game
   reports a win and awards a score.
6. Select New Game and verify that attempts, score, status, history, and secret
   number are reset.
7. Change difficulty and verify that a fresh game starts within the new range.

## Manual Run Trace

```text
Scenario: Normal difficulty, secret number visible in Developer Debug Info = 50

Input: hello
Result: App displays "Enter a whole number." Attempts stay at 0.

Input: 150
Result: App displays "Enter a number between 1 and 100." Attempts stay at 0.

Input: 60
Result: Valid attempt #1. Guess history records 60 as "Too High."
Player hint says "Go lower."

Input: 40
Result: Valid attempt #2. Guess history records 40 as "Too Low."
Player hint says "Go higher."

Input: 50
Result: Valid attempt #3. App reports a win and awards 80 points.

Action: New Game
Result: Attempts return to 0, score returns to 0, history clears, and a new
secret number is generated for the selected range.
```

## Test Results

```text
$ python -m pytest -q
.........................                                                [100%]
25 passed
```

## Enhanced UI

The finished app includes:

- Live attempt, score, and number-range metrics
- Attempt progress bar
- Valid-guess history table
- Difficulty-aware ranges and resets
- Clear input-validation, win, and game-over states

The main UI changes are in `app.py` through `reset_game`, session-state
management, and the Streamlit display flow. The reusable rules live in
`logic_utils.py` through `parse_guess`, `check_guess`, `get_outcome_message`,
`get_range_for_difficulty`, and `update_score`.
