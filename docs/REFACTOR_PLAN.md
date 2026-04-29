# Refactor Plan

Last updated: 2026-04-28

> Disclaimer: This file was written by AI

## Purpose
This file tracks the refactoring phases and the specific files that must be cleaned up before adding more complex gameplay features.

## Phase R1 (Week 1): Foundation Stabilization
- Extract systems from `zelda/level.py` into:
- `zelda/systems/combat_system.py`
- `zelda/systems/magic_system.py`
- `zelda/systems/audio_system.py`
- Add explicit game state flow (`BOOT`, `PLAYING`, `PAUSED`, `DIALOG`, `DEAD`, `CUTSCENE`).
- Add startup resource validation wrapper for images/sounds/fonts.
- Rename `zelda/praticles.py` to `zelda/particles.py` and update imports.

## Phase R2 (Week 2): Entity and Input Decoupling
- Split `zelda/player.py` responsibilities into dedicated modules:
- `zelda/player_controller.py`
- `zelda/player_stats.py`
- `zelda/player_combat.py`
- Replace direct keyboard polling with input abstraction.
- Introduce structured action states for player and enemy behavior.

## Phase R3 (Week 3): Data-Driven Content Refactor
- Refactor `zelda/map_loader.py` to use map/layer config instead of hardcoded layer names.
- Move dialog/NPC/quest/item definitions to external data files:
- `zelda/data/dialogs.json`
- `zelda/data/npcs.json`
- `zelda/data/quests.json`
- `zelda/data/items.json`
- Add world flag structure for progression gating.

## Phase R4 (Week 4): Event and Save Boundaries
- Refactor `zelda/events.py` to support multiple subscribers per event.
- Add event namespaces (`combat.*`, `ui.*`, `quest.*`, `audio.*`).
- Add save system module with schema versioning:
- `zelda/systems/save_system.py`
- Add migration support for save format evolution.

## Files That Need Refactoring (Priority)

## High Priority
- `zelda/level.py`
- Problem: god object with mixed responsibilities.
- Risk: hard to extend safely; high regression risk.

- `zelda/player.py`
- Problem: input, combat, stats, and animation tightly coupled.
- Risk: blocks combos/classes/multiplayer evolution.

- `zelda/events.py`
- Problem: one-callback-per-event model.
- Risk: brittle observer scaling for UI/quests/audio/combat.

- `zelda/map_loader.py`
- Problem: hardcoded TMX layers and spawn rules.
- Risk: each map/content change requires code edits.

## Medium Priority
- `zelda/enemy.py`
- Problem: AI, damage, animation, and sound tightly coupled.
- Risk: boss/elite behavior expansion duplicates logic.

- `main.py`
- Problem: limited scene/state orchestration structure.
- Risk: title/gameover/cutscene flow grows ad hoc.

- `zelda/data/data.py`
- Problem: static dict-heavy gameplay config with weak validation.
- Risk: balancing and tuning become error-prone.

## Hygiene Priority
- `zelda/praticles.py`
- Problem: typo + naming inconsistency.
- Risk: maintainability and onboarding friction.

- `assets/graphics/enemies/squid/attack/0 - Copy*.png`
- Problem: duplicate temporary art files.
- Risk: accidental animation imports and unstable content builds.
