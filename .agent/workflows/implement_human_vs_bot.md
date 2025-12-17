---
description: Implement Human vs Bot CLI
---

# Workflow: Implement Human vs Bot CLI

This workflow builds the interactive CLI for playing against the bot and recording demonstrations.

## Phase 1: CLI Infrastructure

1.  [ ] **Create Script**: `scripts/play_vs_bot.py`.
2.  [ ] **Input Handling**:
    -   Implement `get_human_move(legal_actions)` function.
    -   Parse input string "row,col to row,col" (e.g., "5,0 4,1").
    -   Validate string format.
    -   Match against `legal_actions` list.
3.  [ ] **Visualization**:
    -   Use `env.render()` (ASCII) initially.
    -   (Optional) Upgrade to `rich` based rendering if libraries allow.

## Phase 2: Game Loop

4.  [ ] **Implement Loop**:
    -   Initialize Env and Bot (Heuristic).
    -   While not done:
        -   Render board.
        -   If User turn: `get_human_move`.
        -   If Bot turn: `bot.select_action`.
        -   Step environment.
        -   Log step.
    -   On Game Over: Print winner, save log.

## Phase 3: User Experience

5.  [ ] **Verify Usability**: Play a full game.
6.  [ ] **Add Hints**: Show legal moves with indices for easier selection (e.g., "0: (5,0)->(4,1)").

## Phase 4: Data Validation

7.  [ ] **Check Recorded File**: Ensure the human-played game is saved correctly and can be loaded by the replay system (if exists) or simply validated as valid JSON.
