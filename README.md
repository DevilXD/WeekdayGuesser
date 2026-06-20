# WeekdayGuesser

A simple Python script that interrogates your weekday-deduction/guessing skills.

> [!Note]
> Requires Python 3.10+.

---

# Theory

It’s possible for you to deduce the weekday of any given date, by following a simple mental algorithm based on the [Doomsday rule](https://en.wikipedia.org/wiki/Doomsday_rule). The Doomsday Algorithm is a method developed by mathematician John Conway, who famously was able to deduce the weekday of any given date in under two seconds.

> [!Note]
> For simplicity's sake, the explanation below is intentionally modified and limited to a **1901-2099** years theorethical range, and **1990-2010** years practical range. This reduces the mental capacity needed. See the "Extending the years range" section at the end for more information.
>
> The intended purpose of this is to use it as a party trick for deducing the weekday another person was born on. This works for any other non-birthday date from within the theorethical range though.

To compute the weekday of a particular date, you have to find a reference weekday for a given year first, and then apply an offset based on the combined month and day of the month. For the purpose of this explanation, the following weekday representation offset values are used:

|   Weekday | +Offset | -Offset |
| :-------: | :-----: | :-----: |
|    Monday |  0 / +7 |  0 / -7 |
|   Tuesday |      +1 |      -6 |
| Wednesday |      +2 |      -5 |
|  Thursday |      +3 |      -4 |
|    Friday |      +4 |      -3 |
|  Saturday |      +5 |      -2 |
|    Sunday |      +6 |      -1 |

All calculations related to weekdays have to be done by applying the **"modulo 7" (%)** operation on the result. This allows the weekdays to rotate around from Sunday back to Monday when going up, and Monday to Sunday when going down.

Anchor dates are represented using the `day/month` format. The first number is always the amount of days within a month, not the number representing the month itself.
Years may come with their precomputed reference weekday at the end for convenience, ex: **2000-Tuesday**.

---

## Finding the reference weekday for a given decade

You need to memorize a few things:

- Reference weekday for the year **2000** is **Tuesday (1)**.
- Reference weekady for the year **1990** is **Wednesday (2)**.
- Changing reference decades follows a **1-2-1-1** pattern. The direction and first step can be deduced from the two memorized reference decades.

When changing the reference decade, you have to follow the 1-2-1-2 pattern:

|        1950 |       1960 |         1970 |       1980 |          1990 |        2000 |       2010 |         2020 |         2030 |          2040 |
| :---------: | :--------: | :----------: | :--------: | :-----------: | :---------: | :--------: | :----------: | :----------: | :-----------: |
| Tuesday (1) | Monday (0) | Saturday (5) | Friday (4) | Wednesday (2) | Tuesday (1) | Sunday (6) | Saturday (5) | Thursday (3) | Wednesday (2) |

Notice how the reference weekday increases when going backwards through decades - this can be deduced from the two memorized 2000-Tuesday and 1990-Wednesday reference decades. Since the difference between those two memorized years is 1, the next step between decades changes by 2 instead: 1990-Wednesday -> 1980-Friday, with the next decade step changing by only 1 again. It works similarly when going up the other way, just mind the direction: 2000-Tuesday -> 2010-Sunday. This is how you can use the two reference decades and the 1-2-1-2 rule to figure out the reference decade.

> [!Note]
> These rules don't work for years **1900** and **2100**, as those don't count as leap years and that'd have to be accounted for with another rule. Thus, the maximum theorethical years range for these rules is **1901-2099**.

## Finding the reference weekday for a given year

You need to memorize a few more things:

- Leap years are divisible by **4** - this can be deduced from just the last two digits of the year. If the second-to-last digit is **even**, leap years end with a **0**, **4** and **8**. If the second-to-last digit is **odd**, leap years end with **2** and **6**.
- When counting the years up within a decade, the reference weekday changes up by **1**. When counting down, it changes down by **1**.
- When going up from a non-leap year to a leap year, the reference weekday changes up by **2** instead. Similarly, when going down from a leap year to a non-leap year, it changes down by **2** instead as well.

Once you have the reference decade that's close to the target year, you can quickly arrive at the reference weekday for a given year, by adding the amount of years in the last digit, to the amount of leap years encountered along the way, and taking a modulo 7 operation at the end. The result is an offset from the decade's reference day. Note the format is: `years + leap mod 7 == result`. Here's a few examples:

- 1986 -> 1980-Friday -> 1984 was leap -> `6 + 1 mod 7 == 0` -> +0 offset from Friday -> Friday
- 1999 -> 1990-Wednesday -> 1992 and 1996 were leap -> `9 + 2 mod 7 == 4` -> +4/-3 offset from Wednesday -> Sunday
- 2002 -> 2000-Tuesday -> no leap years -> `2 + 0 mod 7 == 2` -> +2 offset from Tuesday -> Thursday
- 2014 -> 2010-Sunday -> 2012 was leap -> `4 + 1 mod 7 == 5` -> +5/-2 offset from Sunday -> Friday

It's also possible to do this via subtraction, but with a catch - you need to watch out closely for the leap -> non-leap transition, as it's easy to forget to account for it here. For the example year 1999, you can use 2000-Tuesday as the starting point, and simply go back by 1 year. Accounting for the year 2000 being a leap and 1999 being non-leap, you need to substract 2 instead of 1, so for the 2000-Tuesday reference, going back by 2 gives you Sunday immediately. Similarly, going 1 more year back requires you to only substract 1 from the weekday offset (non-leap to non-leap transition), giving you Saturday.

### Speedup: Memorizing reference weekdays for a particular range of years

The fastest way of arriving at the reference weekday for a particular year, is done by simply memorizing a bunch of year-weekday pairs. You have a lot of flexibility here:

- You can memorize the reference decades only (1980, 1990, 2000, 2010, etc.), allowing you to bypass having to use the 1-2-1-2 rule and calculating the offset.
- You can memorize a particular range of years (1990-2010 for ex.), allowing you to skip all year-related offset calculations entirely.

The downside here is having to memorize a lot more information, rather than a bunch of rules explaining how to arrive at the answer. The upside is a huge increase in the weekday deduction speed, of course. Going this route is up for you to decide. Here are the pre-computed weekdays for the 1990-2010 years range:

|         1990  |          1991 |         1992 |       1993 |       1994 |        1995 |         1996 |          1997 |         1998 |         1999 |        2000 |
| :-----------: | :-----------: | :----------: | :--------: | :--------: | :---------: | :----------: | :-----------: | :----------: | :----------: | :---------: |
| Wednesday (2) |  Thursday (3) | Saturday (5) | Sunday (6) | Monday (0) | Tuesday (1) | Thursday (3) |    Friday (4) | Saturday (5) |   Sunday (6) | Tuesday (1) |
|          2000 |          2001 |         2002 |       2003 |       2004 |        2005 |         2006 |          2007 |         2008 |         2009 |        2010 |
|   Tuesday (1) | Wednesday (2) | Thursday (3) | Friday (4) | Sunday (6) |  Monday (0) |  Tuesday (1) | Wednesday (2) |   Friday (4) | Saturday (5) |  Sunday (6) |

---

## Finding the weekday offset for a given month and day

This is the second step of the weekday-deduction process. The whole algorithm relies on the idea of anchors: special day-month pairs. **The year's reference weekday lands exactly on those anchors.**

There's a few more rules you need to memorize:

- For all even-numbered months, with **February (2)** as the only exception, the same-numbered day within the month falls on the reference weekday. This gives you **4/4**, **6/6**, **8/8**, **10/10** and **12/12** as anchors.
- For all other months in order, you need to memorize this sequence: **3-7-7_2-4-5-7**. This gives you **3/1**, **7/2**, **7/3**, **2/5**, **4/7**, **5/9** and **7/14** as anchors.
- The **5/9** and **7/11** anchors are reversible, which means that **9/5** and **11/7** can also be treated as anchors. The PI day (**14/3**) is also an anchor, as well as the last day of February (28th for non-leap years, 29th for leap years).

Remember: The year's reference weekday lands exactly on each of those anchors. For example, if the reference weekday is a Monday, that means that **3/1**, **7/2**, **7/3**, **4/4**, **2/5**, **6/6**, **4/7**, **8/8**, **5/9**, **10/10**, **7/11** and **12/12** were all Mondays within that year. This gives you an anchor point within each of those months, from which you can calculate a weekday for any other day of a particular month, by substracting the amount of days of the date, from the day offset given by the anchor, and then applying modulo **7** at the end. Here's a few examples:

- 14/3, year's reference weekday: Tuesday -> 7/3 anchor -> `14 - 7 mod 7 = 0` -> +0 offset from Tuesday -> Tuesday 
- 25/6, year's reference weekday: Friday -> 6/6 anchor -> `25 - 6 mod 7 = 5` -> +5/-2 offset from Friday -> Wednesday
- 18/9, year's reference weekday: Monday -> 12/9 anchor -> `18 - 12 mod 7 = 6` -> +6/-1 offset from Monday -> Sunday
- 21/12, year's reference weekday: Saturday -> 12/12 anchor -> `21 - 12 mod 7 = 2` -> +2 offset from Saturday -> Monday

### Speedup: Memorizing the offsets and anchor day-month pairs

Again, you can reduce the deduction time by memorizing offsets and anchor day-month pairs. Here are the reduced **(mod 7)** offsets for each month, in months' order:

```
3  0  0  4  2  6  4  1  5  3  0  5
```

And here's a breakdown per offset type, containing all anchor day-month pairs:

|                           |     |     |     |     |     |
| ------------------------: | :-: | :-: | :-: | :-: | :-: |
| February, March, November |   0 |   7 |  14 |  21 |  28 |
|                    August |   1 |   8 |  15 |  22 |  29 |
|                       May |   2 |   9 |  16 |  23 |  30 |
|          January, October |   3 |  10 |  17 |  24 |  31 |
|               April, July |   4 |  11 |  18 |  25 |     |
|       September, December |   5 |  12 |  19 |  26 |     |
|                      June |   6 |  13 |  20 |  27 |     |

## Final exception adjustment for leap years

As the very last step in the deduction process, one needs to test for a specific exception. For leap years that haven't passed through the 29th of February yet, you need to substract 1 from the final result to obtain the correct weekday.

The general rules are simple:

- The year is a leap year.
- The month is either January or February.

For ex. if the final deduced weekday would be a Saturday, for a leap year and either January or February as the month, the actuall correct weekday deduction would be Friday instead.

## Putting it all together

Combining the three steps of figuring out the year's reference weekday, day-month offset and applying the final exception, you can finally arrive at the deduced weekday. Here's some examples:

- 14th of September, 1986 -> 1980-Friday +6+1=Friday -> 5/9 anchor -> 14-5 mod 7 = +2 offset from Friday -> Sunday
- 27th of March, 1997 -> 1990-Wednesday +7+2=Friday -> 7/3 anchor -> 27-7 mod 7 = +6/-1 offset from Friday -> Thursday
- 8th of February, 2004 -> 2000-Tuesday +4+1=Sunday -> 7/2 anchor -> 8-7 mod 7 = +1 offset, but final exception applies, so +0 offset from Sunday -> Sunday
- 19th of June, 2016 -> 2010-Sunday +6+2=Monday -> 6/6 anchor -> 19-6 mod 7 = +6/-1 offset from Monday -> Sunday
- 21st of November, 2026 -> 2020-Saturday +6+1=Saturday -> 7/11 anchor -> 21-7 mod 7 = +0 offset from Saturday -> Saturday

---

# Practice

The Python script lets you test your deduction skills in the 5 categories/modes explained below. Some technical details:

- There's currently no interface to change the script's configuration, other than by editing the code directly. This may be resolved in future versions of the script.
- More than one mode can be enabled at the same time. The weights specify how often each deduction type appears relative to the others. Setting the weight to zero prevents the type from appearing.
- There are three types of input methods: "general value", "offset" and "weekday". General value expects any positive or negative integer, offset expects only a range between -6 and 6, and weekday expects a name of a weekday.
- The weekday's name can be specified by only typing in enough letters, that allow for distinguishing the one and only weekday that matches. This is done to reduce the time wasted on typing in the answer.
- The "weekday" input method is currently disabled for `FULL_DATE` and `YEAR_ONLY` modes, and has been replaced by an alternative input method, that significantly speeds up weekday input. The keys ZXCVBNM (the lowest horizontal row of letters on a QWERTY keyboard) are mapped directly to the Monday-Sunday weekdays range. Simply pressing the corresponding key inputs the weekday immediately, without the need of pressing Enter afterwards.

### FULL_DATE: Deduce the weekday for a specific date

You're asked for the weekday of a specific date. Use the ZXCVBNM keys (mapped to the Monday-Sunday range) to answer.

### YEAR_ONLY: Deduce the reference weekday for a specific year

You're asked for the reference weekday for a specific year. Use the ZXCVBNM keys (mapped to the Monday-Sunday range) to answer.
The current practice range is set to 1990-2010, but can be changed by modifying `MIN_YEAR` and `MAX_YEAR` values.

### MONTH_ONLY: Deduce all day anchor offsets for a specific month

You're asked for all day anchor offsets for a specific month. Input all of them without spaces to answer.
Example answer for January: `310172431`, which corresponds to 3rd, 10th, 17th, 24th and 31th of January as anchors.
The initial `0` can be optionally omitted when inputting the answer for February, March and November.

### DAY_MONTH_ONLY: Deduce the shift value for a specific month and day

You're asked for the shift value for a specific month and day. This can only range between -6 and 6, other values are rejected. A special "(leap)" text may sometimes appear to aid you when applying the final exception.

### DAY_MONTH_REF: Deduce the closest reference day for a given month and day

You're asked for the closest reference day of the month, for a specific month and day. For example, for 10th of September, the closest reference day is 12th of September.
The closest reference day of the month is always up to 3 days apart from the given date, except for dates near the end of the month, where the last reference day is expected.
For February, March and November, the "0th" day is also included as a valid option. Note that there's only one correct answer for a given date.
