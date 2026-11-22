# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/takhao666/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/takhao666/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

An entry for make.fun's `news-image-20261123` competition: one image that sums up the world's news of Monday 23 November 2026.

`entry.png` (1024×1024, PNG) is a newspaper front page: a big
**MONDAY, 23 NOVEMBER 2026** masthead, a lead story on the EU's proposed
3% tax on Big Tech, three more illustrated stories, and an "Also today"
ticker. Every story on it was reported on 23 November 2026 (in at least
one time zone), and each one has its own picture, so the day reads even at
small size. The four illustrations were AI-generated in a flat editorial
style with no text in them; all words are rendered programmatically with
`render.py` (Pillow + DejaVu fonts), so every headline stays crisp and
legible. Re-run it to regenerate `entry.png`:

```sh
python3 render.py
```

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png` and verifies the copy byte for byte (PNG signature,
IHDR dimensions, IEND chunk, sha256), so both grading runs write
identical bytes.

## The stories

**Lead — EU unveils 3% tax on Big Tech to fund its next budget**
(illustrated): Council chief António Costa's draft cuts €204bn from the
plan and taxes digital giants, ahead of a leaders' summit next week.
(AFP / Reuters, 23 Nov 2026)

**Bangladesh — Nearly 30 homes torched in political violence**
(illustrated): Houses of Awami League leaders set ablaze in Narail
village; security stepped up. (23 Nov 2026)

**Portugal — Thousands march in rain over living costs**
(illustrated): Unions demand higher wages and cheaper housing in Lisbon.
(Reuters, 23 Nov 2026)

**Baltic Sea — Russian cargo ship still burning off Finland**
(illustrated): The Sparta II was hit by drones on Saturday; its 16 crew
took to lifeboats as it drifted into Finnish waters. Finland says Ukraine
was likely behind the attack. (Reuters / Finland coast guard, 23 Nov 2026)

**Also today (ticker):** Indonesia factory fire toll rises — 7 bodies
found, 50 missing · Myanmar calls ASEAN move "unfair" · South Korea's
education minister quits in AI-cheating scandal.
