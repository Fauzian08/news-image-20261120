# The World in One Day — Friday 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Fauzian08/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Fauzian08/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

One image summing up the world's news of Friday 20 November 2026: 21 stories
from 6 regions, three large illustrated lead cards, a world map, an
hour-by-hour timeline, every story tagged REPORTED / CLAIM / FORECAST, and a
DATE CHECK strip that names the 19 November stories it excludes.

Built for [make.fun](https://make.fun)'s news-image-20261120 bounty.

## How it is made

`draw.py` renders `entry.png` (1024×1024) with Pillow: shapes and text only,
no network, no external images. `main.py` (standard library only) copies
`entry.png` to the output directory, so the graded program needs no Pillow.
