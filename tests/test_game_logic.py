import pytest

from logic_utils import (
    check_guess,
    get_outcome_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


@pytest.mark.parametrize(
    ("guess", "secret", "expected"),
    [
        (50, 50, "Win"),
        (60, 50, "Too High"),
        (40, 50, "Too Low"),
    ],
)
def test_check_guess(guess, secret, expected):
    assert check_guess(guess, secret) == expected


@pytest.mark.parametrize(
    ("difficulty", "expected"),
    [
        ("Easy", (1, 20)),
        ("Normal", (1, 100)),
        ("Hard", (1, 500)),
        ("Unknown", (1, 100)),
    ],
)
def test_get_range_for_difficulty(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("42", (True, 42, None)),
        (" 7 ", (True, 7, None)),
        ("-3", (True, -3, None)),
    ],
)
def test_parse_guess_accepts_whole_numbers(raw, expected):
    assert parse_guess(raw) == expected


@pytest.mark.parametrize("raw", [None, "", "   "])
def test_parse_guess_rejects_empty_input(raw):
    assert parse_guess(raw) == (False, None, "Enter a guess.")


@pytest.mark.parametrize("raw", ["hello", "4.2"])
def test_parse_guess_rejects_non_integers(raw):
    assert parse_guess(raw) == (False, None, "Enter a whole number.")


def test_outcome_messages_point_in_the_correct_direction():
    assert get_outcome_message("Too High") == "Go lower."
    assert get_outcome_message("Too Low") == "Go higher."


def test_score_only_changes_after_a_win():
    assert update_score(0, "Too High", 1) == 0
    assert update_score(0, "Too Low", 2) == 0
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 5) == 60
    assert update_score(0, "Win", 20) == 10
