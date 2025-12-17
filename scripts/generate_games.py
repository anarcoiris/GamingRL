
import argparse
import os
import sys

# Ensure root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import numpy as np
from tqdm import tqdm
from env.checkers_env import CheckersEnv
from agent.heuristic_agent import HeuristicAgent
from utils.game_logger import GameLogger

def get_agent(mode, env):
    """
    Factory for agents based on mode.
    Returns (agent_p1, agent_p2)
    """
    heuristic_p1 = HeuristicAgent(env.config, depth=2)
    # Heuristic P2 needs to be created carefully? 
    # Current HeuristicAgent implementation handles player ID in select_action.
    # So we can reuse the same instance or create new one.
    heuristic_p2 = HeuristicAgent(env.config, depth=2)
    
    if mode == "random_vs_random":
        return None, None
    elif mode == "heuristic_vs_random":
        # P1 Heuristic, P2 Random
        return heuristic_p1, None
    elif mode == "random_vs_heuristic":
        # P1 Random, P2 Heuristic
        return None, heuristic_p2
    elif mode == "heuristic_vs_heuristic":
        return heuristic_p1, heuristic_p2
    else:
        raise ValueError(f"Unknown mode: {mode}")

def select_move(agent, env, player, legal_actions):
    if not legal_actions:
        return None
        
    if agent is None:
        # Random
        return random.choice(legal_actions)
    else:
        # Heuristic
        # HeuristicAgent expects board and legal_actions
        return agent.select_action(env.board, legal_actions, player=player)

def generate_games(count, mode, outdir):
    os.makedirs(outdir, exist_ok=True)
    
    env = CheckersEnv()
    agent_p1, agent_p2 = get_agent(mode, env)
    
    print(f"Generating {count} games in mode '{mode}' to '{outdir}'...")
    
    for i in tqdm(range(count)):
        obs, info = env.reset()
        logger = GameLogger(metadata={"mode": mode, "p1": str(agent_p1), "p2": str(agent_p2)})
        
        done = False
        truncated = False
        
        while not (done or truncated):
            current_player = env.current_player
            legal_actions = env.get_legal_actions()
            
            if current_player == 1:
                action = select_move(agent_p1, env, 1, legal_actions)
            else:
                action = select_move(agent_p2, env, -1, legal_actions)
                
            # Log step
            # Note: We Log BEFORE step? Or AFTER?
            # Standard: Log State S_t, Action A_t.
            logger.log_step(env.board, action, current_player, env.step_count)
            
            obs, reward, done, truncated, info = env.step(action)
            
        winner = info.get("winner")
        reason = info.get("draw_reason") if winner == 0 else "checkmate" # Simplify
        logger.log_game_over(winner, reason)
        
        filename = f"{logger.metadata['timestamp'].replace(':','-')}_{logger.game_id[:8]}.json"
        logger.save(os.path.join(outdir, filename))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="heuristic_vs_random", 
                        choices=["random_vs_random", "heuristic_vs_random", "random_vs_heuristic", "heuristic_vs_heuristic"])
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--outdir", type=str, default="data/generated")
    
    args = parser.parse_args()
    generate_games(args.count, args.mode, args.outdir)
