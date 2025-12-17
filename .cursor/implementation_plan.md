# Implementation Plan: Interactive Human vs Bot System

## Goal Description
Enable interactive "Human vs Bot" games via a robust CLI (and extensible for future GUI), allowing testing of trained agents against humans or other baselines. Centralize agent loading and user interaction logic effectively.

## User Review Required
- [ ] Confirm if `play.py` should be at root or in `scripts/`. (Proposed: Root for accessibility).
- [ ] confirm if `rich` library is acceptable for the primary CLI interface (fallback to ASCII if missing).

## Proposed Changes

### 1. Centralized Agent Loading (`agent/loader.py`)
Create a factory to instantiate agents easily.
- **Support**: `random`, `heuristic`, `dqn` (from checkpoint).
- **Interface**: `load_agent(type, config_path, checkpoint_path=None)`.

### 2. Interaction Module (`ui/interaction.py`)
Decouple input handling from game logic.
- **Move Parsing**: Handle `a3->b4`, `5,0 4,1`, etc.
- **Validation**: Check against legal moves.
- **Display**: Use `viz.board_renderer` for output.

### 3. Main Entry Point (`play.py`)
A clean script to run games.
- **Args**: `--player1`, `--player2`, `--render_mode`.
- **Logic**: Game loop reusing `CheckersEnv`.
- **Logging**: Integrate `GameLogger` to save replays.

### 4. File Structure Updates
#### [NEW] [agent/loader.py](file:///c:/Users/soyko/Documents/GamingRL/agent/loader.py)
#### [NEW] [ui/interaction.py](file:///c:/Users/soyko/Documents/GamingRL/ui/interaction.py)
#### [NEW] [play.py](file:///c:/Users/soyko/Documents/GamingRL/play.py)
#### [MODIFY] [env/utils.py](file:///c:/Users/soyko/Documents/GamingRL/env/utils.py) (Optional, if helpers needed)

## Verification Plan
### Manual Verification (report to user for him to verify)
- Play a full game Human vs Random. Make human play first.
- Play a few moves Human vs Heuristic to verify input parsing solidity. Make human play second.
- Load a DQN checkpoint and verify inference runs.
- Check generated JSON logs in `data/generated/`.

## Documentation & Architecture Tasks

### Planning / Analysis (report to user before commencing to change mode)
- [ ] Analyze `DESIGN.md` (brief check for alignment)
- [ ] Analyze module-level READMEs (env, agent, viz)
- [ ] Create Implementation Plan
- [ ] Define structure for new `README.md`
- [ ] Identify other documents needing updates

### Execution (report to user before commencing to change mode)
- [ ] Execute documentation updates
- [ ] Update root `README.md`
- [ ] Ensure all links are valid
- [ ] Add architectural diagrams (Mermaid) if applicable

### Verification (report to user before commencing to change mode)
- [ ] Review against "Senior Architect" persona standards
- [ ] Verify formatting