# Context-aware unit designators

Complete visible-value audit of the current Simplified Chinese tables: CWC
(1,928 keys), Resistance (1,310), all 24 standalone missions (1,284), the shared
overlay (1,101), and the retained Combined Arms mirror. Current installed English
and mission formations/radio triggers supplied context; no mission logic changed.

## Convention and scope

- Functional infantry formations use A小队/B小队/C小队/D小队; explicit teams
  can use B组, and platoons use A排/Y排/Z排. Infantry's Alpha squad/platoon
  references describe the same A排; its Bravo team/squad is consistently B小队.
- Context remains significant: Combined Arms has B坦克分队; Houdan's source
  calls its formation Y小队; other explicitly named tank platoons use Y排.
  Supporting formations include G坦克分队, K部队, Z小队, Z坦克分队 and
  F防空分队. War Cry's two-person sniper element uses S狙击组.
- Aircraft use N编队 and member calls N一号/N二号/N长机; Status Quo's
  landing call is C机组. Individual letter-number calls use A一号/A二号/A三号
  or Y一号/Y三号, without inventing a squad for a lone operative.
  Take the Car's lone soldier is A号; Laser Guide's observer is Y号 and the
  supporting aircraft F机组. Hotel infantry become H小队, with H二四号.
- Radio code Alpha becomes 代号 A or A：0-0-1; Code Foxtrot becomes F代码.
  Codes are not formations. No space is inserted inside A小队, B组 or Y排.
- Semantic callsigns (熊爸爸、黑熊、白狼、鹰眼 and others), character/product
  names, spelling jokes and geographic names are untouched. This is not the
  broader mixed-script spacing pass.

Changed values: **292 CWC, 5 Resistance, 115 standalone, 0 globals**; the mirror
has the same **5** changed values as Combined Arms, not five extra campaign keys.
The overlay remains at 1,101 keys. All source-supported caption repairs remain.
Spearhead's support-vehicle radio correctly addresses Y一号 from Z小队 instead
of inventing a Z一号 sender; existing English audio remains unchanged.

## Remaining phonetic words

**No English NATO phonetic words remain in scoped player-facing values.**
Raw CSV searches still find internal key names (e.g. STR_NOVEMBER is the month
十一月) and protected HTML targets such as marker:Bravo, marker:Delta and
#Charlie. These are identifiers, not visible unit names, and must not be renamed.
Bomberman's generated sender headers Alpha 1 / Bravo 1 remain engine-generated,
outside this pass; so do other generated identities/group labels. The original
English voices naturally still speak their original phonetic calls.

## Validation and live checks

All three existing campaign/standalone validators pass: coverage, strict UTF-8,
keys/case, placeholders/references, HTML/links, caption repairs, deployment and
all five unchanged fonts. A disposable audit against the pre-pass commit also
checks exact ordered keys, exact HTML tags/attributes and literal `\n` tokens
across every scoped table; **7,461 non-target installed files** match the pre-pass
SHA-256 baseline. The Combined Arms mirror is identical to the campaign table.

Only validate_standalone.py needs a narrow baseline update: Resistance CSVs
superseded by this pass are checked by validate_resistance.py, while every
campaign non-CSV file remains protected. No validation framework was added.

Actual installed PoseidonGame.exe 3.05 / GL33, existing mod/fonts and isolated
profile, 1280x900: positional installed mission.sqm loads the stock editor,
then its **Preview** runs the mission. No editor save, mission copies, script
changes, campaign progression or debriefing completion are claimed.

- Combined Arms: in-mission map plan/objective show A机械化步兵小队 and
  B坦克分队, with existing bilingual geographic links intact.
- Resistance Occupation (10a): in-mission map shows radio option A：0-0-1.
  The later conditional B装甲小队 command was not triggered.
- Bomberman: plan/objectives and map labels show B小队/C小队; radio menu
  shows their attack commands. Calling B小队 displays the A一号 order and
  B小队 reply; generated Latin sender headers visibly remain stock.

No missing glyphs, mojibake or new clipping observed. Existing narrow-page
punctuation wrapping remains a later QA item. Tests stayed muted; audio/lip-sync
preservation is established by hashes, not listening. Caps Lock was restored.
Other changed lines are statically validated, not individually played.

Subsequently, the [generated-label pass](GENERATED_NAMES.md) localizes the stock
group display-name keys, without changing this authored-text convention. Its
generic group labels use A组/B组 rather than inventing an unknown echelon.

Engine/UI source, fonts, mission logic/scripts, audio/lip-sync, geography and
deployment/reversal architecture are unchanged. Only the localization test
installation received CSV updates; the separate CWR-RR installation was not used.
