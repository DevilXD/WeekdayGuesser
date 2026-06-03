# WeekdayDeduction

A simple Python script that interrogates your weekday-deduction skills.

---

# Theory

It’s possible for you to deduce the weekday of any given date, by following a simple mental algorithm based on the [Doomsday rule](https://en.wikipedia.org/wiki/Doomsday_rule). The Doomsday Algorithm is a method developed by mathematician John Conway, who famously was able to deduce the weekday of any given date in under two seconds.

> [!Note]
> For simplicity's sake, the explanation below is intentionally modified and limited to a 1901-2099 years theorethical range, and 1990-2010 years practical range. This reduces the mental capacity needed. See the "Extending the years range" section at the end for more information.
>
> The intended purpose of this is to use it as a party trick for deducing the weekday another person was born on. This works for any other non-birthday date from within the theorethical range though.

To compute the weekday of a particular date, you have to find a reference weekday for a given year first, and then apply an offset based on the combined month and day of the month. For the purpose of this explanation, the following weekday representation offset values are used:

|   Weekday | +Offset | -Offset |
| :-------: | :-----: | :-----: |
|    Monday |   0 / 7 |  0 / -7 |
|   Tuesday |       1 |      -6 |
| Wednesday |       2 |      -5 |
|  Thursday |       3 |      -4 |
|    Friday |       4 |      -3 |
|  Saturday |       5 |      -2 |
|    Sunday |       6 |      -1 |

All calculations related to weekdays have to be done by applying "modulo 7" (%) operation on the result. This allows the weekdays to rotate around from Sunday back to Monday when going up, and Monday to Sunday when going down.

Dates are represented using the day/month/year format. The first number is always the amount of days within a month, not the number representing the month itself.

---

## Finding the referene weekday for a given decade

You need to memorize a few things:

- Reference weekday for year 2000 is Tuesday (1).
- Reference weekady for year 1990 is Wednesday (2).
- Changing reference decades follows a 1-2-1-2 pattern. Direction can be deduced from the two memorized reference decades.
- When counting up within a decade, the reference weekday changes up by 1. When counting down, it changes down by 1.
- Leap years are divisible by 4 - this can be deduced from just the last two digits. If the second-to-last digit is even, leap years end with a 0, 4 and 8. If the second-to-last digit is odd, leap years end with 2 and 6.
- When going up from a non-leap year to a leap year, you need to increase the weekday count by 2 instead. Similarly, when going down from a leap year to a non-leap year, you need to decrease it by 2.

When changing the reference decade, you have to follow the 1-2-1-2 pattern:

|        1950 |       1960 |         1970 |       1980 |          1990 |        2000 |       2010 |         2020 |         2030 |          2040 |
| :---------: | :--------: | :----------: | :--------: | :-----------: | :---------: | :--------: | :----------: | :----------: | :-----------: |
| Tuesday (1) | Monday (0) | Saturday (5) | Friday (4) | Wednesday (2) | Tuesday (1) | Sunday (6) | Saturday (5) | Thursday (3) | Wednesday (2) |

Notice how the reference weekday increases when going backwards through decades - this can be deduced from the two memorized 2000-Tuesday and 1990-Wednesday reference decades. Since the difference between those two is 1, the next step between decades changes by 2 instead: 1990-Wednesday -> 1980-Friday, with the next decade step changing by only 1 again. It works similarly when going up the other way, just mind the direction: 2000-Tuesday -> 2010-Sunday. This is how you can use the two reference decades and the 1-2-1-2 rule to figure out the reference decade.

## Finding the reference weekday for a given year

You need to memorize a few more things:

- Leap years are divisible by 4 - this can be deduced from just the last two digits of the year. If the second-to-last digit is even, leap years end with a 0, 4 and 8. If the second-to-last digit is odd, leap years end with 2 and 6.
- When counting the years up within a decade, the reference weekday changes up by 1. When counting down, it changes down by 1.
- When going up from a non-leap year to a leap year, the reference weekday changes up by 2 instead. Similarly, when going down from a leap year to a non-leap year, it changes down by 2 instead as well.

Once you have the reference decade that's close to the target year, you can quickly arrive at the reference weekday for a given year, by adding the amount of years in the last digit to the amount of leap years encountered along the way, and taking a modulo 7 operation at the end. The result is an offset from the decade's reference day. Here's a few examples:

- 1986 -> 1980-Friday -> 1984 was leap -> `6 last digit + 1 leap % 7 == 0` -> +0 offset from Friday -> Friday
- 1999 -> 1990-Wednesday -> 1992 and 1996 were leap -> `9 last digit + 2 leap % 7 == 4` -> +4 offset from Wednesday -> Sunday
- 2002 -> 2000-Tuesday -> no leap years -> `2 last digit + 0 leap % 7 == 2` -> +2 offset from Tuesday -> Thursday
- 2014 -> 2010-Sunday -> 2012 was leap -> `4 last digit + 1 leap % 7 == 5` -> +5 offset from Sunday -> Friday

It's also possible to do this via substraction, but with a catch - you need to watch out closely for the leap -> non-leap transition, as it's easy to forget to account for it here. For the example year 1999, you can use 2000-Tuesday as the starting point, and simply go back by 1 year. Accounting for the year 2000 being a leap and 1999 being non-leap, you need to substract 2 instead of 1, so for the 2000-Tuesday reference, going back by 2 gives you Sunday immediately. Similarly, going 1 more year back requires you to only substract 1 from the weekday offset (non-leap to non-leap transition), giving you Saturday.

### Speedup: Memorizing reference weekdays for a particular range of years

The fastest way of arriving at the reference weekday for a particular year, is done by simply memorizing a bunch of year-weekday pairs. You have a lot of flexibility here:

- You can memorize the reference decades only (1980, 1990, 2000, 2010, etc.), allowing you to bypass having to use the 1-2-1-2 rule and calculating the offset.
- You can memorize a particular range of years (1990-2010 for ex.), allowing you to skip all year-related offset calculations entirely.

The downside here is having to memorize a lot more information, rather than a bunch of rules explaining how to arrive at the answer. The upside is a huge increase in the weekday deduction speed, of course. Going this route is up for you to decide. Here are the pre-computed weekdays for the 1990-2010 years range:

|         1990  |          1991 |         1992 |       1993 |       1994 |        1995 |         1996 |          1997 |         1998 |         1999 |        2000 |
| :-----------: | :-----------: | :----------: | :--------: | :--------: | :---------: | :----------: | :-----------: | :----------: | :----------: | :---------: |
| Wednesday (2) |  Thursday (3) | Saturday (5) | Sunday (6) | Monday (0) | Tuesday (1) | Thursday (3) |    Friday (4) | Saturday (5) |   Sunday (6) | Tuesday (1) |
|          2000 |          2001 |         2002 |       2003 |       2004 |        2005 |         2006 |          2007 |         2008 |         2009 |        2010 |
| :-----------: | :-----------: | :----------: | :--------: | :--------: | :---------: | :----------: | :-----------: | :----------: | :----------: | :---------: |
|   Tuesday (1) | Wednesday (2) | Thursday (3) | Friday (4) | Sunday (6) |  Monday (0) |  Tuesday (1) | Wednesday (2) |   Friday (4) | Saturday (5) |  Sunday (6) |

---

## Finding the weekday offset for a given month and day

This is the second step of the weekday-deduction process. There's a few more rules you need to memorize:

- For all even-numbered months, with February (2) as the only exception, the same-numbered day within the month falls on the reference weekday. This gives you 4/4, 6/6, 8/8, 10/10 and 12/12 as anchors.
- For all other months in order, you need to memorize this sequence: 3-7-7_2-4-5-7. This gives you 3/1, 7/2, 7/3, 2/5, 4/7, 5/9 and 7/11 as anchors.
- The 5/9 and 7/11 anchors are reversible, which means that 9/5 and 11/7 can also be treated as anchors. The PI day (14/3) is also an anchor.

The year's reference weekday lands exactly on each of those anchors. For example, if the reference weekday is a Monday, that means that 3/1, 7/2, 7/3, 4/4, 2/5, 6/6, 4/7, 8/8, 5/9, 10/10, 7/11 and 12/12 were all Mondays wihin that year. This gives you an anchor point within each of those months, from which you can calculate a weekday for any other day of a particular month, by simply adding together the amount of days from the date, to the day offset given by the anchor, and then applying modulo 7 at the end. Here's a few examples:

- 25/6, year's reference weekday: Friday -> 6/6 anchor -> `25 + 6 % 7 == 3` -> +3 offset from Friday -> Monday
