from __future__ import annotations

import math
import random
from time import time
from collections import defaultdict

from translate import TR
from guess import Guess, GuessType
from constants import MAX_ANSWER_TIME
from settings import SLOW_MULTI, FAST_THRESHOLD, LOSE_INSTANTLY
from utils import (  # noqa
    uinput,
    uinput2,
    wday_check,
    shift_check,
    value_check,
    get_guess_type,
    random_from_dict,
    check_win_threshold,
)

TR.set_language("English")  # use this to change language to any supported by the lang folder


fast: int = 0
good: int = 0
wrong: int = 0
good_sum: float = 0.0
fast_sum: float = 0.0


print()
repeat_flag: bool = False
last_guess: Guess | None = None
wrong_dates: defaultdict[Guess, int] = defaultdict(int)
while True:
    wrong_sum: int = sum(wrong_dates.values())
    score: float = fast + good * SLOW_MULTI - wrong_sum
    win_threshold: float = check_win_threshold(100, wrong)
    progress: float = min(max(score / win_threshold, 0.0), 1.0)
    if score >= win_threshold and (wrong_sum <= 0 or score >= win_threshold * 2):
        print(
            TR("youve_won").format(
                score=f"{score:.1f}/{win_threshold}",
                good=good,
                good_avg=good_sum/good,
                fast=fast,
                slow=good-fast,
                fast_avg=fast_sum/fast,
                wrong=wrong
            )
        )
        break
    for _ in range(100):
        x_limit: int = 20  # For any k_factor, the chance for this limit maxes at y_limit percent
        y_limit: float = 0.8  # max chance
        # k_factor scales linearly from x_limit to this value as the game progresses
        final_k_factor: float = 5
        # k_factor resulting chances breakdown (ends with x_limit ~= y_limit):
        # k=4:  1 ~=  17.8% , 2 ~= *31.7%*, 3 ~= *42.5%*, 5 ~=  57.5% , 10 ~=  73.9% , 15 ~= 78.6%
        # k=5:  1 ~= *14.8%*, 2 ~=  26.9% , 3 ~=  36.8% , 5 ~= *51.5%*, 10 ~= *70.5%*, 15 ~= 77.4%
        # k=6:  1 ~=  12.7% , 2 ~= *23.5%*, 3 ~= *32.6%*, 5 ~=  46.9% , 10 ~=  67.3% , 15 ~= 76.1%
        # k=8:  1 ~= *10.2%*, 2 ~=  19.3% , 3 ~=  27.3% , 5 ~= *40.5%*, 10 ~=  62.2% , 15 ~= 73.8%
        # k=9:  1 ~=   9.4% , 2 ~=  17.9% , 3 ~= *25.4%*, 5 ~=  38.2% , 10 ~= *60.2%*, 15 ~= 72.8%
        # k=11: 1 ~=   8.3% , 2 ~= *15.9%*, 3 ~=  22.8% , 5 ~=  34.9% , 10 ~=  57.0% , 15 ~= 71.1%
        # k=14: 1 ~=   7.3% , 2 ~=  14.0% , 3 ~= *20.3%*, 5 ~= *31.6%*, 10 ~=  53.7% , 15 ~= 69.2%
        # k=19: 1 ~=   6.3% , 2 ~=  12.3% , 3 ~=  17.9% , 5 ~=  28.4% , 10 ~= *50.3%*, 15 ~= 67.1%
        # lin:  1 ~=   4.0% , 2 ~=   8.0%,  3 ~=  12.0% , 5 ~=  20.0% , 10 ~=  40.0% , 15 ~= 60.0%
        k_factor: float = -(x_limit - final_k_factor) * progress + x_limit
        repeat_chance: float = min(
            0.8 * (1 - math.exp(-wrong_sum / k_factor)) / (1 - math.exp(-x_limit / k_factor)),
            y_limit,
        )
        if repeat_flag and random.random() < repeat_chance:
            guess = random_from_dict(wrong_dates, k=1)
        else:
            guess = Guess(get_guess_type())
        if guess != last_guess:
            last_guess = guess
            break

    ask_time: float = time()
    exp_answer: int = guess.answer()
    print(guess)
    print()
    score_text: str = f"{score:.1f}/{win_threshold:.1f}"
    match guess.type:
        case GuessType.MONTH_ONLY:
            usr_answer: int = uinput(
                TR("input", "ref_sequence").format(score=score_text),
                value_check,
            )
        case GuessType.DAY_MONTH_REF:
            usr_answer = uinput(
                TR("input", "closest_ref").format(score=score_text),
                value_check,
            )
        case GuessType.DAY_MONTH_ONLY:
            usr_answer = uinput(TR("input", "shift").format(score=score_text), shift_check)
        case _:
            # usr_answer = uinput(TR("input", "weekday").format(score=score_text), wday_check)
            usr_answer = uinput2(TR("input", "weekday").format(score=score_text))
    # Limit the max answer time
    answer_time: float = min(time() - ask_time, MAX_ANSWER_TIME)

    if usr_answer == exp_answer:
        good += 1
        good_sum += answer_time
        if answer_time < FAST_THRESHOLD:
            fast += 1
            fast_sum += answer_time
            repeat_flag = True
        elif wrong_sum > 30:
            repeat_flag = True
        if (attempts := wrong_dates.get(guess)) is not None:
            wrong_dates[guess] -= 1
            if wrong_dates[guess] <= 0:
                del wrong_dates[guess]
        elif answer_time >= FAST_THRESHOLD and score < win_threshold:
            wrong_dates[guess] += 1
        print(
            TR("good").format(
                wrong=sum(wrong_dates.values()),
                sign='>' if answer_time >= MAX_ANSWER_TIME else '',
                time=answer_time,
            )
        )
    else:
        wrong += 1
        repeat_flag = False
        wrong_dates[guess] += 5 if score < win_threshold else 1
        if LOSE_INSTANTLY:
            answer_text: str = str(exp_answer)
            if guess.type is GuessType.DAY_MONTH_ONLY:
                answer_text = str(exp_answer if exp_answer < 4 else exp_answer - 7)
            print(TR("lose").format(answer=answer_text))
            break
        else:
            print(
                TR("wrong").format(
                    wrong=sum(wrong_dates.values()),
                    sign='>' if answer_time >= MAX_ANSWER_TIME else '',
                    time=answer_time,
                )
            )

    print()

# Highscore for DAY_MONTH_ONLY:
# You've won! Score: 100.5/100.0 (67 good (2.517s avg), 67/0 fast/slow (2.517s fast avg), 0 wrong)
