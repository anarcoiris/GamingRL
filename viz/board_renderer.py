"""Advanced board rendering utilities with Rich and ASCII support.

This module provides enhanced board visualization with:
- Rich-based colorful terminal rendering
- Q-value overlays
- Action highlighting
- Game state information display
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Union

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.style import Style
    from rich.layout import Layout
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


# Piece symbols
PIECE_SYMBOLS = {
    "empty_light": " ",
    "empty_dark": "·",
    "player1": "●",      # Player 1 (White/Red)
    "player1_king": "♔",
    "player2": "○",      # Player 2 (Black)
    "player2_king": "♚",
}

# Alternative ASCII symbols (for terminals without Unicode support)
PIECE_SYMBOLS_ASCII = {
    "empty_light": " ",
    "empty_dark": ".",
    "player1": "w",
    "player1_king": "W",
    "player2": "b",
    "player2_king": "B",
}

# Rich color styles
STYLES = {
    "light_square": Style(bgcolor="wheat1"),
    "dark_square": Style(bgcolor="dark_green"),
    "player1_piece": Style(color="red", bold=True),
    "player1_king": Style(color="bright_red", bold=True),
    "player2_piece": Style(color="white", bold=True),
    "player2_king": Style(color="bright_white", bold=True),
    "highlight_from": Style(bgcolor="yellow"),
    "highlight_to": Style(bgcolor="cyan"),
    "highlight_capture": Style(bgcolor="red"),
    "q_value_high": Style(color="green"),
    "q_value_mid": Style(color="yellow"),
    "q_value_low": Style(color="red"),
}


class BoardRenderer:
    """Renderer for checkers board with multiple output formats.
    
    Supports:
    - ASCII rendering (simple terminal)
    - Rich rendering (colorful terminal)
    - Q-value overlay rendering
    - Action highlighting
    
    Attributes:
        use_unicode: Whether to use Unicode symbols
        console: Rich Console instance (if available)
    """
    
    def __init__(
        self,
        use_unicode: bool = True,
        use_rich: bool = True,
    ):
        """Initialize board renderer.
        
        Args:
            use_unicode: Use Unicode piece symbols
            use_rich: Use Rich library for colorful output
        """
        self.use_unicode = use_unicode
        self.symbols = PIECE_SYMBOLS if use_unicode else PIECE_SYMBOLS_ASCII
        
        if use_rich and RICH_AVAILABLE:
            self.console = Console()
            self.rich_enabled = True
        else:
            self.console = None
            self.rich_enabled = False
    
    def render_ascii(
        self,
        board: np.ndarray,
        current_player: int = 1,
        last_move: Optional[Dict] = None,
        legal_actions: Optional[List[Dict]] = None,
    ) -> str:
        """Render board as ASCII string.
        
        Args:
            board: Board array (8, 8) with values:
                   0: empty, 1: player1, 2: player1 king,
                   -1: player2, -2: player2 king
            current_player: Current player (1 or -1)
            last_move: Optional last move to highlight
            legal_actions: Optional list of legal actions to show
            
        Returns:
            ASCII string representation of the board
        """
        lines = []
        
        # Header
        lines.append("   " + "  ".join("abcdefgh"))
        lines.append("  +" + "---" * 8 + "+")
        
        # Board rows
        for row in range(8):
            line = f"{8 - row} |"
            for col in range(8):
                cell_value = board[row, col]
                symbol = self._get_piece_symbol(cell_value, row, col)
                
                # Add highlighting markers
                prefix = " "
                suffix = ""
                
                if last_move:
                    if (row, col) == tuple(last_move.get("from", [])):
                        prefix = "["
                        suffix = "]"
                    elif (row, col) == tuple(last_move.get("to", [])):
                        prefix = ">"
                        suffix = "<"
                
                line += f"{prefix}{symbol}{suffix}"
            
            line += f" | {8 - row}"
            lines.append(line)
        
        # Footer
        lines.append("  +" + "---" * 8 + "+")
        lines.append("   " + "  ".join("abcdefgh"))
        
        # Player info
        player_str = "Player 1 (●)" if current_player == 1 else "Player 2 (○)"
        lines.append(f"\nCurrent turn: {player_str}")
        
        if legal_actions is not None:
            lines.append(f"Legal moves: {len(legal_actions)}")
        
        return "\n".join(lines)
    
    def render_rich(
        self,
        board: np.ndarray,
        current_player: int = 1,
        last_move: Optional[Dict] = None,
        q_values: Optional[Dict[Tuple[int, int], float]] = None,
        game_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Render board using Rich library to console.
        
        Args:
            board: Board array (8, 8)
            current_player: Current player (1 or -1)
            last_move: Optional last move to highlight
            q_values: Optional Q-values per square for overlay
            game_info: Optional game state information
        """
        if not self.rich_enabled:
            print(self.render_ascii(board, current_player, last_move))
            return
        
        table = Table(
            show_header=True,
            show_edge=True,
            box=box.HEAVY,
            padding=0,
        )
        
        # Add columns
        table.add_column("", justify="center", width=2)
        for col in "abcdefgh":
            table.add_column(col, justify="center", width=3)
        table.add_column("", justify="center", width=2)
        
        # Add rows
        for row in range(8):
            row_cells = [Text(str(8 - row), style="bold")]
            
            for col in range(8):
                cell_value = board[row, col]
                is_dark = (row + col) % 2 == 1
                
                # Get piece symbol
                symbol = self._get_piece_symbol(cell_value, row, col)
                
                # Determine style
                if cell_value == 1:
                    piece_style = STYLES["player1_piece"]
                elif cell_value == 2:
                    piece_style = STYLES["player1_king"]
                elif cell_value == -1:
                    piece_style = STYLES["player2_piece"]
                elif cell_value == -2:
                    piece_style = STYLES["player2_king"]
                else:
                    piece_style = Style()
                
                # Background style
                if last_move:
                    if (row, col) == tuple(last_move.get("from", [])):
                        bg_style = STYLES["highlight_from"]
                    elif (row, col) == tuple(last_move.get("to", [])):
                        bg_style = STYLES["highlight_to"]
                    elif (row, col) in [tuple(c) for c in last_move.get("captures", [])]:
                        bg_style = STYLES["highlight_capture"]
                    else:
                        bg_style = STYLES["dark_square"] if is_dark else STYLES["light_square"]
                else:
                    bg_style = STYLES["dark_square"] if is_dark else STYLES["light_square"]
                
                # Combine styles
                combined_style = piece_style + bg_style
                
                # Add Q-value overlay if provided
                if q_values and (row, col) in q_values:
                    q_val = q_values[(row, col)]
                    symbol = f"{symbol}\n{q_val:.2f}"
                
                row_cells.append(Text(f" {symbol} ", style=combined_style))
            
            row_cells.append(Text(str(8 - row), style="bold"))
            table.add_row(*row_cells)
        
        # Create panel with game info
        player_name = "Player 1 (Red)" if current_player == 1 else "Player 2 (Black)"
        title = f"[bold]Checkers - Turn: {player_name}[/bold]"
        
        if game_info:
            info_parts = []
            if "step" in game_info:
                info_parts.append(f"Step: {game_info['step']}")
            if "reward" in game_info:
                info_parts.append(f"Reward: {game_info['reward']:.3f}")
            if "epsilon" in game_info:
                info_parts.append(f"ε: {game_info['epsilon']:.3f}")
            if info_parts:
                title += f"\n[dim]{' | '.join(info_parts)}[/dim]"
        
        panel = Panel(table, title=title, border_style="blue")
        self.console.print(panel)
    
    def render_with_q_overlay(
        self,
        board: np.ndarray,
        legal_actions: List[Dict],
        q_values: List[float],
        current_player: int = 1,
    ) -> None:
        """Render board with Q-values shown for each legal action.
        
        Args:
            board: Board array
            legal_actions: List of legal actions
            q_values: Q-value for each legal action
            current_player: Current player
        """
        if not self.rich_enabled:
            # ASCII fallback
            lines = [self.render_ascii(board, current_player, None, legal_actions)]
            lines.append("\nActions with Q-values:")
            for i, (action, q) in enumerate(zip(legal_actions, q_values)):
                from_sq = action.get("from", [])
                to_sq = action.get("to", [])
                from_str = f"{chr(ord('a') + from_sq[1])}{8 - from_sq[0]}"
                to_str = f"{chr(ord('a') + to_sq[1])}{8 - to_sq[0]}"
                lines.append(f"  {i+1}. {from_str} → {to_str}: Q={q:.4f}")
            print("\n".join(lines))
            return
        
        # Build Q-value dictionary for squares
        from_q_values = {}
        for action, q in zip(legal_actions, q_values):
            from_sq = tuple(action.get("from", []))
            if from_sq not in from_q_values or q > from_q_values[from_sq]:
                from_q_values[from_sq] = q
        
        self.render_rich(board, current_player, None, from_q_values)
        
        # Print action details
        self.console.print("\n[bold]Legal Actions:[/bold]")
        table = Table(box=box.SIMPLE)
        table.add_column("#", style="dim")
        table.add_column("From")
        table.add_column("To")
        table.add_column("Q-Value", justify="right")
        table.add_column("Captures", style="red")
        
        # Sort by Q-value (descending)
        sorted_actions = sorted(
            zip(range(len(legal_actions)), legal_actions, q_values),
            key=lambda x: x[2],
            reverse=True,
        )
        
        for i, action, q in sorted_actions:
            from_sq = action.get("from", [])
            to_sq = action.get("to", [])
            captures = action.get("captures", [])
            
            from_str = f"{chr(ord('a') + from_sq[1])}{8 - from_sq[0]}"
            to_str = f"{chr(ord('a') + to_sq[1])}{8 - to_sq[0]}"
            cap_str = str(len(captures)) if captures else "-"
            
            q_style = "green" if q > 0 else "red" if q < 0 else "yellow"
            
            table.add_row(
                str(i + 1),
                from_str,
                to_str,
                Text(f"{q:.4f}", style=q_style),
                cap_str,
            )
        
        self.console.print(table)
    
    def render_game_summary(
        self,
        stats: Dict[str, Any],
        winner: Optional[int] = None,
    ) -> None:
        """Render end-of-game summary.
        
        Args:
            stats: Game statistics
            winner: Winner (1, -1, or 0 for draw)
        """
        if not self.rich_enabled:
            print("\n" + "=" * 50)
            print("GAME OVER")
            if winner == 1:
                print("Winner: Player 1")
            elif winner == -1:
                print("Winner: Player 2")
            else:
                print("Result: Draw")
            for key, value in stats.items():
                print(f"  {key}: {value}")
            print("=" * 50)
            return
        
        # Determine winner text
        if winner == 1:
            winner_text = "[green bold]Player 1 Wins![/green bold]"
        elif winner == -1:
            winner_text = "[blue bold]Player 2 Wins![/blue bold]"
        else:
            winner_text = "[yellow bold]Draw![/yellow bold]"
        
        # Build stats table
        table = Table(show_header=False, box=box.ROUNDED)
        table.add_column("Metric", style="dim")
        table.add_column("Value", style="bold")
        
        for key, value in stats.items():
            if isinstance(value, float):
                table.add_row(key, f"{value:.4f}")
            else:
                table.add_row(key, str(value))
        
        panel = Panel(
            table,
            title=f"[bold]Game Over - {winner_text}[/bold]",
            border_style="gold1",
        )
        self.console.print(panel)
    
    def _get_piece_symbol(
        self,
        cell_value: int,
        row: int,
        col: int,
    ) -> str:
        """Get the symbol for a cell value.
        
        Args:
            cell_value: Value in the cell
            row: Row index
            col: Column index
            
        Returns:
            Symbol string
        """
        if cell_value == 0:
            is_dark = (row + col) % 2 == 1
            return self.symbols["empty_dark"] if is_dark else self.symbols["empty_light"]
        elif cell_value == 1:
            return self.symbols["player1"]
        elif cell_value == 2:
            return self.symbols["player1_king"]
        elif cell_value == -1:
            return self.symbols["player2"]
        elif cell_value == -2:
            return self.symbols["player2_king"]
        else:
            return "?"


class EpisodeReplayRenderer:
    """Renderer for replaying recorded episodes.
    
    Provides step-by-step visualization of recorded game episodes.
    """
    
    def __init__(self, renderer: Optional[BoardRenderer] = None):
        """Initialize replay renderer.
        
        Args:
            renderer: Board renderer to use (creates default if None)
        """
        self.renderer = renderer or BoardRenderer()
        self.current_step = 0
    
    def replay_episode(
        self,
        states: List[np.ndarray],
        actions: List[Dict],
        rewards: List[float],
        delay: float = 1.0,
        interactive: bool = True,
    ) -> None:
        """Replay an episode step by step.
        
        Args:
            states: List of board states
            actions: List of actions taken
            rewards: List of rewards received
            delay: Delay between steps (seconds)
            interactive: If True, wait for input between steps
        """
        import time
        
        total_reward = 0.0
        
        for i, (state, action, reward) in enumerate(zip(states, actions, rewards)):
            total_reward += reward
            
            game_info = {
                "step": i + 1,
                "reward": reward,
                "total_reward": total_reward,
            }
            
            # Determine current player from step number
            current_player = 1 if i % 2 == 0 else -1
            
            # Clear console if using Rich
            if self.renderer.rich_enabled:
                self.renderer.console.clear()
            
            self.renderer.render_rich(
                state,
                current_player,
                action,
                game_info=game_info,
            )
            
            if interactive:
                input(f"\nStep {i+1}/{len(states)} - Press Enter to continue...")
            else:
                time.sleep(delay)
        
        # Show final state if available
        if len(states) > len(actions):
            final_state = states[-1]
            if self.renderer.rich_enabled:
                self.renderer.console.clear()
            self.renderer.render_rich(final_state, -current_player)
            print(f"\nEpisode complete! Total reward: {total_reward:.4f}")


def print_board(
    board: np.ndarray,
    current_player: int = 1,
    use_rich: bool = True,
) -> None:
    """Convenience function to print a board.
    
    Args:
        board: Board array
        current_player: Current player
        use_rich: Whether to use Rich rendering
    """
    renderer = BoardRenderer(use_rich=use_rich)
    if use_rich and renderer.rich_enabled:
        renderer.render_rich(board, current_player)
    else:
        print(renderer.render_ascii(board, current_player))
