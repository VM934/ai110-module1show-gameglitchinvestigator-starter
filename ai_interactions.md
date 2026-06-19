# AI Interactions Log

## Agent Workflow

**What task did you give the agent?**

Audit and complete the Game Glitch Investigator starter project, fix its
objective bugs, refactor reusable logic, improve test coverage, and verify the
live application.

**What did the agent do?**

- Audited the starter files and git history.
- Ran the original tests and recorded the three failures.
- Refactored game rules into `logic_utils.py`.
- Reworked Streamlit session-state and reset handling in `app.py`.
- Expanded the tests from 3 cases to 25 cases, including live Streamlit
  interaction tests.
- Updated the README, reflection, and interaction log.
- Ran pytest, style checks, Python compilation, and live-app verification.

**What did you have to verify or fix manually?**

I reviewed whether the documented behavior matched the actual starter and
whether the reflection accurately described my experience. I also verified the
live UI and reviewed the final repository before submission.

## Test Generation

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Reasoning |
|---|---|---|---|---|
| Empty input | Test invalid guesses without consuming attempts | Reject `None`, blank, and whitespace | Yes | Empty input should not become a valid guess |
| Decimal input | Test ambiguous numeric input | Reject `4.2` instead of silently converting it to `4` | Yes | A guessing game requests whole numbers |
| Hint direction | Verify higher/lower messages | `Too High` maps to `Go lower`; `Too Low` maps to `Go higher` | Yes | The starter messages contradicted the comparison result |
| Scoring | Test whether wrong guesses change score | Wrong guesses preserve the current score | Yes | Incorrect guesses should not award points |
| Difficulty | Verify every configured range | Easy, Normal, Hard, and unknown fallback | Yes | Difficulty changes must produce predictable ranges |

## Verification Commands

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m pycodestyle app.py logic_utils.py tests
.venv/bin/python -m py_compile app.py logic_utils.py tests/test_game_logic.py tests/test_app.py
```

## Style and Refactor Notes

Prompt used:

```text
Review the project for grading readiness. Focus on readable names, separated
logic, PEP8-style formatting, testable helper functions, and whether the
README/reflection clearly explain the debugging process.
```

Useful suggestions I kept:

- Move comparison, parsing, scoring, and difficulty rules out of the Streamlit
  page so they can be tested directly.
- Use names like `parse_guess`, `check_guess`, and `update_score` because they
  describe one job each.
- Keep player-facing messages separate from the raw comparison result so the
  code can say `Too High` while the UI says `Go lower.`

Suggestions I reviewed before accepting:

- The assistant suggested testing invalid input and edge cases. I accepted that,
  but I checked the tests against the actual app behavior instead of assuming
  the generated tests were correct.
- The assistant suggested making the app reset after a win. I kept the reset
  manual through the New Game button because that gives the player time to see
  the winning result and score.

Style check output:

```text
$ .venv/bin/python -m pycodestyle app.py logic_utils.py tests
# no output; pycodestyle found no reported style violations
```
