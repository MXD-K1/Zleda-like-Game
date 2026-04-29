# TODOS - 90 Day Playable + Publish Plan

Last updated: 2026-04-28
Scope: finish single-player core, add boss/content loop, ship release build, and implement multiplayer in controlled scope.

> Disclaimer: This file was written by AI 

## 0) Non-Negotiable Principles
- Keep game playable at all times on `main`.
- Ship vertical slices early, then scale.
- Refactor before major feature spikes.
- No new feature enters without save/load + UI + audio hooks.
- Every asset/sound added must have source + license recorded.

---

## 1) Refactoring Phases (Start Now)

### Phase R1 (Week 1): Stabilize Foundation
Goal: remove architectural friction that will block quests, bosses, and multiplayer.

- [ ] Create `zelda/systems/` package.
- [ ] Move combat orchestration out of [`zelda/level.py`](/E:/MyProjects/Python/ZeldaGame/zelda/level.py) into `systems/combat_system.py`.
- [ ] Move magic dispatch out of [`zelda/level.py`](/E:/MyProjects/Python/ZeldaGame/zelda/level.py) into `systems/magic_system.py`.
- [ ] Move sound boot/loop logic out of [`zelda/level.py`](/E:/MyProjects/Python/ZeldaGame/zelda/level.py) into `systems/audio_system.py`.
- [ ] Add `GameState` enum (`BOOT`, `PLAYING`, `PAUSED`, `DIALOG`, `DEAD`, `CUTSCENE`) and replace boolean flags.
- [ ] Add `ResourceManager` to wrap `load_images/load_sounds/init_fonts` with validated startup report.
- [ ] Standardize naming: rename `praticles.py` -> `particles.py` and update imports.
- [ ] Replace stringly-typed magic (`'heal'`, `'flame'`) with constants/enums.

### Phase R2 (Week 2): Decouple Entities and Input
Goal: make player/enemy logic extensible for combos, classes, and network sync.

- [ ] Split [`zelda/player.py`](/E:/MyProjects/Python/ZeldaGame/zelda/player.py):
- [ ] `player_controller.py` for input mapping.
- [ ] `player_stats.py` for health/energy/damage formulas.
- [ ] `player_combat.py` for attack state machine.
- [ ] Add typed dataclasses for weapon/magic stats in `zelda/data/`.
- [ ] Replace direct `pygame.key.get_pressed()` usage with input abstraction for multiplayer/local co-op support.
- [ ] Add explicit player action states (`MOVE`, `ATTACK_LIGHT`, `ATTACK_HEAVY`, `CAST`, `STUN`, `DEAD`).
- [ ] Refactor [`zelda/enemy.py`](/E:/MyProjects/Python/ZeldaGame/zelda/enemy.py) AI into behavior components.

### Phase R3 (Week 3): Data-Driven Content
Goal: stop hardcoding map/enemy/dialog rules in code.

- [ ] Replace hardcoded layer names in [`zelda/map_loader.py`](/E:/MyProjects/Python/ZeldaGame/zelda/map_loader.py) with config map.
- [ ] Add spawn component schema (`enemy_type`, `level`, `loot_table`, `aggro_range`).
- [ ] Create `data/dialogs.json`, `data/npcs.json`, `data/quests.json`, `data/items.json`.
- [ ] Dialog renderer reads from data, not inline strings.
- [ ] Add world flag system (`world_flags.json`) for quest gates and door unlocks.

### Phase R4 (Week 4): Event and Save Boundaries
Goal: make future feature growth safe.

- [ ] Refactor [`zelda/events.py`](/E:/MyProjects/Python/ZeldaGame/zelda/events.py) to support multiple listeners/event.
- [ ] Add event namespaces (`combat.*`, `ui.*`, `quest.*`, `audio.*`).
- [ ] Add safe publish mode (log warning if no listener instead of raising in non-critical events).
- [ ] Add `save_system.py` with schema versioning (`save_version`).
- [ ] Add migration hook for old save versions.

---

## 2) Files/Places That Need Refactoring (Blocking Long-Term Extension)

### High Priority (Do first)
- [`zelda/level.py`](/E:/MyProjects/Python/ZeldaGame/zelda/level.py)
- Problem: god object (resource load, combat, ui, map control, pause, audio, particle orchestration).
- Impact: every new feature creates merge conflicts and regression risk.

- [`zelda/player.py`](/E:/MyProjects/Python/ZeldaGame/zelda/player.py)
- Problem: mixed responsibilities (input, state, stats, combat, animation, progression).
- Impact: hard to add combos, classes, net sync, AI possession tests.

- [`zelda/events.py`](/E:/MyProjects/Python/ZeldaGame/zelda/events.py)
- Problem: one callback per event; throws hard errors for missing subscriptions.
- Impact: brittle as systems scale (quests/audio/UI observers cannot co-exist).

- [`zelda/map_loader.py`](/E:/MyProjects/Python/ZeldaGame/zelda/map_loader.py)
- Problem: map layers are hardcoded and spawn logic is monolithic.
- Impact: adding new tile layers/biomes/interactions requires code edits every time.

### Medium Priority
- [`zelda/enemy.py`](/E:/MyProjects/Python/ZeldaGame/zelda/enemy.py)
- Problem: AI state, damage model, sounds, animation tightly coupled.
- Impact: boss mechanics and elite variants become duplicated spaghetti.

- [`main.py`](/E:/MyProjects/Python/ZeldaGame/main.py)
- Problem: no explicit scene/state orchestration abstraction.
- Impact: cutscenes/title/gameover/options flow will stay ad-hoc.

- [`zelda/data/data.py`](/E:/MyProjects/Python/ZeldaGame/zelda/data/data.py)
- Problem: gameplay tuning likely static dict-heavy and hard to validate.
- Impact: balancing work slows down and causes runtime errors.

### Hygiene Priority
- [`zelda/praticles.py`](/E:/MyProjects/Python/ZeldaGame/zelda/praticles.py)
- Problem: typo in module name.
- Impact: long-term maintainability + team confusion.

- `assets/graphics/enemies/squid/attack` duplicate files (`0 - Copy*.png`)
- Problem: unclean content pipeline.
- Impact: accidental wrong animation import and inconsistent builds.

---

## 3) Detailed 12-Week Execution TODO

## Week 1 - Refactor Foundation + Performance Debug
- [ ] Add profiler markers in game loop (`update`, `draw`, `collision`, `audio`).
- [ ] Reproduce lag spike with deterministic test route.
- [ ] Fix camera jitter/offset edge bug in camera group.
- [ ] Extract `AudioSystem`, route BGM/SFX through it.
- [ ] Extract `CombatSystem` from `Level.player_attack_logic`.
- [ ] Add startup resource validation report (missing files, bad decode).
- [ ] Rename `praticles.py` and update imports.
- [ ] Add smoke test: boot to gameplay loop for 5 minutes.
- [ ] Acceptance gate: no hitch > 50ms in normal play.

## Week 2 - Player/Enemy Architecture Refactor
- [ ] Add `InputAction` enum.
- [ ] Implement input adapter layer for keyboard/controller.
- [ ] Split player state handling into clean state machine.
- [ ] Implement attack window timings as data, not constants in methods.
- [ ] Refactor enemy status transitions into component class.
- [ ] Add unit tests for damage + invulnerability timing.
- [ ] Acceptance gate: no gameplay regression in movement/combat.

## Week 3 - Interaction + Dialog Data Refactor
- [ ] Implement `Interactable` base class.
- [ ] Add interaction prompt system with distance checks.
- [ ] Replace direct dialog strings with `dialogs.json`.
- [ ] Add choice branch support + conditional requirements.
- [ ] Add NPC registry from `npcs.json`.
- [ ] Add tests for dialog branching and fallback lines.
- [ ] Acceptance gate: 5 NPCs with branching dialog fully data-driven.

## Week 4 - Save/Quest/Event Refactor
- [ ] Build `QuestSystem` with explicit states.
- [ ] Build `SaveSystem` with schema version.
- [ ] Persist player stats, quest state, world flags, inventory.
- [ ] EventBus multi-subscriber refactor.
- [ ] Add checkpoint respawn state and death recovery path.
- [ ] Add save corruption recovery fallback.
- [ ] Acceptance gate: quest progress survives reload reliably.

## Week 5 - World Building Pass
- [ ] Define overworld to dungeon map graph.
- [ ] Standardize TMX layer contracts and document them.
- [ ] Add transition points (doors, edges, portals).
- [ ] Add locked-door + key requirement interaction.
- [ ] Add collision audit pass on all walkable maps.
- [ ] Acceptance gate: 20+ minutes uninterrupted traversal.

## Week 6 - Boss Vertical Slice
- [ ] Implement boss base class with phase transitions.
- [ ] Add telegraphed attacks (windup, active, recovery windows).
- [ ] Add boss-specific hazards (AoE, projectiles, summons).
- [ ] Add boss UI health bar + intro/outro triggers.
- [ ] Add victory rewards (quest completion + skill unlock).
- [ ] Acceptance gate: boss fight complete and beatable without bugs.

## Week 7 - Combat Depth + Special Attacks
- [ ] Implement light combo chain (3-step).
- [ ] Implement heavy attack with stamina/energy cost.
- [ ] Implement dodge/roll with i-frames.
- [ ] Implement at least 2 specials (directional slash, flame wave).
- [ ] Add hitstop/camera shake/screen flash tuning.
- [ ] Balance damage and cooldown across enemy types.
- [ ] Acceptance gate: combat loop feels responsive and readable.

## Week 8 - Audio + UX + Options
- [ ] Implement area-based BGM switching.
- [ ] Add SFX for all key actions and menus.
- [ ] Add options menu (master/music/sfx volumes).
- [ ] Add key rebinding menu.
- [ ] Add accessibility options (text speed, font scale).
- [ ] Acceptance gate: external tester can configure controls/audio alone.

## Week 9 - Content Completion
- [ ] Populate 2-3 enemy archetypes per region.
- [ ] Add 10-15 quests (main + side mix).
- [ ] Add interactables: chests, signs, levers, lootables, shops.
- [ ] Add itemization pass (consumables, keys, upgrades).
- [ ] Add minimap/world hint system (optional but recommended).
- [ ] Acceptance gate: 60-90 minute full progression loop.

## Week 10 - Multiplayer (Scoped)
- [ ] Decide mode:
- [ ] Local co-op required.
- [ ] Online optional experimental.
- [ ] Add Player2 input mapping + join/drop flow.
- [ ] Implement shared camera constraints.
- [ ] Sync combat events and enemy aggro with 2 players.
- [ ] If online prototype: host-authoritative sync for movement + attacks.
- [ ] Acceptance gate: local co-op dungeon run without desync/crash.

## Week 11 - QA/Optimization/Release Candidate
- [ ] Build test matrix: resolutions, window/fullscreen, controller/keyboard.
- [ ] Run structured playtests and classify issues P0/P1/P2.
- [ ] Fix all P0 and high-priority P1 bugs.
- [ ] Optimize expensive sprite collision and draw ordering paths.
- [ ] Freeze content and feature set.
- [ ] Tag `rc1`.
- [ ] Acceptance gate: stable RC build for 2+ testers.

## Week 12 - Packaging and Publishing
- [ ] Build standalone executable (PyInstaller or Briefcase).
- [ ] Verify all runtime assets bundled correctly.
- [ ] Add full credits + attributions + license references.
- [ ] Finalize `README`, controls, known issues, changelog.
- [ ] Create itch.io page (description, screenshots, trailer/gif, tags).
- [ ] Publish GitHub Release with source + binary.
- [ ] Acceptance gate: public download works on clean machine.

---

## 4) Code Quality and Tooling TODO
- [ ] Add `ruff` + `black` configs.
- [ ] Add `mypy` (gradual typing, start with `events`, `data`, `systems`).
- [ ] Add CI workflow: lint + tests + packaging smoke check.
- [ ] Add `tests/` with at least:
- [ ] save/load roundtrip.
- [ ] combat damage math.
- [ ] quest state transitions.
- [ ] boss phase transition correctness.
- [ ] Add pre-commit hooks for formatting/lint.

---

## 5) Asset/Sound Integration TODO
- [ ] Create `docs/ASSET_MANIFEST.csv`.
- [ ] Record source URL, license, author, attribution text for each imported asset.
- [ ] Normalize sprite dimensions and origin points by category.
- [ ] Remove duplicate/temporary image files.
- [ ] Normalize SFX loudness (target LUFS range).
- [ ] Validate all referenced files exist at boot.
- [ ] Ensure no asset with unknown license ships.

---

## 6) Definition of Done (Publish Ready)
- [ ] Full playthrough possible without blockers.
- [ ] Save/load stable and backward-safe.
- [ ] At least 1 polished boss and meaningful progression.
- [ ] NPC/dialog/interaction systems data-driven.
- [ ] Controls/options/audio/settings available.
- [ ] Performance stable near 60 FPS target.
- [ ] No open P0 bugs.
- [ ] Build packaged, tested, and publicly released.
