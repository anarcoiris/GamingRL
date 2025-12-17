---
description: Implement Game Logger & Data Generation
---

# Workflow: Implement Game Logger & Data Generation

This workflow implements the system to record games in JSON format and generate synthetic datasets.

## Phase 1: Game Logger

1.  [ ] **Design Schema**: implementation of `utils/game_logger.py` to match `env/tests/test_cases/*.json` format but for full games (list of moves/states).
2.  [ ] **Implement Logger Class**:
    -   Methods: `log_step(board, action, player)`, `log_outcome(winner)`, `save(filepath)`.
    -   Ensure JSON serializability of numpy arrays (use `tolist()`).
3.  [ ] **Unit Test Logger**: Create `tests/test_game_logger.py` to verify JSON output validity.

## Phase 2: Game Generation Script

4.  [ ] **Create Script**: `scripts/generate_games.py`.
    -   Arguments: `--mode` (random_vs_random, heuristic_vs_random, etc.), `--count` (number of games), `--outdir`.
    -   Loop:
        -   Reset Env.
        -   Loop steps: Agent selects action -> Env step -> Logger log.
        -   Save JSON on done.
5.  [ ] **Verify Output**: Run generation of 5 games and inspect JSONs manually.

## Phase 3: Integration & Standards

6.  [ ] **Update Standards**: Ensure generated data follows `data/README.md` structure (create if missing).
7.  [ ] **Gitignore**: Ensure `data/generated/` is gitignored.
