# Simplified Chinese typography polish

These completed Simplified Chinese changes are unchanged. The Traditional Chinese
first pass reuses the same compensation, wrapping and compact key labels with
separate regional fonts; see [its notes](TRADITIONAL_CHINESE.md).

## Changes

- Chinese title Oswald glyphs/advances now compensate the engine's .628 horizontal
  multiplier, matching the compensation already used for Chinese. Latin is no
  longer doubly condensed beside natural-width Chinese. Oswald's face, weight,
  height and baseline remain; stock-language fonts and engine role scales do not change.
- Existing HTML and plain multiline-control wrapping now prefer legal Chinese
  character boundaries in ChineseSimplified only. Closing punctuation stays with
  preceding text, opening parentheses stay with following text, and Latin tokens
  stay intact where they fit. HTML also reserves room for closing punctuation
  immediately following a link/span. This fixes observed Combined Arms diary
  commas and the split `Everon`, without editing its authored text or HTML.
- Chinese binding labels use standard `PgUp` / `PgDn` keycaps, avoiding the narrow
  alternate cell's six-character `Page U` / `Page D` truncation. Binding identities
  and all eight stock-language labels are unchanged.

Only `font/cwr_title.ttf` was rebuilt; its 8,228-codepoint coverage and CJK metrics
are unchanged. The other four fonts, their Latin styling and all font licenses
are unchanged. `font/build_font.py --role title` reproduces this asset from the
hash-checked sources in `font/NOTICE.md`; required text now reads the actual
ChineseSimplified CSV column. Deploy the title to the existing mod's
`Fonts/ChineseSimplified/cwr_title.ttf` and use the rebuilt client. No new deployment
layout, translation CSV edits, commercial-asset edits or mission-logic changes.

## Actual-game checks

Rebuilt GL33 client with isolated GOG Remastered 3.05 data and test profiles:

- 1280x900: main menu, settings/bindings, campaign and standalone selection;
  Combined Arms plan/objectives, diary/tactical notes, ten-person roster, gear,
  live truck dialogue/HUD and a **forced** `end1` debriefing (not an earned finish).
- 1280x900: editor and unit-properties dialog; local multiplayer browser,
  Everon Sector Control selector/lobby; Bomberman notes, map and M16 encyclopedia
  description reached through its actual gear-info link. No online/second client.
- Plain hint dialog: reused the existing Combined Arms diary text as a temporary
  harness-injected hint (HTML removed for this check), retaining explicit breaks.
  Its Chinese/Latin text, punctuation, height and Continue button render correctly;
  this was a UI test, not a newly authored or naturally triggered mission hint.
- 1920x1080: Chinese main menu, Combined Arms title/diary/objectives and Resistance
  campaign selection; live English/French briefing switching restores stock text,
  title proportions, fonts and wrapping. No-mod English main menu and Bomberman
  briefing/group/map comparison also remain stock.

No missing glyphs, mojibake, new clipping or baseline regressions appeared in
these checks. The original control sizes, scrolling, font hierarchy and authored
line breaks remain. This is representative QA, not a full campaign/screen replay.

## Validation and limits

Client/core/normal UI builds pass. Focused wrap/font-mapping/binding tests:
23 cases / 173 assertions pass, including Chinese punctuation/link reservation
and all-eight-language binding isolation. Core excluding external-data:
826 cases / 6,373 assertions pass; four game-data scans skip.
All five localization validators and terrain/wizard/MP/UI deployment checks pass,
including font coverage, stock columns, protected references, deployed equality
and original commercial input hashes. This is not a full-suite claim; the earlier
documented missing external UI fixtures are not repaired here.

The boundary rule is deliberately small, not a full Unicode typesetter. Explicit
authored breaks and tokens wider than a whole control can still require local QA;
long arbitrary profile names and other key names retain stock clipping/marquee
behavior. No baseline/letter-spacing redesign was justified by the checked screens.
The separate final terminology/content/punctuation QA is now complete; its
Chinese-only long-identity heading fix and checks are recorded in
[the localization README](README.md#final-simplified-chinese-content-qa).
