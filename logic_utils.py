"""Pure game logic for the Game Glitch Investigator project."""

DIFFICULTY_RANGES = {
    "Easy": (1, 20),
    "Normal": (1, 100),
    "Hard": (1, 500),
}

OUTCOME_MESSAGES = {
    "Win": "Correct!",
    "Too High": "Go lower.",
    "Too Low": "Go higher.",
}


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive number range for a difficulty."""
    return DIFFICULTY_RANGES.get(difficulty, DIFFICULTY_RANGES["Normal"])


def parse_guess(raw: str | None) -> tuple[bool, int | None, str | None]:
    """Parse a whole-number guess from user input."""
    if raw is None or not raw.strip():
        return False, None, "Enter a guess."

    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "Enter a whole number."

    return True, value, None


def check_guess(guess: int, secret: int) -> str:
    """Compare a guess with the secret number."""
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def get_outcome_message(outcome: str) -> str:
    """Return the player-facing hint for an outcome."""
    return OUTCOME_MESSAGES.get(outcome, "Try again.")


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Award more points for winning in fewer valid attempts."""
    if outcome != "Win":
        return current_score

    points = max(10, 110 - (10 * attempt_number))
    return current_score + points
