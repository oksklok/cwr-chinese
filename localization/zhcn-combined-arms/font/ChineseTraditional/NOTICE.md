# Traditional Chinese font notices

The five modified `CWR ZhTW Title/Body/Mono/Serif/Hand` faces use the SIL Open
Font License 1.1 in [../OFL.txt](../OFL.txt). These renamed derivatives do not
claim endorsement. Original Latin contributors, their notices, input hashes
and existing title-width compensation remain as recorded in [../NOTICE.md](../NOTICE.md).
No Simplified Chinese or stock font asset was changed.

| Role | Traditional Chinese contributor | Weight |
| --- | --- | --- |
| Title | Noto Sans TC | Bold 700 |
| Body / mono | Noto Sans TC | Medium 500 |
| Serif | Noto Serif TC | SemiBold 600 |
| Hand / diary | Iansui | Regular 400 |

- [Noto Sans TC source/OFL](https://github.com/google/fonts/tree/main/ofl/notosanstc):
  Copyright 2014-2021 Adobe, Reserved Font Name 'Source'. Download
  `NotoSansTC[wght].ttf` as `NotoSansTC.ttf`.
  SHA-256 `864727D210D54F2537BBE23B3A839436C3992AF72DE9322AF5270897246BD44F`.
- [Noto Serif TC source/OFL](https://github.com/google/fonts/tree/main/ofl/notoseriftc):
  (c) 2017-2024 Adobe in the font; the accompanying OFL additionally records
  Copyright 2012 Google Inc. All Rights Reserved. Download
  `NotoSerifTC[wght].ttf` as `NotoSerifTC.ttf`.
  SHA-256 `0077E18F57C6908F4A000969880940BDB0DAD057C0E8D98B49DC364C3D1B09C6`.
- [Iansui source](https://github.com/ButTaiwan/iansui),
  [Google Fonts source/OFL](https://github.com/google/fonts/tree/main/ofl/iansui):
  Copyright 2025 The Iansui Project Authors in the downloaded font; its OFL
  records Copyright 2022 The Iansui Project Authors. Download `Iansui-Regular.ttf`.
  SHA-256 `6E6340D80D618A42B48ADE9370C34FA37A8210750C6FBC8EFE65F23716538A2B`.

Fonts retain original Latin outlines/advances and vertical metrics, including
the existing Chinese-only compensated Oswald title. CJK widths use the same
inverse engine role scales as Simplified. Taiwan-region sources supply regional
glyph forms. Subsets cover the actual Traditional corpus and punctuation, not
all Big5/pan-CJK or arbitrary user text. The diary's 林鷚 needs a single 鷚 glyph
from Noto Sans TC Medium because Iansui lacks it. Each face also retains the
existing corresponding Simplified 简 glyph to display the raw 简体中文 picker
autonym; the SC source/contributor notices in ../NOTICE.md apply to that glyph.
These fallback contributors are also recorded in the generated font name tables.

The Taiwan editorial pass extended only the Traditional subsets for ten newly
required characters: 史契棧檻甘薯訂迺邱鈴. All 4,272 existing non-CJK glyph
outlines/advances and role vertical metrics match the previous Traditional fonts;
the Simplified fonts remain byte-identical. Contributors and weights are unchanged.

Reproduce with fontTools 4.66.1 and the three hash-checked sources above:

The consolidated linguistic corrections add the required glyphs
俐兮凡叉帆懈拚搏撇擒攬簣膨酷駁 to the Traditional subsets. Existing glyph
outlines, advances, font roles and vertical metrics are preserved. The builder
reads the Chinese-only master directly; reconstructed CSV fixtures are optional.

```text
python localization/zhcn-combined-arms/font/build_font.py SOURCE_DIRECTORY game-local/Remastered/fonts --language ChineseTraditional
```

Keep the existing Simplified fonts available for the picker glyph. Deploy only
the final five TTFs to `@zhcn-prototype/Fonts/ChineseTraditional/`; sources and
temporary intermediates stay local. The font license does not license game assets.
