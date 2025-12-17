"""Agent loader factory for consistent agent instantiation."""

import torch
from typing import Optional, Any, Dict
from agent.dqn import DQNAgent
from agent.heuristic_agent import HeuristicAgent
import random

class RandomAgent:
    """Simple agent that selects actions randomly."""
    def select_action(self, state, legal_actions, **kwargs):
        if not legal_actions:
            return None
        return random.choice(legal_actions)

def load_agent(agent_type: str, config: Dict[str, Any], checkpoint_path: Optional[str] = None, device: Optional[str] = None) -> Any:
    """
    Factory function to load different types of agents.
    
    Args:
        agent_type: One of 'random', 'heuristic', 'dqn'
        config: Environment configuration dictionary
        checkpoint_path: Path to model weights (required for 'dqn')
        device: Device to load model on ('cpu', 'cuda')
        
    Returns:
        Agent instance
    """
    agent_type = agent_type.lower()
    
    if agent_type == "random":
        return RandomAgent()
    
    elif agent_type == "heuristic":
        # Using depth from config or default to 3
        depth = config.get("heuristic_depth", 3)
        return HeuristicAgent(config=config, depth=depth)
    
    elif agent_type == "dqn":
        if not checkpoint_path:
            raise ValueError("Checkpoint path is required for DQN agent")
        
        agent = DQNAgent(
            state_shape=(4, 8, 8),
            device=device
        )
        agent.load_checkpoint(checkpoint_path)
        agent.q_network.eval()
        return agent
    
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")
