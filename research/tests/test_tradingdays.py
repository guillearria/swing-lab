"""research/tradingdays — the exchange calendar (2026-09-13)."""
from datetime import date, timedelta

from research import tradingdays as T


def test_every_listed_holiday_is_a_weekday_and_the_list_covers_this_year():
    assert all(d.weekday() < 5 for d in T.HOLIDAYS)
    assert sum(1 for d in T.HOLIDAYS if d.year == 2026) == 10   # the NYSE's fixed ten
    assert sum(1 for d in T.HOLIDAYS if d.year == 2027) == 10
    assert date(2026, 9, 7) in T.HOLIDAYS                        # Labor Day, the live case


def test_count_is_the_weekday_count_minus_holidays():
    assert T.count(date(2026, 9, 4), date(2026, 9, 8)) == 1      # Fri + [Labor Day] → 1, was 2
    assert T.count(date(2026, 8, 10), date(2026, 8, 14)) == 4    # a plain week
    assert T.count(date(2026, 8, 15), date(2026, 8, 16)) == 0    # a Saturday
    assert T.count(date(2026, 9, 8), date(2026, 9, 4)) == 0      # reversed range is empty


def test_add_walks_over_holidays():
    assert T.add(date(2026, 8, 13), 21) == date(2026, 9, 14)     # TWLO — bare weekdays gave 09-11
    assert T.add(date(2026, 8, 14), 21) == date(2026, 9, 15)     # TPR — the digest said 09-14
    assert T.add(date(2026, 8, 4), 21) == date(2026, 9, 2)       # no holiday inside: unchanged


def test_a_year_without_entries_degrades_to_weekdays():
    d0, d1 = date(2030, 1, 1), date(2031, 1, 1)
    weekdays = sum(1 for i in range((d1 - d0).days) if (d0 + timedelta(days=i)).weekday() < 5)
    assert T.count(d0, d1) == weekdays


def test_can_have_matured_mirrors_the_score_gates():
    # CRL 21d logged Wed 08-12: 21st bar is Fri 09-11 → scoreable from 09-12 (what happened)
    assert not T.can_have_matured("2026-08-12", 21, today=date(2026, 9, 11))
    assert T.can_have_matured("2026-08-12", 21, today=date(2026, 9, 12))
    # TWLO 21d logged Thu 08-13, Labor Day inside: 21st bar Mon 09-14 → scoreable from 09-15
    assert not T.can_have_matured("2026-08-13", 21, today=date(2026, 9, 14))
    assert T.can_have_matured("2026-08-13", 21, today=date(2026, 9, 15))
    assert not T.can_have_matured("2026-09-10", 63, today=date(2026, 9, 14))   # a fresh core row
