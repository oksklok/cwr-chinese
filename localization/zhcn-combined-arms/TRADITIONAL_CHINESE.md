# Traditional Chinese (Taiwan)

Selectable **繁體中文 / ChineseTraditional / zh-TW**, independent of Simplified,
with English fallback and voices. Phase 3 editorial review and representative
final content QA are complete. This is not a claim of exhaustive playthroughs.

## Coverage and wording

217 tables now contain 11,148 Traditional cells, including the retained 27-cell
Combined Arms mirror and one canonical-only identity cell. Excluding those,
there are 11,120 authored/display cells. Every existing ChineseSimplified and
eight-stock-language cell, ordered key, HTML tag/link and line-break token is
unchanged by the editorial pass. Canonical-only identity metadata stays canonical.

| Content | Traditional cells |
| --- | ---: |
| CWC: 78 mission/support folders and root | 1,928 |
| Resistance: 39 folders/root | 1,310 authored + 1 canonical |
| Standalone: 24 missions | 1,284 |
| Authored multiplayer: 30 missions | 1,511 stock + 27 display |
| Wizard: 36 templates | 2,198 |
| Shared UI/equipment/editor/terrain/generated/campaign metadata | 2,862 |
| Combined Arms retained mirror | 27 |

The finished Simplified master supplied meaning and project conventions.
[OpenCC](https://github.com/BYVoid/OpenCC)'s `s2twp` conversion, through
`opencc-python-reimplemented` 0.1.7, supplied the draft, followed by a targeted regional pass,
contextual checks and runtime review. It is a draft aid, not a new historical
translation source; conversion scripts are not shipped or required at runtime.

Reviewed conventions include 戰車/反戰車, 飛彈/巡弋飛彈, 砲兵/機砲/砲彈,
導引, 雷射, 彈匣; 選單/設定/預設, 儲存/讀取, 檔案/資料夾, 滑鼠,
伺服器/網路/區域網路/頻寬/埠, 螢幕/影像 and 任務精靈. 計畫 replaces
計劃; quotation marks use 「」/『』. The Combined Arms diary's “first time
under fire” means 首次面對槍林彈雨, not being hit by a bullet. 影像設備桌 is
equipment, not a software-video reference. The SC wording is deliberately frozen.

Names include 大衛·阿姆斯壯, 維克多·特羅斯卡, 羅伯特·哈默,
山姆·尼科爾斯 and 詹姆斯·加斯托夫斯基. Established place-name transliterations,
62 terrain labels and bilingual exceptions are retained in Traditional form.
Compact A小隊/B組/Y排 and semantic 熊爸爸/鷹眼 callsigns remain. Model numbers,
coordinates, technical identifiers and user/profile names stay intact.
`STR_CWRC_IDENTITY_VIKTOR_CANONICAL` remains **Victor Troska**, never display text.

### Completed editorial review

Read the Traditional prose across all content categories, including narrative,
dialogue, encyclopedia descriptions and repeated template/UI text; consulted the
installed English source where meaning was uncertain. Conversion was not rerun.
352 existing Traditional values were corrected: CWC 90, Resistance 35,
standalone 49, multiplayer 22, wizard 10, shared tables 145, mirror 1.

- Contextual repairs include Bomberman's 全幹掉, 幹得很好, 的士兵 (not
  計程車兵), 重裝甲 (not 重灌甲), 第一項目標 and radio 代碼 (not 程式碼).
  Physical passage uses 通過; via/through-a-means uses 透過. Correct 乾杯,
  乾淨, 乾脆 and 干擾 were retained after contextual review.
- Taiwan usage includes 醫護兵, 滅音, 刺針, 阿帕契, 契努克, 公車,
  機車, 馬鈴薯, 規格, 品質, 貼圖, 影格率, 更新率, 自訂, 套用,
  控制器, 類比, 唯讀 and network 位址. Dialogue uses natural 哪裡/這裡
  forms without rewriting already-good sentences. News uses 報導/消息;
  radio/software messages retain 訊息 where appropriate.
- Contextual proper-name repairs include 加布里埃爾, 傑里 and 帕托奇卡;
  historical references use 雷根, 甘迺迪, 邱吉爾 and 史達林. Existing
  project character/place spellings and formation policy remain intact.
- A missing existing controller key, `STR_DISP_OPT_CTL_GAMEPAD_REVERSE_Y`,
  now displays 反轉 Y 軸. Its Simplified wording is reused; every stock column
  retains the exact previous English fallback, `Y-axis inversion`.
- The HK encyclopedia title was shortened to `HK MP5SD6 滅音型` after an
  actual orphaned 槍 was observed. The subtitle and body retain its weapon class.

Follow-up: removed callsign-conversion whitespace in exactly 12 Traditional
values: authored Shadow Killer 4, standalone Shadow Killer 4, Heli Train/Heli
Train 2 one each, War Cry 2. 劍魚基地、螢火蟲基地 and 大天使 now join the
surrounding Chinese naturally. Every Simplified/stock cell and all other syntax
remain exact; five validators and four deployment checks pass. Four loose tables
were redeployed and the recognized Shadow Killer mod bank regenerated locally
(prior bank retained in `traditional-spacing-banks`). No fonts/engine changes or
additional physical game testing were needed for this whitespace-only correction.
Phase 3 remains complete.

## Mechanism, fonts and deployment

The existing mod `CfgLanguages` registers a separate UTF8 language, zh-TW aliases,
`voice=0`, English fallback and `Fonts/ChineseTraditional`. Normal settings persist
`textLanguage="ChineseTraditional"` independently of `voiceLanguage="English"`.
The eight stock languages remain stock; disabling the mod removes both Chinese
registry entries. Automatic Windows primary-language selection remains conservative.

Five separate regional hybrid fonts use Noto Sans TC 700/500, Noto Serif TC 600,
and Iansui Regular 400. Latin styling and line metrics match the existing Chinese
roles. See [font notices, hashes, two glyph fallbacks and reproduction](font/ChineseTraditional/NOTICE.md).
Only three existing UI language conditions were extended to Traditional: plain
and HTML Chinese wrapping, and narrow PgUp/PgDn binding labels. No new layout,
font system, identity logic, mission scripts, audio or commercial asset changes.

Use [README manual deployment](README.md#deployment-and-reversal), including the
new five-font directory; copy all bilingual tables/config metadata and run the
same four builders. Existing generated banks must be checked against their prior
supported source before retirement/regeneration; builders intentionally refuse
unrecognized output. This installation's recognized prior banks were archived in
`game-local/localization-backup/traditional-first-pass-banks` and its two reviewed
successors in `traditional-reviewed-banks`. Stock backups were not overwritten.
This editorial pass archived 21 recognized changed banks in
`game-local/localization-backup/traditional-editorial-banks` before regeneration.
Original GOG executable/PBOs/base fonts are unchanged. Reversal is unchanged:
disable/remove only patch-owned overlays and restore loose files from original
hash-checked inventories when complete asset reversal is desired.

## First-pass representative physical checks

Rebuilt GL33 client with isolated GOG Remastered 3.05 data/profile, 1280×900:

- Main/menu language picker, settings, normal exit/restart: Traditional persists,
  voice language remains English. Live TC ↔ SC ↔ English ↔ French works; stock
  text/fonts return. Missing/empty translation English fallback is regression-tested.
- CWC Combined Arms: title/identity, plan/objectives, diary, opening natural M16A2
  dialogue and HUD. A real in-mission `marker:Regina` link hit-test/click routed
  successfully; precise map recentering was not separately measured.
- Resistance Crossroad: briefing/objective, Nogova 多利納 map label, display name
  and choice actions; authored Tasmania dialogue caption invoked via the diagnostic
  `say` path rather than claiming a naturally reached full cutscene. Script `name
  player` remains David Armstrong / Victor Troska in their respective missions.
- Bomberman: selector/title, composed briefing/objectives/marker labels and gear;
  M21 encyclopedia full description and image via its in-mission info link.
- Editor: map/buttons, 新增單位 dialog, rank/equipment/control labels; canceled
  without saving an authored mission.
- Generated Clean Sweep on Everon: wizard selection, generated briefing/objective,
  勒穆勒 terrain label and live M16 HUD/gameplay. No entire generated mission finish.
- Authored Shadow Killer on Malden: selection, local-host role lobby, briefing,
  杜爾當 terrain label, objectives and live HK HUD/gameplay. No online/second client.
- No mod: English main menu and Bomberman briefing/group/markers use stock text/fonts.

No missing-glyph boxes, mojibake or new clipping appeared in these samples. Font
coverage is static across every Traditional cell, not merely sampled screens.
The lighter Iansui Regular diary face is readable; it is intentionally not a
fake Medium face. Dense stock mission-marker/map-label overlap is not redesigned.

## Editorial-pass physical checks and validation

Rebuilt GL33 client with isolated GOG 3.05 data at 1280×900:

- Bomberman selector, composed briefing/objectives/map and HUD; corrected 全幹掉
  radio text rendered with its English voice, invoked diagnostically through
  `sideRadio`, not claimed as a naturally earned convoy outcome. An actual
  briefing marker-link hit-test/click dispatched `marker:Start` successfully.
- CWC Rescue intelligence page: corrected 重裝甲, long text and generated
  identity. Resistance Counterattack diary/plan: corrected LAW 火箭筒的士兵,
  objectives and character identity. No missing glyphs or new clipping observed.
- HK MP5SD6 and Stinger encyclopedia prose/images/specifications. The observed
  HK title orphan was fixed and physically retested; the shorter title fits.
- Display/control settings and controller tuning: 更新率/長寬比/套用,
  控制器/類比 and the previously missing 反轉 Y 軸 label.
- Live Traditional → Simplified → English → French → Traditional on the same
  controller screen: fonts/text switch correctly; stock wording remains intact.
  The new controller key retains the previous English fallback in French too.
  Voice language stays English. No-mod English main menu and Bomberman briefing,
  groups and markers remain stock.
- Authored Return to Eden local selection, role lobby and composed briefing/map
  checked. See the inherited source defect below; its buried corrected objective
  wording was not separately verified on-screen. No second client or match finish.

All five localization validators and four deployment checks pass. The final before/after
audit preserves every SC/stock cell plus extras and ordered keys, verifies the
byte-identical Combined Arms mirror and unchanged SC font files. The five TC
subsets gained ten genuinely missing glyphs (史契棧檻甘薯訂迺邱鈴); 4,272 existing
non-CJK outlines/advances and all vertical metrics match the prior TC assets.
Client/core and UI test builds pass; focused language/config/stringtable/
identity checks: 60 cases/309 assertions; wrap/font/bindings/settings: 24/189;
existing stock CSV regressions: 3 passed. Full external-data UI suite was not rerun;
its previously documented absent Remaster fixtures are not claimed as passing.

No known actionable Taiwan wording issue remains after the complete review.
**Inherited stock-content limitation:** Return to Eden's
`STR_3_9_C_RETURNTOEDEN_EDEN_BRIEFING_OBJ_1` through `_OBJ_4` include accumulated
intelligence/plan HTML in the hash-verified installed English source. The actual
briefing repeats these blocks and pushes objectives down; embedded source newlines
also produce occasional intra-sentence spaces. Existing Simplified and stock
columns contain the same structure. Their HTML and line-breaks were deliberately
not rewritten under this pass's preservation contract. This is not a Traditional
conversion defect; fixing the shared stock-shaped fragments is a separate bounded
content repair, not a claim that the original experience is flawless.

No full campaign/multiplayer endings, exhaustive dialogs, 1920×1080 pass or arbitrary
user-name glyph coverage is claimed. The existing 11 standalone stock audio references
without source captions remain; no invented captions. Distribution is not started.
