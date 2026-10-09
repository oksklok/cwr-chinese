# Font notices and sources

All five `cwr_*.ttf` files are modified fonts distributed under the SIL Open
Font License 1.1 in [OFL.txt](OFL.txt). Their new internal family names are
`CWR ZhCN Title`, `CWR ZhCN Body`, `CWR ZhCN Mono`, `CWR ZhCN Serif`, and
`CWR ZhCN Hand`. These names do not claim endorsement by the original authors.
The OFL does not license the game's other assets or the campaign translation.

## Chinese contributors

- Noto Sans SC: Copyright 2014-2021 Adobe (http://www.adobe.com/),
  with Reserved Font Name 'Source'.
  [Google Fonts source](https://github.com/google/fonts/tree/main/ofl/notosanssc).
  Download `NotoSansSC[wght].ttf` as `NotoSansSC.ttf`.
  SHA-256: `A3041811A78C361B1DE50F953C805E0244951C21C5BD412F7232EF0D899AF0DA`.
- Noto Serif SC: (c) 2017-2024 Adobe (http://www.adobe.com/), as recorded in the
  downloaded font; the Google Fonts OFL file additionally records
  Copyright 2012 Google Inc. All Rights Reserved.
  [Google Fonts source](https://github.com/google/fonts/tree/main/ofl/notoserifsc).
  Download `NotoSerifSC[wght].ttf` as `NotoSerifSC.ttf`.
  SHA-256: `050080D9255A86808F2945BFFAC582B31EF32BC36411CE29563B4961670C66F9`.
- LXGW WenKai: Copyright 2021-2026 LXGW (https://github.com/lxgw/LxgwWenKai).
  Copyright 2020 The Klee Project Authors (https://github.com/fontworks-fonts/Klee).
  [Version 1.522 source and OFL](https://github.com/lxgw/LxgwWenKai/tree/v1.522).
  [Medium TTF](https://github.com/lxgw/LxgwWenKai/releases/download/v1.522/LXGWWenKai-Medium.ttf).
  SHA-256: `D4BDEB38A39151D74D084CBA5090F8CB7D20BF83EEDB78C35939AE70B9F4E3F6`.

## Latin contributors

The original role fonts supplied with GOG Remastered 3.05 contain OFL 1.1
license declarations in their name tables. Their non-CJK glyphs are retained
in the corresponding modified font, not redistributed as separate originals.

- Title / Oswald: Copyright 2016 The Oswald Project Authors
  (https://github.com/googlefonts/OswaldFont).
  Original `cwr_title.ttf` SHA-256:
  `3651C7B0D540D412A536320E1AB296DAEB254DB20FA38BD33B186FF9BF1657FE`.
- Body / Roboto: Copyright 2011 The Roboto Project Authors
  (https://github.com/googlefonts/roboto-classic).
  Original `cwr_body.ttf` SHA-256:
  `CB244F96329B3504D7C198206A0B4FF1660FAFB63882D9C211A1785D7083F424`.
- Mono / UnuarangaKuriero (renamed Courier Prime):
  Copyright (c) 2015 Quote-Unquote Apps. Reserved Font Name: Courier Prime,
  as recorded in its license name entry.
  Original `cwr_mono.ttf` SHA-256:
  `C74CA4DC965B2F791483A43C4ABD3B6B270B761C34DFE1B91FE2A038DD3A1DE7`.
- Serif / Vollkorn: Copyright 2018 The Vollkorn Project Authors
  (https://github.com/FAlthausen/Vollkorn-Typeface).
  Original `cwr_serif.ttf` SHA-256:
  `CC431374627239BCD1F7D1D82E45D0FE49867A81946A31289C17D43001AB1CAA`.
- Hand / Caveat: Copyright 2014 The Caveat Project Authors
  (https://github.com/googlefonts/caveat).
  Original `cwr_hand.ttf` SHA-256:
  `ED12CEEB807081B63CD13B0580F3C734D1C04E7BBF8DC9525B1AF8281C2E6CE0`.

## Reproduction and modifications

Use Python with fontTools 4.66.1:

```text
python build_font.py SOURCE_DIRECTORY game-local/Remastered/fonts
# Rebuild only the title role:
python build_font.py SOURCE_DIRECTORY game-local/Remastered/fonts --role title
```

Only the three source files above are needed in SOURCE_DIRECTORY. The helper
checks their hashes and those of the installed originals. Sources and temporary
build files are not committed. Only the five finished fonts are shipped.

Chinese selections cover the 6,763 GB2312 Han characters, ChineseSimplified CSV values, and
common CJK punctuation; these are not complete pan-CJK fonts. Noto Sans is
instantiated at 700 for title and 500 for body/mono; Noto Serif at 600 for serif;
WenKai uses its Medium face (OS/2 weight 500; its style name says Regular).
Original Latin weights are respectively
700/700/700/700/600. Roboto's width axis is frozen at its existing default 100.
This default instancing rounds 23 original side bearings by at most one font
unit, without changing advances.

Chinese outlines and advances are scaled horizontally by the inverse of each
role's stock engine width multiplier: title 1/.628, body 1, mono 1/.8,
serif 1/.935, hand 1/1.05. The Chinese-only title asset also scales Oswald's
outlines/advances by 1/.628, removing the additional engine squeeze beside natural-
width Chinese while retaining Oswald's condensed face, weight and baseline.
The other four roles retain original non-CJK outlines/advances. All role vertical
metrics are retained relative to the originals' static default instances.
Fonts are merged, renamed, and stripped of unused CJK
layout/variation data. Font role multipliers and UI sizes are unchanged; stock
languages still load the unmodified stock fonts. See ../TYPOGRAPHY.md for the
separate Chinese-only wrapping and key-label changes.
