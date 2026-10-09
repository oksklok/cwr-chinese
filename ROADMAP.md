# Chinese localization roadmap

- Current milestone: Phase 3 complete; Phase 4 Windows local release candidate implemented and tested
- Current work: practical existing-installation RC2; exact-installer acceptance in progress
- Next task: finish RC2 acceptance, then final public source/license/notice review and release documentation
- Known blockers: public-release review/publication gates remain; Steam runtime acceptance still pending
- Do not forget: inherited stock Return to Eden briefing defect, redistribution audit and exact public-artifact testing

This is the source of truth for remaining localization work. Follow the phases and checklist order below.

## Completed milestones

- [x] Cold War Crisis (CWC / 1985) fresh retranslation from current Remastered English.
- [x] Resistance campaign translation.
- [x] All 24 official standalone missions translated.
- [x] All 30 official authored multiplayer missions: 1,511 stock keys and 27 localized literal-display keys, preserving other languages.
- [x] Current 2,706-key shared stock global Chinese overlay, plus generated-name/UI metadata.
- [x] Current hybrid Chinese fonts, preserving Latin styling.

## Phase 1 — Simplified Chinese text completion

- [x] Clean up functional NATO/unit designators across CWC, Resistance and standalone missions: Alpha/Bravo/Charlie → A小队/B小队/C小队; choose 组/小队/排 by context. Keep semantic callsigns such as 熊爸爸 translated normally.
- [x] Standardize mixed CJK/Latin spacing: 前往 Ff52、HEAT 破甲弹、M16A2 步枪; keep unit designators joined: A小队、B组、Y排.
- [x] Investigate and localize built-in terrain-map place-name labels: 62 labels on Everon/Malden/Nogova via local-only stock-derived mod overlays; Kolgujev has no stock town labels. See localization/zhcn-combined-arms/terrain/README.md for generation, compatibility and test limits.
- [x] Retire redundant 中文（Latin） town names where the same island's Chinese terrain labels are confirmed; retain useful island/unlabelled-place references. See localization/zhcn-combined-arms/BILINGUAL_NAMES.md.
- [x] Localize configured identities such as David Armstrong, generated group labels such as Alpha 8, and the Resistance... category without changing identifiers or stock fallbacks. See localization/zhcn-combined-arms/GENERATED_NAMES.md for rebuilt-client requirements and remaining limits.
- [x] Finish residual-English/global coverage: UI/encyclopedia, all 36 wizard templates and all 30 authored multiplayer missions; runtime literal audit and representative populated roster/editor/profile/connection/debriefing/marker-link checks passed. See localization/zhcn-combined-arms/RESIDUAL_UI.md for intentional exceptions and bounded test limits.

## Phase 2 — Simplified Chinese language and presentation

- [x] Add proper Simplified Chinese language support instead of using the English column: selectable 简体中文, persisted text selection, English fallback and runtime switching. See localization/zhcn-combined-arms/LANGUAGE_SUPPORT.md.
- [x] Verify other languages remain stock and unaffected: all eight original columns validated; English/French live checks and stock English without the mod.
- [x] Add Chinese-specific font routing: the existing five faces load only for ChineseSimplified; stock-language fonts stay stock.
- [x] Polish mixed CJK/Latin typography: balanced title proportions, Chinese punctuation/Latin-token wrapping and narrow Page-key labels. See localization/zhcn-combined-arms/TYPOGRAPHY.md for representative checks and limits.
- [x] Finish terminology, punctuation, spacing, wrapping and residual-English QA, including representative in-game checks. See localization/zhcn-combined-arms/README.md#final-simplified-chinese-content-qa for corrections, validation and bounded runtime coverage.

## Phase 3 — Traditional Chinese

- [x] Build a complete Traditional Chinese first pass from the finished Simplified Chinese master; selectable 繁體中文 / ChineseTraditional, persistence, English fallback and separate regional fonts. See localization/zhcn-combined-arms/TRADITIONAL_CHINESE.md.
- [x] Review terminology, proper names and wording across the complete corpus; correct contextual conversion errors and Taiwan usage without altering Simplified or stock values.
- [x] Verify corpus-wide font/glyph coverage and representative physical presentation in-game.
- [x] Finish Taiwan editorial review and representative final presentation/content QA. See localization/zhcn-combined-arms/TRADITIONAL_CHINESE.md for corrections, physical checks and inherited stock-content limits; no full playthrough is claimed.

## Phase 4 — Distribution

- [x] Establish the initial licensing audit and local-generation packaging approach. See localization/zhcn-combined-arms/DISTRIBUTION.md for findings, release gates and exact-restoration strategy.
- [x] Implement the Chinese-only payload and local installation/uninstallation core: exact reconstruction, original backups, receipts, rollback, reinstall and user-edit preservation.
- [x] Build the Windows installer/uninstaller wrapper around the tested core: neutral CWRC client, private PyInstaller helper and Inno Setup local RC; not published.
- [x] Add verified clean GOG Remastered 3.05 compatibility/hash/conflict checks.
- [x] Narrow compatibility to required 3.05 sources, preserve extra content/mods, and move standalone localization into mod PBOs.
- [ ] Complete exact RC2 installer acceptance on GOG and the available Steam installation.
- [x] Complete bounded clean-install core runtime acceptance: authored MP lobby/briefing/gameplay, radio live switching and no-mod English; see DISTRIBUTION.md for chat-history and test limits.
- [x] Test the exact local RC wrapper's install/uninstall/reinstall workflow, shortcut launch, user-edit conflict preservation and interruption/retry; exact original restoration verified.
- [ ] Audit redistribution rights, licenses and package contents.
- [x] Move the patch into [oksklok/cwr-chinese](https://github.com/oksklok/cwr-chinese): localization-focused main plus its own pinned client-source branch; no old-fork dependency, release binaries or commercial assets. Public release remains gated below.
- [ ] Finalize README, credits and known limitations.
- [ ] Produce a tagged release ZIP.
- [ ] Test the exact public artifact before giving it to Dad.
