# Resistance / 抵抗力量

Complete campaign-text replacement for the installed GOG Arma: Cold War Assault
Remastered **3.05**. Select 简体中文 text with English voices and the existing
`@zhcn-prototype` mod; see [current language support](LANGUAGE_SUPPORT.md).
Earlier tests below used the English-column prototype. No installer is added.
The patch directory retains its prototype name.

## Coverage and source

Exact installed directory: `game-local/Remastered/Campaigns/resistance`.
`campaign/resistance/` supplies complete replacement main UTF-8 CSVs for all
**39 mission/support folders: 20 numbered playable/branch folders and 19 cutscene,
ending, escape, reward and punishment folders**. Together with the campaign-root
table, there are **40 CSVs and 1,310 keys**: 1,308 original keys plus two
stock-reference repairs. All original keys, casing and order are preserved;
originally empty text stays empty.

Coverage includes campaign/chapter and mission names, cutscene captions,
overviews, plans, objectives, diary/intel pages, marker/waypoint display text,
dialogue and scripted radio, tutorials/hints, debriefings and ending letters.
`description.ext` has four display-name edits and six optional identity
`nameKey` fields from the later [generated-label pass](GENERATED_NAMES.md).
Reverting those display names and stripping only that metadata reproduces the
original file byte-for-byte, including whitespace.

The brief historical-source check found **no usable Resistance Chinese tables**:
TZKdeveloperIF's preserved
[OFP_CWR_Remastered_CHN_Campaigns](https://github.com/TZKdeveloperIF/OFP_CWR_Remastered_CHN_Campaigns)
archive at `d09050e7cdbe0bfa1186ceb654518c70416c1574` contains `1985`, `BTL1` and
`Retailation`, not Resistance. The checked current repository tree likewise had
no Resistance campaign. Its README mentions old Chinese CWC/Resistance material
and 天人互动, but that is not evidence that those missing tables are available.
Limited web searching did not supply a usable translation. This does **not**
claim a historical Chinese Resistance release never existed.

**Zero historical Resistance values were reused.** All 1,308 source keys were
translated directly from the current installed English campaign. CWC has since
also been freshly retranslated; do not attribute either current translation to
天人互动 or TZKdeveloperIF. No rights to redistribute original game assets are
asserted. No audio, lip-sync, mission scripts or HTML templates are included.

## Terminology and geography

Recurring names: 维克托·特罗斯卡 (Viktor Troska), 詹姆斯·加斯托夫斯基
(James Gastovski), 杰罗尼莫 (Geronimo), 加布里埃尔／加布 (Gabriel/Gabe),
斯托扬·亚科蒂奇 (Stoyan Yakotich), 马雷克 (Marek), 古巴 (Guba),
伊日·霍德克 (Jiří Hodek). Dialogue uses suitable shorter forms.
Calls include 狐狸 (Fox), 松鸦 (Jay), 猛虎 (Tiger), 猎鹰 (Hawk),
熊爸爸 (Papa Bear), 雄鹰一号 (Eagle 1), 红熊 (Red Bear), 捕鼠人 (Rat Catcher)
and 塔斯马尼亚恶魔 (Tasmanian Devil). 黑林 (Blackwood) is a base callsign,
not a renamed map location. Weapon/model designations remain Latin.
The later [unit-designator cleanup](UNIT_DESIGNATORS.md) changes five values:
radio option Alpha becomes A, and the Occupation branches' Bravo command becomes
B装甲小队. Semantic callsigns and geographic policy are unchanged.

Navigation-critical references to towns covered by Nogova's terrain overlay now
use Chinese alone, including the hostage-location dialogue's 维尔卡韦斯. Island
names and the unlabelled 诺瓦韦斯（Nová Ves） retain their bilingual navigation
references. See the [selective retirement review](BILINGUAL_NAMES.md); short
titles and routine dialogue/radio continue to use Chinese where appropriate.
Internal markers, HTML attributes/anchors, classes, filenames and keys are never
renamed. Existing shared mappings remain 艾弗隆 (Everon), 马尔登 (Malden) and
科尔古耶夫 (Kolgujev); the source's Kolguyev spelling denotes the same island.

| Latin location | Chinese location | Latin location | Chinese location |
| --- | --- | --- | --- |
| Nogova | 诺戈瓦 | Petrovice | 彼得罗维采 |
| Lipany | 利帕尼 | Dolina | 多利纳 |
| Mokropsy | 莫克罗普西 | Modrava | 莫德拉瓦 |
| Bludov | 布卢多夫 | Velka Ves | 维尔卡韦斯 |
| Nová Ves | 诺瓦韦斯 | Blata | 布拉塔 |
| Mirov | 米罗夫 | Davle | 达夫莱 |
| Neveklov | 内韦克洛夫 | | |

Obvious source misspellings `Morkopsy`/`Morkospsy` are rendered consistently as
Mokropsy. The Hostages dialogue says Velka Ves while its diary says Nová Ves;
these distinct source locations are retained rather than silently changing the
plot. Moscow and the Kremlin use their established Chinese names 莫斯科 and
克里姆林宫. Stock terrain labels are configuration text, not baked map lettering.
The separate [terrain overlay](terrain/README.md) now localizes Nogova's 30
built-in labels; it adds no invented location entries. The selective retirement
pass removes redundant Latin town suffixes from 26 Resistance values, preserving
Nová Ves as distinct from Velka Ves and leaving all other wording unchanged.

## Shared overlay and narrow repairs

The existing partial global table now has **1,094 keys: 99 additions, zero changes
to the prior 995 translations**. Additions cover Resistance addon weapons,
ammunition and equipment (including pistols, 6G30, Kozlice, UZI, FAL, G3 and
Skorpion), vehicles/crew labels, bus/motorcycle, door actions, empty inventory
slots and ending-credit headings, including the shared "presents" caption.
Already translated keys are reused, not
duplicated. Original model designations and credit/person names are retained.

Two original unresolved references are repaired exclusively by supplying text:

- `x01facetoface.noe/intro.sqs` requests `STRD_Dx02t51`; its table only defines
  `STRD_Dx01t51`. An exact-spelling alias supplies 美军特种部队指挥所.
- `x03futureplans.noe/mission.sqm` uses `@STRD_D06n52` for the visible `Hold`
  marker without supplying it. The campaign-root table adds 敌军基地, matching
  the existing Field Exercise key's original "Enemy base" meaning.

Shorter Field Exercise and Fireworks sentences improve the observed narrow-page
wrapping without dropping information or changing HTML tags. No script, marker
identifier, logic, audio, lip-sync, executable, engine/UI source or font changed.
All five existing hybrid fonts already cover the new text; no rebuild occurred.
CWC CSVs/configuration/prototype mirror remain byte-for-byte unchanged.

## Deployment and reversal

The local patch is already deployed. Close the game before copying/restoring.
Use the [existing manual deployment](README.md#deployment-and-reversal), now
covering both campaigns. Keep the mod's absolute path, Remastered working
directory and `--lang English`. A disposable test profile does not replace the
normal player's progress.

Resistance's originals are at
`game-local/localization-backup/resistance-original/`. `reversal.json` inventories
**41 targets** (39 mission CSVs, the shared CSV and `description.ext`), their
original existence and hashes. Forty targets existed; the root
`stringtable.utf8.csv` was absent. The original legacy root `stringtable.csv` is
untouched and separately backed up. `before-hashes.json` records the whole game
before this pass. Never overwrite these originals with deployed Chinese files.

For a fresh installation, back up the corresponding 41 files before deploying,
preserving relative paths and recording absent files. To reverse Resistance,
verify backup hashes and restore each existing target to its exact relative path
under `Campaigns/resistance`. Remove only the newly added root UTF-8 CSV if it
was originally absent; never delete the campaign directory. Restore
`pre-resistance-global.utf8.csv` to the mod's `bin/stringtable.utf8.csv` to reverse
only these global additions while retaining CWC and its fonts. For full reversal,
also follow CWC's separate inventory and launch without `--mod`. Saves are not
removed. Disabling the mod alone does not reverse campaign CSV replacements.

## Validation and representative play checks

From the repository root, with fontTools 4.66.1 available:

```text
python localization/zhcn-combined-arms/validate_campaign.py
python localization/zhcn-combined-arms/validate_resistance.py
```

Both validators pass: complete folder/key coverage, exact case/order, strict
UTF-8, two-column rows without duplicate keys, preserved placeholders/references,
HTML tags/attributes/links, no unresolved literal runtime references in
Resistance, coverage in all five unchanged fonts and deployment equality.
The existing global-key validation now reads only CSV members of four stock
Resistance equipment PBOs, because their keys are absent from BIN's tables.
Compressed-member checksums are verified; no addon assets are extracted or
modified. This is a bounded validation helper, not a localization framework.

**7,563 other installed game files** match their pre-pass SHA-256 hashes,
including all CWC files, executable, fonts, scripts, audio, lip-sync, HTML and
addons. CWC's existing validator also passes its 78 folders / 1,928 keys and
3,706 unrelated campaign-file hashes with the expanded shared overlay.
The new Resistance configuration deliberately preserves original whitespace;
Git's whitespace check flags its pre-existing stock trailing spaces.

Actual-game checks use the installed `PoseidonGame.exe`, English voices,
subtitles enabled, Cadet and an isolated profile at 1280x900:

- Campaign book, early/late mission titles, preview statistics and Chinese
  main/briefing/debrief controls.
- Contact: bilingual Dolina plan/objectives, marker, opening dialogue captions
  and a real success-debrief screen reached with `ENDMISSION`.
- No Turning Back: brief/map, controlled on-foot movement, opening scripted
  radio, weapon HUD and squad command/status menu.
- Field Exercise: vehicle-oriented mission briefing, bilingual port/route
  objectives, markers and on-foot HUD/squad display. Direct unlock does not
  reproduce the accumulated campaign vehicle inventory; no tank-driving test.
  The final route-name wording and translated empty gear slots were rechecked
  after deployment in a freshly launched game.
- Fireworks: plan/objectives/map, diary and working intel/manual links. Both
  reconnaissance and explosives-manual text were displayed in-game.
- Fire Fight: late mission plan, normal in-mission weapon HUD/inventory actions
  and a real success-debrief screen reached with `ENDMISSION`.
- Game Over (`x12gameover.noe`): separately selected with the campaign unlock;
  the ending cutscene ran normally through the closing-letter dialogue captions
  and translated credit headings. This was not earned by finishing Fire Fight.
  The subsequently added shared "presents" label was statically validated, not
  redisplayed through another full ending.

`CAMPAIGN` unlocked the selected missions. Forced debriefs are **not natural
completion claims**; there was no full campaign playthrough. English voice
selection and unchanged audio/lip-sync hashes are verified. Audio was not
independently auditioned: the already-muted device was preserved.

Representative client-only screenshots:
[campaign title](../../docs/zhcn-resistance/campaign-title.png),
[Contact plan](../../docs/zhcn-resistance/contact-plan.png) and
[subtitles](../../docs/zhcn-resistance/contact-subtitles.png),
[infantry radio/HUD](../../docs/zhcn-resistance/defense-radio-hud.png),
[Field Exercise plan](../../docs/zhcn-resistance/field-plan.png) and
[gear slots](../../docs/zhcn-resistance/gear-slots.png),
[Fireworks diary](../../docs/zhcn-resistance/fireworks-diary.png),
[intel](../../docs/zhcn-resistance/fireworks-intel.png) and
[explosives manual](../../docs/zhcn-resistance/fireworks-manual.png),
[late forced debrief](../../docs/zhcn-resistance/firefight-debrief.png),
[ending letter](../../docs/zhcn-resistance/ending-letter.png) and
[credits](../../docs/zhcn-resistance/ending-credits.png).
These are representative observations, not screenshots of every translated key.

## Known limits

- Built-in Nogova map labels are Chinese when the local terrain overlay has
  been generated; unsupported terrain/version combinations remain unverified.
  Baked-in cover/logo art, some engine-generated
  group/character/callsign labels and credit/person names remain Latin. This is
  not a complete game-wide language pack; unrelated settings/editor/multiplayer
  strings and long equipment-encyclopedia descriptions remain outside scope.
- Unused old hardcoded debug captions and commented-out Czech/English script
  text are untouched; active campaign CSV references are translated. Supplying
  Chinese text does not change the script's language-selection behavior.
- No missing glyphs, mojibake or clipping appeared in the tested screens.
  Stock line breaking has no Chinese punctuation rules: leading commas/full
  stops or split parenthesized Latin names can still occur on narrow pages.
  Tested wording was tightened where useful, without modifying fonts or UI.
- All branch transitions, alternate debriefs/endings, equipment carryover and
  long late pages have not been manually exercised. Other resolutions and every
  late scripted line remain unverified live, though statically validated.
