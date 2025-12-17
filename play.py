"""Unified entry point for playing checkers against bots or other humans."""

import argparse
import sys
import os
import json
import time
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from env.checkers_env import CheckersEnv
from agent.loader import load_agent
from agent.heuristic_agent import HeuristicAgent
from ui.interaction import get_human_action, list_legal_moves
from viz.board_renderer import BoardRenderer
from utils.game_logger import GameLogger

def run_game(args):
    """Execution of the game loop."""
    # Load config
    config_path = args.config
    with open(config_path, "r") as f:
        config = json.load(f)

    # Initialize environment
    env = CheckersEnv(config)
    renderer = BoardRenderer(use_rich=not args.no_rich)
    
    # Setup Loggers
    logger = GameLogger(metadata={
        "p1_type": args.p1,
        "p2_type": args.p2,
        "config": config_path
    })

    # Load agents
    # Player 1 is 'agent_1', Player -1 is 'agent_2'
    agents = {}
    
    # Agent 1 (Player 1)
    if args.p1 != "human":
        agents[1] = load_agent(args.p1, config, args.p1_checkpoint)
        print(f"Loaded Agent 1: {args.p1}")
    else:
        agents[1] = "human"
        print("Player 1: Human")

    # Agent 2 (Player -1)
    if args.p2 != "human":
        agents[-1] = load_agent(args.p2, config, args.p2_checkpoint)
        print(f"Loaded Agent 2: {args.p2}")
    else:
        agents[-1] = "human"
        print("Player 2: Human")

    # Main Loop
    obs, info = env.reset()
    done = False
    truncated = False
    automatic_mode = not args.step
    
    print("\n" + "="*50)
    print("GAME STARTED")
    if args.step:
        print("Step-by-step mode: Press Enter to advance, 'a' for automatic.")
    print("="*50)

    while not (done or truncated):
        current_player = env.current_player
        legal_actions = env.get_legal_actions()
        
        if not legal_actions:
            print(f"No legal actions for player {current_player}. Game over.")
            break

        # Render board
        if renderer.rich_enabled:
            renderer.render_rich(env.board, current_player, game_info={"step": env.step_count})
        else:
            print(renderer.render_ascii(env.board, current_player))

        # Select Action
        agent = agents[current_player]
        
        if agent == "human":
            if args.list:
                list_legal_moves(legal_actions)
            action = get_human_action(legal_actions)
            if action is None: # User requested exit
                print("Game terminated by user.")
                return
        else:
            # Bot turn
            if not automatic_mode:
                user_step = input(f"\n[Bot {current_player}] Press Enter to step, 'a' for automatic: ").strip().lower()
                if user_step == 'a':
                    automatic_mode = True
                elif user_step in ['q', 'quit']:
                    return

            print(f"Player {current_player} ({args.p1 if current_player == 1 else args.p2}) is thinking...")
            
            # Differentiate call based on agent type
            if isinstance(agent, HeuristicAgent):
                # Heuristic needs raw board
                action = agent.select_action(env.board, legal_actions, player=current_player)
            else:
                # DQNAgent and RandomAgent expect the observation (4, 8, 8)
                action = agent.select_action(obs, legal_actions)
            
            if automatic_mode:
                time.sleep(args.delay)
            print(f"Bot chose: {action['from']} -> {action['to']}")

        # Step
        logger.log_step(env.board, action, current_player, env.step_count)
        obs, reward, done, truncated, info = env.step(action)

    # Game Over
    if renderer.rich_enabled:
        renderer.render_rich(env.board, env.current_player)
    else:
        print(renderer.render_ascii(env.board, env.current_player))

    winner = info.get("winner", 0)
    stats = {
        "steps": env.step_count,
        "winner": winner,
        "reason": info.get("draw_reason", "terminal state") if winner == 0 else "victory"
    }
    
    renderer.render_game_summary(stats, winner)
    logger.log_game_over(winner, stats["reason"])

    # Saving
    os.makedirs(args.outdir, exist_ok=True)
    filename = f"game_{time.strftime('%Y%m%d_%H%M%S')}.json"
    save_path = os.path.join(args.outdir, filename)
    logger.save(save_path)
    print(f"\nGame data saved to: {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GamingRL - Play Checkers")
    parser.add_argument("--p1", type=str, default="human", choices=["human", "random", "heuristic", "dqn"], help="Player 1 type")
    parser.add_argument("--p2", type=str, default="heuristic", choices=["human", "random", "heuristic", "dqn"], help="Player 2 type")
    parser.add_argument("--p1_checkpoint", type=str, help="Path to DQN checkpoint for player 1")
    parser.add_argument("--p2_checkpoint", type=str, help="Path to DQN checkpoint for player 2")
    parser.add_argument("--config", type=str, default="config/checkers_rules.json", help="Path to rules config")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between bot moves (seconds)")
    parser.add_argument("--no_rich", action="store_true", help="Disable Rich rendering")
    parser.add_argument("--list", action="store_true", help="Always list legal moves indexes")
    parser.add_argument("--step", action="store_true", help="Step-by-step bot moves")
    parser.add_argument("--outdir", type=str, default="data/generated", help="Directory to save game logs")
    
    args = parser.parse_args()
    
    try:
        run_game(args)
    except KeyboardInterrupt:
        print("\nAborted.")
