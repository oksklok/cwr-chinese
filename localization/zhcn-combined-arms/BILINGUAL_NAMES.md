# Selective bilingual-name retirement

The installed GOG Remastered 3.05 Chinese terrain overlay is now the navigation
reference for covered towns. The source of truth is the actual **62-entry**
[locally reconstructed `stringtable_terrain.utf8.csv`](distribution/payload.json), not merely
the prose glossaries: Everon/Eden 18, Malden/Abel 14, Nogova/Noe 30;
Kolgujev/Cain has no stock town entries.

## Reviewed changes

Reviewed geographic references across both complete campaigns (including their
root/support tables), all 24 standalone missions, the shared global overlay and
the Combined Arms mirror. Remove only `（Latin Name）` following an established
Chinese town spelling whose built-in label is confirmed on that mission's island.
Briefings, objectives, diary/intel, visible labels, dialogue/destination replies,
overviews and debriefings all follow the same coverage decision.

| Scope | Changed values | Changed tables |
| --- | ---: | ---: |
| CWC / 1985 | 144 | 28 |
| Resistance | 26 | 13 |
| Standalone | 70 | 17 |
| Shared global overlay | 0 | 0 |
| Combined Arms prototype mirror | 4 | 1 |

The mirror remains byte-identical to the campaign table; its four values are not
additional campaign keys. All other wording, Chinese spellings, spacing, keys,
row order, placeholders, HTML attributes/links, marker IDs, coordinates and
literal line-break tokens remain unchanged. The stock `Saint Phillippe` label
and prose `Saint Philippe` identify the same Everon town, 圣菲利普; this is the
only spelling alias needed for this review. No new geographic mappings added.

## Intentional bilingual references

- **洛利斯（Lolisse）**, Malden: absent from the 14 built-in town labels. Keep
  route/target/convoy references even where a particular mission offers a marker;
  those mission-specific markers are not a general terrain-name replacement.
- **诺瓦韦斯（Nová Ves）**, Nogova: absent from the 30 entries. Hostages' diary
  names this place, whereas its dialogue names covered 维尔卡韦斯 (Velka Ves).
  Do not equate the two or rewrite the plot. Velka Ves can be Chinese-only.
- **基乌斯克（Kiusk）**, Kolgujev: no stock town labels at all; Ground Attack II's
  useful convoy-origin reference stays bilingual. No Cain table changed.
- **艾弗隆（Everon）／艾弗隆岛（Everon）、马尔登（Malden）、科尔古耶夫
  （Kolgujev）、诺戈瓦（Nogova）**: island-level and cross-island references are
  not covered by town labels. Retain existing bilingual navigation references;
  already-Chinese routine dialogue and short titles remain unchanged.

Bases/landmarks qualified by a covered town can drop that town's suffix (for
example 莱维附近的基地); no base, region or landmark itself is renamed.
Unrelated Latin models, characters, callsigns, key labels and technical text stay.

## Validation and actual-game checks

All three existing localization validators pass after local deployment: folder/
key coverage, order/case, UTF-8, references/placeholders, HTML/link targets,
caption repairs, five-font coverage and deployment equality. A disposable audit
compares every pre-pass row against precisely the approved same-island suffix
removals, including unchanged rows/other columns and mirror equality. No new
validator or shipped tooling was added.

The terrain builder's `--check` passes all 62 entries, five font cmaps, stock input
hashes, generated-overlay equality and name-only asset preservation. The terrain
CSV, generated overlays and fonts are unchanged. Existing validators also verify
7,461 unrelated installed files unchanged, including scripts, HTML, executable,
audio and lip-sync. The 11 pre-existing untranscribed standalone references remain
stock; this pass does not invent captions.

Fresh direct launches of the installed `PoseidonGame.exe`, GL33, 1280x900 window,
English mode with `@zhcn-prototype` (including terrain overlays) and the isolated
`game-local/test-profile`; stock editor **Preview** followed by the real in-mission
map/briefing, not campaign progression or a complete playthrough:

- **CWC Combined Arms, Everon:** Chinese-only 雷吉纳 plan/objective and matching
  built-in 雷吉纳 label; other Chinese town labels and original mission markers.
- **CWC Pathfinder, Malden:** Chinese-only 沙普瓦/圣玛丽 briefing and objectives,
  matching terrain labels; target markers, unit icons and zoom remain functional.
- **Resistance Occupation (10a), Nogova:** Chinese-only 米罗夫 briefing reference
  and objective, matching built-in 米罗夫; original castle/base/support markers.
- **Standalone Ground Attack (04), Malden:** Chinese-only 拉特里尼泰 in the plan,
  matching terrain label; objectives, helicopter/route markers and surrounding
  Chinese towns. Its convoy objective visibly retains **洛利斯（Lolisse）**.

No missing glyphs, mojibake or new text clipping observed. Original hard line
breaks and punctuation wrapping remain (e.g. a comma on the next line after a
Pathfinder/Ground Attack objective link); no layout/HTML edits were made.
Existing marker-to-town overlaps and map gadget/edge occlusion remain stock.
Other resolutions and every individual town were not manually retested.

**Successful marker-link clicking remains unverified.** A fresh exact-window
pointer-position attempt over Combined Arms' 雷吉纳 link did not reliably move
the game's internal UI cursor, so no successful link activation is claimed.
All link targets and marker definitions remain statically verified unchanged.
Tests stayed muted, the original audio state/Caps Lock were restored, and all
test game processes were normally closed.

## Deployment boundary

CSV deployment/reversal is unchanged; see the main README and campaign/standalone
reversal inventories. **Deploy the generated Chinese terrain overlays as well as
these CSVs**: town references now rely on them. Supported inputs remain the exact
GOG 3.05 hashes; other versions/third-party worlds/config-replacing mods are not
newly validated. No commercial config/PBO bytes are committed or redistributed.

No engine/UI source, fonts, terrain definitions, mission logic, audio/lip-sync,
validators or shared global strings changed. The next roadmap item is generated/
hardcoded English; it was not started here.
