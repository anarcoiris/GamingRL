"""Tests for BoardRenderer."""

import pytest
import numpy as np


class TestBoardRenderer:
    """Test suite for BoardRenderer."""
    
    @pytest.fixture
    def empty_board(self):
        """Create an empty board."""
        return np.zeros((8, 8), dtype=int)
    
    @pytest.fixture
    def initial_board(self):
        """Create initial checkers board setup."""
        board = np.zeros((8, 8), dtype=int)
        
        # Player 2 (black) pieces on rows 0-2
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row, col] = -1
        
        # Player 1 (white/red) pieces on rows 5-7
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row, col] = 1
        
        return board
    
    def test_initialization_default(self):
        """Test default initialization."""
        from viz.board_renderer import BoardRenderer
        
        renderer = BoardRenderer()
        assert renderer.use_unicode is True
    
    def test_initialization_ascii(self):
        """Test ASCII-only initialization."""
        from viz.board_renderer import BoardRenderer
        
        renderer = BoardRenderer(use_unicode=False, use_rich=False)
        assert renderer.use_unicode is False
        assert renderer.rich_enabled is False
    
    def test_render_ascii_empty(self, empty_board):
        """Test ASCII rendering of empty board."""
        from viz.board_renderer import BoardRenderer
        
        renderer = BoardRenderer(use_unicode=False, use_rich=False)
        result = renderer.render_ascii(empty_board)
        
        assert "a" in result  # Column labels
        assert "8" in result  # Row labels
        assert isinstance(result, str)
    
    def test_render_ascii_initial(self, initial_board):
        """Test ASCII rendering of initial board."""
        from viz.board_renderer import BoardRenderer
        
        renderer = BoardRenderer(use_unicode=False, use_rich=False)
        result = renderer.render_ascii(initial_board)
        
        # Should contain piece symbols
        assert "w" in result or "●" in result  # Player 1
        assert "b" in result or "○" in result  # Player 2
    
    def test_render_ascii_with_last_move(self, initial_board):
        """Test ASCII rendering with highlighted last move."""
        from viz.board_renderer import BoardRenderer
        
        renderer = BoardRenderer(use_unicode=False, use_rich=False)
        
        last_move = {
            "from": [5, 0],
            "to": [4, 1],
        }
        
        result = renderer.render_ascii(initial_board, last_move=last_move)
        
        # Should contain highlight markers
        assert "[" in result or ">" in result
    
    def test_get_piece_symbol(self, empty_board):
        """Test getting piece symbols."""
        from viz.board_renderer import BoardRenderer
        
        renderer = BoardRenderer(use_unicode=True)
        
        # Empty dark square
        symbol = renderer._get_piece_symbol(0, 1, 0)
        assert symbol == "·"
        
        # Empty light square
        symbol = renderer._get_piece_symbol(0, 0, 0)
        assert symbol == " "
        
        # Player 1 regular piece
        symbol = renderer._get_piece_symbol(1, 0, 0)
        assert symbol == "●"
        
        # Player 1 king
        symbol = renderer._get_piece_symbol(2, 0, 0)
        assert symbol == "♔"
        
        # Player 2 regular piece
        symbol = renderer._get_piece_symbol(-1, 0, 0)
        assert symbol == "○"
        
        # Player 2 king
        symbol = renderer._get_piece_symbol(-2, 0, 0)
        assert symbol == "♚"
    
    def test_print_board_function(self, initial_board):
        """Test convenience print_board function."""
        from viz.board_renderer import print_board
        
        # Should not raise
        print_board(initial_board, current_player=1, use_rich=False)


class TestEpisodeReplayRenderer:
    """Test suite for EpisodeReplayRenderer."""
    
    def test_initialization(self):
        """Test replay renderer initialization."""
        from viz.board_renderer import EpisodeReplayRenderer
        
        renderer = EpisodeReplayRenderer()
        assert renderer.current_step == 0
    
    def test_initialization_with_custom_renderer(self):
        """Test replay renderer with custom board renderer."""
        from viz.board_renderer import EpisodeReplayRenderer, BoardRenderer
        
        custom = BoardRenderer(use_unicode=False, use_rich=False)
        renderer = EpisodeReplayRenderer(renderer=custom)
        
        assert renderer.renderer is custom
