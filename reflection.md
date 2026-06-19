# Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The first version looked like a working guessing game, but several parts of its
behavior were unreliable. The higher and lower messages were reversed, invalid
input consumed attempts, and starting a new game did not fully reset the game.
The UI also displayed a hard-coded range that could disagree with the selected
difficulty. The biggest warning sign was that the app could run while still
behaving incorrectly.

**Bug Reproduction Log**

| Input / Action | Expected Behavior | Actual Starter Behavior | Console Output / Error |
|---|---|---|---|
| Guess `60` when secret is `50` | Report `Too High` and tell player to go lower | Reported `Too High` but displayed `Go HIGHER!` | No console error |
| Submit blank input | Show validation error without using an attempt | Increased attempts and stored invalid input in history | `Enter a guess.` |
| Select New Game after a loss | Reset the entire game | Changed the secret, but preserved lost status, score, and history | App immediately stopped on the old status |
| Run provided tests | Game logic tests should pass | `check_guess` was not implemented in `logic_utils.py` | 3 `NotImplementedError` failures |

## 2. How did you use AI as a teammate?

I used an AI coding assistant as a teammate to audit the starter code,
identify inconsistent behavior, propose a refactor, and generate additional
tests. A useful suggestion was separating player-facing hint messages from
`check_guess`, which made the provided test contract clear and easy to verify.
I verified that suggestion by running pytest and manually checking the live
app. I did not accept every behavior in the AI-generated starter, such as
truncating decimal input or rewarding some incorrect guesses, because targeted
tests showed those choices were confusing.

## 3. Debugging and testing your fixes

I treated a bug as fixed only when both the relevant automated test passed and
the live Streamlit behavior matched the expected result. I expanded the three
provided comparison tests into a 25-test suite covering difficulty ranges,
input parsing, hint direction, scoring, and complete app interactions. I also
compiled the Python files and manually exercised the running app. AI helped
propose edge cases, but the tests and live behavior were the evidence used to
accept or reject each change.

## 4. What did you learn about Streamlit and state?

Streamlit reruns the script from top to bottom after a user interacts with a
widget. Normal Python variables can therefore be recreated on every rerun,
while `st.session_state` keeps values such as the secret number, score, status,
and history between interactions. A reliable reset has to update every related
session-state value, not only the secret number. I also learned that changing a
difficulty setting should intentionally start a fresh game so old state cannot
conflict with the new range.

## 5. Looking ahead: your developer habits

I want to keep using small pure functions and targeted tests before changing a
larger user interface. Next time I work with AI-generated code, I will define
the expected behavior first and ask for tests that can disprove the proposed
solution. This project reinforced that AI-generated code can look polished and
still contain contradictory logic. I should treat AI as a collaborator whose
work needs evidence-based review, not as an authority.
