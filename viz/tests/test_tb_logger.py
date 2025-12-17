"""Tests for TensorBoardLogger and TrainingMetricsTracker."""

import pytest
import numpy as np
import tempfile
import shutil
from pathlib import Path

import torch
import torch.nn as nn


class TestTrainingMetricsTracker:
    """Test suite for TrainingMetricsTracker."""
    
    def test_add_and_get_mean(self):
        """Test adding metrics and getting mean."""
        from viz.tb_logger import TrainingMetricsTracker
        
        tracker = TrainingMetricsTracker(window_size=10)
        
        for i in range(5):
            tracker.add("loss", float(i))
        
        mean = tracker.get_mean("loss")
        assert mean is not None
        assert abs(mean - 2.0) < 0.01  # Mean of 0,1,2,3,4 = 2.0
    
    def test_window_size_limit(self):
        """Test that window size is enforced."""
        from viz.tb_logger import TrainingMetricsTracker
        
        tracker = TrainingMetricsTracker(window_size=5)
        
        for i in range(10):
            tracker.add("loss", float(i))
        
        # Should only have last 5 values: 5,6,7,8,9
        mean = tracker.get_mean("loss")
        assert mean is not None
        assert abs(mean - 7.0) < 0.01  # Mean of 5,6,7,8,9 = 7.0
    
    def test_get_latest(self):
        """Test getting the most recent value."""
        from viz.tb_logger import TrainingMetricsTracker
        
        tracker = TrainingMetricsTracker()
        
        tracker.add("reward", 1.0)
        tracker.add("reward", 2.0)
        tracker.add("reward", 3.0)
        
        latest = tracker.get_latest("reward")
        assert latest == 3.0
    
    def test_get_all_means(self):
        """Test getting means for all metrics."""
        from viz.tb_logger import TrainingMetricsTracker
        
        tracker = TrainingMetricsTracker()
        
        tracker.add("loss", 1.0)
        tracker.add("loss", 2.0)
        tracker.add("reward", 10.0)
        tracker.add("reward", 20.0)
        
        means = tracker.get_all_means()
        
        assert "loss" in means
        assert "reward" in means
        assert abs(means["loss"] - 1.5) < 0.01
        assert abs(means["reward"] - 15.0) < 0.01
    
    def test_reset(self):
        """Test resetting the tracker."""
        from viz.tb_logger import TrainingMetricsTracker
        
        tracker = TrainingMetricsTracker()
        
        tracker.add("loss", 1.0)
        tracker.reset()
        
        assert tracker.get_mean("loss") is None


class TestTensorBoardLogger:
    """Test suite for TensorBoardLogger."""
    
    @pytest.fixture
    def temp_log_dir(self):
        """Create a temporary directory for logs."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_initialization(self, temp_log_dir):
        """Test logger initialization."""
        from viz.tb_logger import TensorBoardLogger
        
        logger = TensorBoardLogger(log_dir=temp_log_dir)
        assert logger.step == 0
        assert logger.log_dir.exists()
        logger.close()
    
    def test_log_scalar(self, temp_log_dir):
        """Test logging scalar values."""
        from viz.tb_logger import TensorBoardLogger
        
        logger = TensorBoardLogger(log_dir=temp_log_dir)
        
        # Should not raise
        logger.log_scalar("test/loss", 0.5, step=0)
        logger.log_scalar("test/reward", 1.0, step=0)
        
        logger.close()
    
    def test_log_histogram(self, temp_log_dir):
        """Test logging histograms."""
        from viz.tb_logger import TensorBoardLogger
        
        logger = TensorBoardLogger(log_dir=temp_log_dir)
        
        values = np.random.randn(100)
        logger.log_histogram("test/distribution", values, step=0)
        
        # Also test with torch tensor
        tensor_values = torch.randn(100)
        logger.log_histogram("test/distribution_torch", tensor_values, step=0)
        
        logger.close()
    
    def test_log_model_weights(self, temp_log_dir):
        """Test logging model weights."""
        from viz.tb_logger import TensorBoardLogger
        
        logger = TensorBoardLogger(log_dir=temp_log_dir)
        
        model = nn.Sequential(
            nn.Linear(10, 5),
            nn.ReLU(),
            nn.Linear(5, 2),
        )
        
        logger.log_model_weights(model, step=0)
        logger.close()
    
    def test_increment_step(self, temp_log_dir):
        """Test step counter incrementing."""
        from viz.tb_logger import TensorBoardLogger
        
        logger = TensorBoardLogger(log_dir=temp_log_dir)
        
        assert logger.step == 0
        logger.increment_step()
        assert logger.step == 1
        logger.increment_step(5)
        assert logger.step == 6
        
        logger.close()
    
    def test_context_manager(self, temp_log_dir):
        """Test using logger as context manager."""
        from viz.tb_logger import TensorBoardLogger
        
        with TensorBoardLogger(log_dir=temp_log_dir) as logger:
            logger.log_scalar("test", 1.0, 0)
        
        # Should be closed after exiting context
    
    def test_log_training_metrics(self, temp_log_dir):
        """Test convenience method for training metrics."""
        from viz.tb_logger import TensorBoardLogger
        
        logger = TensorBoardLogger(log_dir=temp_log_dir)
        
        logger.log_training_metrics(
            loss=0.5,
            reward=10.0,
            epsilon=0.1,
            step=100,
            extra_metrics={"win_rate": 0.6},
        )
        
        logger.close()
    
    def test_log_q_values(self, temp_log_dir):
        """Test logging Q-value statistics."""
        from viz.tb_logger import TensorBoardLogger
        
        logger = TensorBoardLogger(log_dir=temp_log_dir)
        
        q_values = np.array([0.5, 0.8, 0.3, 0.9, 0.1])
        logger.log_q_values(q_values, step=0)
        
        logger.close()
