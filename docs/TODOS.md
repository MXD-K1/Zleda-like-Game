# TODOs - 90 Day Playable + Publish Plan

Last updated: 2026-04-29
Scope: finish single-player core, add boss/content loop, ship release build, and implement multiplayer in controlled scope.

> Disclaimer: This file was written by AI

## 0) Non-Negotiable Principles
- Keep game playable at all times on `main`.
- Ship vertical slices early, then scale.
- Stabilize core systems before major feature spikes.
- No new feature enters without save/load + UI + audio hooks.
- Every asset/sound added must have source + license recorded.

## Game Core Decisions (Lock These Early)
- [x] Set working title to `ZeldaGame`.
- [ ] Decide and lock final game name.
- [x] Decide game type: 2D top-down action-adventure RPG. (Locked)
- [x] Decide core mode: single-player first; local co-op optional stretch; pvp later. (Locked)
- [x] Decide target platform: Windows/Linux PC first release. (Locked)
- [x] Decide engine/runtime: Python + Pygame. (Locked)
- [x] Decide camera style: top-down follow camera with smooth damping. (Locked)
- [x] Decide art direction: pixel art. (Locked)
- [x] Decide combat style: real-time melee + magic with dodge timing. (Locked)
- [x] Decide progression model: quest-gated world progression + unlockable abilities. (Locked)
- [x] Decide save model: manual save + checkpoint autosave. (Locked)
- [x] Decide difficulty model: fixed base difficulty, optional assists in settings. (Locked)
- [x] Decide narrative scope: light to medium story with NPC-driven quests (no heavy cutscene dependency). (Locked)
- [x] Decide world scope for v1.0: one overworld + at least one dungeon + one full boss. (Locked)
- [x] Decide session target: 45-90 minute complete playable loop for first public build. (Locked)
- [x] Decide content pipeline: data-driven dialogs/NPCs/quests/items where practical. (Locked) 
- [x] Decide release gates: `alpha` for unstable feature-complete testing, `beta` for content-locked bug fixing. (Locked)
- [x] Decide out-of-scope for v1.0: online multiplayer, mod SDK (if intend), procedural full game world. (Locked)
- [ ] Decide target resolution(s) (for example `1280x720` base + scale options).
- [ ] Decide supported input devices at launch (keyboard only vs keyboard + controller).
- [ ] Decide death penalty rules (respawn cost, lost currency, or no penalty).
- [ ] Decide checkpoint density (rare/normal/frequent) and placement standard.
- [ ] Decide quest failure policy (can fail vs cannot fail).
- [ ] Decide inventory limit model (unlimited, slot-based, or weight-based).
- [ ] Decide economy model (currency sources/sinks and max carry rules).
- [ ] Decide healing model (consumables only vs regen vs mixed).
- [ ] Decide boss count for v1.0 (minimum 1, target number).
- [ ] Decide minimum content target for v1.0 (maps, enemy types, quest count).
- [ ] Decide dialogue tone and writing style guide (short lines, humor level, lore depth).
- [ ] Decide save slot count and overwrite behavior.
- [ ] Decide minimum hardware target (low-end PC baseline).
- [ ] Decide performance budget per frame (CPU/GPU target for 60 FPS).
- [ ] Decide localization scope for v1.0 (English only or multi-language prep).
- [ ] Decide accessibility baseline for launch (remap, text scale, contrast, assist options).
- [ ] Decide playtest cadence (weekly/biweekly) and tester count target.
- [ ] Decide release channel order (itch.io first, then GitHub release, or same day).

## Beginner Mode (How to Use This TODO)
- You are a beginner, so build in this order: `Easy -> Medium -> Advanced`.
- Do not start `Advanced` tasks until at least 70% of `Must Have` Easy+Medium are done.
- Keep pull requests small (1 to 5 tasks each).
- If stuck for more than 45 minutes, switch to a smaller task and come back.
- Use `alpha` when core systems are playable but unstable (expect bugs, missing polish).
- Use `beta` after alpha feedback is addressed and all Must Have features are done (focus on bug fixing and balancing, not new features).
- `P0` = critical bug (crash, save corruption, hard progress blocker). Fix immediately before new work.
- `P1` = major bug (important feature broken, bad gameplay regression). Fix before release.
- `P2` = minor bug/polish issue (workaround exists, low risk). Batch and fix after P0/P1.

## Must Have vs Nice to Have Feature Backlog (Beginner Friendly)
Target size: 150 features

### Must Have - Easy (32)
- [x] Player can move in 4/8 directions. (limited by asset back)
- [x] Player idle/walk animations play correctly.
- [x] Camera follows player smoothly.
- [x] Basic collision with walls/obstacles.
- [ ] Player cannot walk outside map bounds.
- [x] One melee attack button.
- [x] Attack has cooldown.
- [x] Enemy takes damage from player attack.
- [x] Enemy death removes sprite and collider.
- [x] Player can take damage.
- [x] Player invulnerability frames after hit.
- [x] Health bar UI updates in real time.
- [ ] Energy/magic bar UI updates in real time.
- [ ] Pause menu opens/closes reliably.
- [ ] Resume from pause works.
- [ ] Main menu with Start/Quit options.
- [ ] Game over screen appears on death.
- [ ] Restart from game over works.
- [ ] One test map fully playable.
- [ ] Map transition trigger works.
- [ ] Basic NPC interaction key prompt.
- [ ] One NPC with one-line dialog.
- [ ] Simple quest accept/complete flow.
- [ ] Quest log UI shows active quest.
- [ ] Inventory opens and closes.
- [ ] Pick up item from ground.
- [ ] Coin/currency counter updates.
- [ ] Basic chest interaction (open once).
- [ ] Save game to file.
- [ ] Load game from file.
- [x] Background music plays in map.
- [x] Hit sound effect plays on attack connect.

### Must Have - Medium (24)
- [ ] Light combo chain (2-3 hits).
- [ ] Heavy attack with higher stamina cost.
- [ ] Dodge/roll with brief invulnerability.
- [ ] Enemy patrol behavior.
- [ ] Enemy chase behavior when player near.
- [ ] Enemy attack telegraph animation.
- [ ] Enemy knockback on hit.
- [ ] Status effect system scaffold (burn/slow placeholder).
- [x] Magic cast system with cooldown + energy cost.
- [x] Two spells implemented.
- [ ] Damage numbers toggle (debug UI).
- [ ] Interaction system with range checks.
- [ ] Branching dialog with at least one choice.
- [ ] Door unlock via key item.
- [ ] World flag persistence for opened doors/chests.
- [ ] Checkpoint respawn system.
- [ ] Better save schema with version field.
- [ ] Save corruption fallback message.
- [ ] Audio sliders (master/music/sfx).
- [ ] Key rebinding for keyboard.
- [ ] Controller support baseline.
- [ ] Minimap for current area.
- [ ] At least 5 enemy types.
- [ ] At least 5 side quests.
- [ ] Add profiler markers in game loop (`update`, `draw`, `collision`, `audio`).
- [ ] Reproduce lag spike with deterministic test route.
- [ ] Fix camera jitter/offset edge bug in camera group.
- [ ] Add startup resource validation report (missing files, bad decode).
- [ ] Add smoke test: boot to gameplay loop for 5 minutes.
- [ ] Add `InputAction` enum.
- [ ] Implement attack window timings as data, not constants in methods.
- [ ] Finalize `README`, controls, known issues, and changelog.

### Must Have - Advanced (12)
- [ ] One full boss fight with 2 phases.
- [ ] Boss intro and outro sequence.
- [ ] Boss arena lock/unlock flow.
- [ ] Quest chain with prerequisites.
- [ ] Data-driven dialog/NPC/quest loader.
- [ ] Event bus with multi-listener support.
- [ ] Combat log/event debug overlay.
- [ ] Area-based music switching.
- [ ] Performance pass targeting stable 60 FPS.
- [ ] Packaging build for Windows / Linux.
- [ ] Crash-safe autosave at checkpoints.
- [ ] Full 45-90 minute playable progression loop.
- [ ] Build test matrix: resolutions, window/fullscreen, controller/keyboard.
- [ ] Run structured playtests and classify issues P0/P1/P2.
- [ ] Fix all P0 and high-priority P1 bugs.
- [ ] Freeze content and feature set before release build.
- [ ] Tag `alpha` build.
- [ ] Tag `beta` build after alpha fixes are complete.
- [ ] Verify all runtime assets are bundled correctly.
- [ ] Publish GitHub Release with source + binary.

### Nice to Have - Easy (12)
- [ ] Footstep sound variation by surface.
- [ ] Day/night visual tint toggle.
- [ ] Damage flash effect on enemies.
- [ ] Screen shake on heavy hit.
- [ ] Loot pickup sounds.
- [ ] Simple tutorial popups.
- [ ] Settings menu remembers choices.
- [ ] NPC nameplates above characters.
- [ ] Better quest completion popup.
- [ ] Optional FPS counter.
- [ ] Optional grid overlay debug.
- [ ] Screenshot keybind.

### Nice to Have - Medium (10)
- [ ] Crafting prototype with 3 recipes.
- [ ] Merchant buy/sell UI.
- [ ] Equipment slots (weapon/charm/armor).
- [ ] Elemental resistances on enemies.
- [ ] Elite enemy variants.
- [ ] Randomized loot tables.
- [ ] Localized text file structure (future i18n).
- [ ] Accessibility preset profiles.
- [ ] Better map transitions with fade.
- [ ] Cutscene trigger system (basic timeline).
- [ ] Create itch.io page (description, screenshots, trailer/gif, tags).

### Nice to Have - Advanced (24)
- [ ] Local co-op second player.
- [ ] Shared camera for co-op.
- [ ] Network prototype (experimental online).
- [ ] Boss modifiers/new game plus seed.
- [ ] Mod support for custom maps (limited).
- [ ] Replay/ghost run prototype.
- [ ] Procedural dungeon seed mode.
- [ ] Adaptive difficulty that reacts to player performance.
- [ ] Dynamic weather affecting visibility/combat.
- [ ] Faction reputation system with branching rewards.
- [ ] Enemy memory system (retreat/regroup/call backup).
- [ ] Companion AI party member prototype.
- [ ] Cinematic camera scripting tool.
- [ ] In-game cutscene editor (basic track system).
- [ ] Build-in telemetry dashboard for balancing.
- [ ] Daily challenge mode with leaderboard file export.
- [ ] Challenge mutators (no-heal, double-speed, low-vision).
- [ ] Skill tree respec system.
- [ ] Rune/enchantment crafting with rarity tiers.
- [ ] Dual-class loadout swap system.
- [ ] In-game codex/lore unlock tracker.
- [ ] Advanced photo mode with camera controls.
- [ ] Ghost replay race against previous run.
- [ ] Seasonal event content toggle system.
- [ ] Dynamic boss intro narration system.
- [ ] Enemy squad formations with role-based AI.
- [ ] Area hazard generator (traps, vents, falling rocks).
- [ ] Chain quest journal with recap summaries.
- [ ] Build variant manager (debug, playtest, release).
- [ ] In-game bug report form with screenshot attach.
- [ ] Analytics snapshot export to CSV after sessions.
- [ ] Difficulty presets with custom override sliders.
- [ ] World randomizer mode (items/enemies/doors).
- [ ] Arena survival mode with wave scripting.
- [ ] Puzzle dungeon toolkit (switches, timers, pressure plates).
- [ ] Mount or companion traversal system.
- [ ] Material farming routes and respawn rules.
- [ ] Achievement and milestone tracker.
- [ ] Smart NPC schedules (day/night routines).
- [ ] Environmental storytelling props system.
- [ ] Alternate endings triggered by world flags.
- [ ] Multi-phase final boss with adaptive pattern mix.
- [ ] Advanced accessibility mode (high contrast + assist aim).
- [ ] Modular DLC content loader scaffold.

---

## 1) Code Quality and Tooling TODO
- [ ] Add `ruff` and its config.
- [ ] Add `mypy` (gradual typing, start with `events`, `data`, `systems`).
- [ ] Add CI workflow: lint + tests + packaging smoke check.
- [ ] Add `tests/` with at least:
  - [ ] save/load roundtrip.
  - [ ] combat damage math.
  - [ ] quest state transitions.
  - [ ] boss phase transition correctness.
- [ ] Add pre-commit hooks for formatting/lint.

---

## 2) Asset/Sound Integration TODO
- [ ] Create `docs/ASSET_MANIFEST.csv`.
- [ ] Record source URL, license, author, attribution text for each imported asset. (continuous)
- [ ] Normalize sprite dimensions and origin points by category.
- [ ] Remove duplicate/temporary image files.
- [ ] Normalize SFX loudness (target LUFS range).
- [ ] Validate all referenced files exist at boot.
- [ ] Ensure no asset with unknown license ships. (continuous)

---

## 3) Definition of Done (Publish Ready)
- [ ] Full playthrough possible without blockers.
- [ ] Save/load stable and backward-safe.
- [ ] At least 1 polished boss and meaningful progression.
- [ ] NPC/dialog/interaction systems data-driven.
- [ ] Controls/options/audio/settings available.
- [ ] Performance stable near 60 FPS target.
- [ ] No open P0 bugs.
- [ ] Build packaged, tested, and publicly released.
