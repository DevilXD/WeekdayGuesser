from guess import GuessType


YEAR_MIN: int = 1990  # lowest  possible: 1901
YEAR_MAX: int = 2010  # highest possible: 2099
SLOW_MULTI: float = 0.5  # multiplier for slow answers
# (seconds) threshold below which an answer is considered as a fast one
FAST_THRESHOLD: float = 10.0
# False: The game teaches you by showing the guesses you've got wrong again
# True: The game instantly ends on the first wrong answer
LOSE_INSTANTLY: bool = False
# The weighted frequency for each type of guess that can appear
# Only relative weights matter. Set to zero to disable.
GUESS_CHANCES: dict[GuessType, float] = {
    GuessType.FULL_DATE: 0.0,
    GuessType.YEAR_ONLY: 0.0,
    GuessType.MONTH_ONLY: 0.0,
    GuessType.DAY_MONTH_ONLY: 1.0,
    GuessType.DAY_MONTH_REF: 0.0,
}
