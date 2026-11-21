[![The Passport Page of a Country That Isn't There](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![Rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Joppy26/the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![Reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Joppy26/the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

# The Passport Page of a Country That Isn't There

An open passport spread for the **Republic of Skerrya**, a small cold-climate
island republic in the northern sea that does not exist. Its capital is
Veyhavn, a harbour town where the fishing boats come in under the lighthouse,
and every field of the passport is printed in Skerryan and English.

## What the spread shows

**Left page — the data page.** The holder is Ella Maren Vey, born 14 March
1990 in Veyhavn, Skerrya. Her passport (No. SKR 0842173) was issued by the
Harbour Office, Veyhavn, on 12 January 2021 and runs to 12 January 2031.
Beside a drawn line-art portrait sits a two-line machine-readable zone whose
check digits are computed with the real ICAO 7-3-1 algorithm, so the strip
agrees with the name, dates and document number printed above it.

**Right page — visas and endorsements.** Three round trips, all after the
passport was issued and in order: Nordmark (Havnostad) in June 2022, the
Tarn Isles (Port Tarn) in September 2023, and Nordmark again in May–June
2024. Each entry and exit is stamped in its own ink colour, slightly
askew the way a real border stamp lands.

**The telling detail.** Condition 7, stamped in red: the holder may not take
paid work aboard fishing vessels without a permit from the Harbour Master of
Veyhavn, and permits are issued only in the daylight months, April to
September. Under it, a harbour-tax stamp records 40 kr paid at Veyhavn on
the day of issue. That is the kind of place Skerrya is: a working harbour
where the sea sets the rules.

## How it works

`main.py` (Python 3, Pillow only, standard library otherwise) draws the whole
spread in code: the cream pages, the lighthouse emblem, the line-art
portrait, the bilingual fields, the six ink stamps, the condition box and
the MRZ. It uses only the DejaVu fonts already on the machine. There is no
network, no clock and no randomness anywhere, so every run writes the exact
same PNG bytes.

Run it:

```sh
python3 main.py
```

It writes `entry.png` (1024×1024, about 214 KB) to `/output/entry.png`, or to
`$MAKEFUN_OUTPUT_DIR/entry.png` when that variable is set.
