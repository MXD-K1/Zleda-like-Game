# Refactor Plan

Last updated: 2026-04-28

> Disclaimer: This file was written by AI

## Purpose
This file tracks the refactoring phases and the specific files that must be cleaned up before adding more complex gameplay features.

## Phase R1 (Week 1): Foundation Stabilization
- [ ] Extract systems from `zelda/src/level.py` into:
  - `zelda/src/systems/combat_system.py`
  - `zelda/src/systems/magic_system.py`
  - `zelda/src/systems/audio_system.py`
- [ ] Add explicit game state flow (`BOOT`, `PLAYING`, `PAUSED`, `DIALOG`, `DEAD`, `CUTSCENE`).
- [ ] Add startup resource validation wrapper for images/sounds/fonts.
- [x] Rename `zelda/src/praticles.py` to `zelda/src/particles.py` and update imports.

## Phase R2 (Week 2): Entity and Input Decoupling
- [ ] Split `zelda/src/player.py` responsibilities into dedicated modules:
  - `zelda/src/player_controller.py`
  - `zelda/src/player_stats.py`
  - `zelda/src/player_combat.py`
- [ ] Replace direct keyboard polling with input abstraction.
- [ ] Introduce structured action states for player and enemy behavior.

## Phase R3 (Week 3): Data-Driven Content Refactor
- [ ] Refactor `zelda/src/map_loader.py` to use map/layer config instead of hardcoded layer names.
- [ ] Move dialog/NPC/quest/item definitions to external data files:
  - `zelda/src/data/dialogs.json`
  - `zelda/src/data/npcs.json`
  - `zelda/src/data/quests.json`
  - `zelda/src/data/items.json`
- [ ] Add world flag structure for progression gating.

## Phase R4 (Week 4): Event and Save Boundaries
- [ ] Refactor `zelda/src/events.py` to support multiple subscribers per event.
- [ ] Add event namespaces (`combat.*`, `ui.*`, `quest.*`, `audio.*`).
- [ ] Add save system module with schema versioning:
- [ ] `zelda/src/systems/save_system.py`
- [ ] Add migration support for save format evolution.

## Files That Need Refactoring (Priority)

## High Priority
- [ ] `zelda/src/level.py`
  - Problem: god object with mixed responsibilities.
  - Risk: hard to extend safely; high regression risk.

- [ ] `zelda/src/player.py`
  - Problem: input, combat, stats, and animation tightly coupled.
  - Risk: blocks combos/classes/multiplayer evolution.

- [ ] `zelda/src/events.py`
  - Problem: one-callback-per-event model.
  - Risk: brittle observer scaling for UI/quests/audio/combat.

- [ ] `zelda/src/map_loader.py`
  - Problem: hardcoded TMX layers and spawn rules.
  - Risk: each map/content change requires code edits.

## Medium Priority
- [ ] `zelda/src/entities/enemy.py`
  - Problem: AI, damage, animation, and sound tightly coupled.
  - Risk: boss/elite behavior expansion duplicates logic.

- [ ] `zelda/main.py`
  - Problem: limited scene/state orchestration structure.
  - Risk: title/gameover/cutscene flow grows ad hoc.

- [ ] `zelda/src/data/data.py`
  - Problem: static dict-heavy gameplay config with weak validation.
  - Risk: balancing and tuning become error-prone.

## Hygiene Priority
- [x] `zelda/src/praticles.py`
  - Problem: typo + naming inconsistency.
  - Risk: maintainability and onboarding friction.

- [ ] `zelda/assets/graphics/enemies/squid/attack/0 - Copy*.png`
  - Problem: duplicate temporary art files.
  - Risk: accidental animation imports and unstable content builds.
