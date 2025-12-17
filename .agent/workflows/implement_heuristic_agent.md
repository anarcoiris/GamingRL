---
description: Implement Heuristic Agent (Minimax)
---

# Workflow: Implement Heuristic Agent

This workflow guides the implementation of a Minimax-based heuristic agent for the Checkers environment.

## Phase 1: Preparation & Design

1.  [ ] **Review Environment API**: Ensure clear understanding of `get_legal_actions` and `step` in `env/checkers_env.py`.
2.  [ ] **Create Test Plan**: Create a new test file `agent/tests/test_heuristic_agent.py` describing expected behaviors (e.g., choosing a capture over a non-capture, blocking a win).

## Phase 2: Implementation

3.  [ ] **Create Agent File**: Create `agent/heuristic_agent.py`.
    -   Define `HeuristicAgent` class.
    -   Implement `evaluate_board(board, player)` static method.
    -   Implement `minimax(board, depth, maximizing_player)` method with Alpha-Beta pruning.
    -   Implement `select_action(board, legal_actions)` method.
4.  [ ] **Implement Evaluation Logic**:
    -   Base score: Piece count (Men: 1, Kings: 1.5).
    -   Positional score: Center control bonus.
5.  [ ] **Implement Minimax**:
    -   Recursive search.
    -   Use `env.rules.Rules` or equivalent to simulate moves without full environment overhead if possible, or use a cloned environment state. *Note: Using `deepcopy` on state is safer for now.*

## Phase 3: Verification

6.  [ ] **Run Unit Tests**: Execute `pytest agent/tests/test_heuristic_agent.py`.
7.  [ ] **Benchmark**: Create a script `scripts/benchmark_heuristic.py` to play 100 games vs Random Agent.
    -   // turbo
    -   Target: >90% Win Rate.
8.  [ ] **Documentation**: Update `agent/README.md` with usage instructions.

## Phase 4: Integration

9.  [ ] **Register Agent**: Ensure the agent can be easily instantiated for the VS mode.
