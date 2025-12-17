"""TensorBoard logging utilities for training visualization.

This module provides a structured interface for logging training metrics,
model weights, and visualizations to TensorBoard.
"""

import os
from pathlib import Path
from typing import Dict, Optional, Union, List, Any
import numpy as np

try:
    from torch.utils.tensorboard import SummaryWriter
    TENSORBOARD_AVAILABLE = True
except ImportError:
    TENSORBOARD_AVAILABLE = False
    SummaryWriter = None

import torch
import torch.nn as nn


class TensorBoardLogger:
    """Logger for TensorBoard visualization.
    
    Provides structured logging for:
    - Scalar metrics (loss, reward, win rate, epsilon)
    - Histograms (weights, gradients, Q-values)
    - Images (board states)
    - Custom visualizations
    
    Attributes:
        log_dir: Directory for TensorBoard logs
        writer: TensorBoard SummaryWriter instance
        step: Global step counter
    """
    
    def __init__(
        self,
        log_dir: str = "logs/tensorboard",
        experiment_name: Optional[str] = None,
        flush_secs: int = 30,
    ):
        """Initialize TensorBoard logger.
        
        Args:
            log_dir: Base directory for logs
            experiment_name: Optional experiment name (subdirectory)
            flush_secs: How often to flush to disk
        """
        if not TENSORBOARD_AVAILABLE:
            raise ImportError(
                "TensorBoard not available. Install with: pip install tensorboard"
            )
        
        self.log_dir = Path(log_dir)
        if experiment_name:
            self.log_dir = self.log_dir / experiment_name
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.writer = SummaryWriter(
            log_dir=str(self.log_dir),
            flush_secs=flush_secs,
        )
        self.step = 0
        self._custom_scalars_layout = {}
    
    def log_scalar(
        self,
        tag: str,
        value: float,
        step: Optional[int] = None,
    ) -> None:
        """Log a scalar value.
        
        Args:
            tag: Metric name (e.g., 'loss', 'reward')
            value: Metric value
            step: Global step (uses internal counter if None)
        """
        if step is None:
            step = self.step
        self.writer.add_scalar(tag, value, step)
    
    def log_scalars(
        self,
        main_tag: str,
        tag_scalar_dict: Dict[str, float],
        step: Optional[int] = None,
    ) -> None:
        """Log multiple related scalars.
        
        Args:
            main_tag: Main category name
            tag_scalar_dict: Dictionary of tag -> value
            step: Global step
        """
        if step is None:
            step = self.step
        self.writer.add_scalars(main_tag, tag_scalar_dict, step)
    
    def log_histogram(
        self,
        tag: str,
        values: Union[torch.Tensor, np.ndarray],
        step: Optional[int] = None,
        bins: str = "tensorflow",
    ) -> None:
        """Log a histogram of values.
        
        Args:
            tag: Histogram name
            values: Values to histogram
            step: Global step
            bins: Binning strategy
        """
        if step is None:
            step = self.step
        
        if isinstance(values, torch.Tensor):
            values = values.detach().cpu().numpy()
        
        self.writer.add_histogram(tag, values, step, bins=bins)
    
    def log_model_weights(
        self,
        model: nn.Module,
        step: Optional[int] = None,
        prefix: str = "weights",
    ) -> None:
        """Log histograms of all model weights.
        
        Args:
            model: PyTorch model
            step: Global step
            prefix: Tag prefix for weights
        """
        if step is None:
            step = self.step
        
        for name, param in model.named_parameters():
            if param.requires_grad:
                self.log_histogram(
                    f"{prefix}/{name}",
                    param.data,
                    step,
                )
    
    def log_model_gradients(
        self,
        model: nn.Module,
        step: Optional[int] = None,
        prefix: str = "gradients",
    ) -> None:
        """Log histograms of all model gradients.
        
        Args:
            model: PyTorch model
            step: Global step
            prefix: Tag prefix for gradients
        """
        if step is None:
            step = self.step
        
        for name, param in model.named_parameters():
            if param.requires_grad and param.grad is not None:
                self.log_histogram(
                    f"{prefix}/{name}",
                    param.grad.data,
                    step,
                )
                # Also log gradient norm
                grad_norm = param.grad.data.norm(2).item()
                self.log_scalar(f"{prefix}_norm/{name}", grad_norm, step)
    
    def log_image(
        self,
        tag: str,
        image: Union[torch.Tensor, np.ndarray],
        step: Optional[int] = None,
        dataformats: str = "CHW",
    ) -> None:
        """Log an image.
        
        Args:
            tag: Image tag
            image: Image tensor (C, H, W) or (H, W, C)
            step: Global step
            dataformats: Format of the image tensor
        """
        if step is None:
            step = self.step
        
        if isinstance(image, np.ndarray):
            image = torch.from_numpy(image)
        
        self.writer.add_image(tag, image, step, dataformats=dataformats)
    
    def log_figure(
        self,
        tag: str,
        figure,
        step: Optional[int] = None,
        close: bool = True,
    ) -> None:
        """Log a matplotlib figure.
        
        Args:
            tag: Figure tag
            figure: Matplotlib figure
            step: Global step
            close: Whether to close the figure after logging
        """
        if step is None:
            step = self.step
        
        self.writer.add_figure(tag, figure, step, close=close)
    
    def log_text(
        self,
        tag: str,
        text: str,
        step: Optional[int] = None,
    ) -> None:
        """Log text.
        
        Args:
            tag: Text tag
            text: Text content
            step: Global step
        """
        if step is None:
            step = self.step
        
        self.writer.add_text(tag, text, step)
    
    def log_hyperparameters(
        self,
        hparams: Dict[str, Any],
        metrics: Optional[Dict[str, float]] = None,
    ) -> None:
        """Log hyperparameters.
        
        Args:
            hparams: Dictionary of hyperparameters
            metrics: Optional dictionary of final metrics
        """
        if metrics is None:
            metrics = {}
        
        self.writer.add_hparams(hparams, metrics)
    
    def log_training_metrics(
        self,
        loss: float,
        reward: float,
        epsilon: float,
        step: Optional[int] = None,
        extra_metrics: Optional[Dict[str, float]] = None,
    ) -> None:
        """Log common training metrics.
        
        Convenience method for logging standard DQN training metrics.
        
        Args:
            loss: Training loss
            reward: Episode reward
            epsilon: Current epsilon value
            step: Global step
            extra_metrics: Additional metrics to log
        """
        if step is None:
            step = self.step
        
        self.log_scalar("training/loss", loss, step)
        self.log_scalar("training/reward", reward, step)
        self.log_scalar("training/epsilon", epsilon, step)
        
        if extra_metrics:
            for name, value in extra_metrics.items():
                self.log_scalar(f"training/{name}", value, step)
    
    def log_evaluation_metrics(
        self,
        win_rate: float,
        avg_reward: float,
        avg_episode_length: float,
        step: Optional[int] = None,
        extra_metrics: Optional[Dict[str, float]] = None,
    ) -> None:
        """Log evaluation metrics.
        
        Args:
            win_rate: Win rate percentage
            avg_reward: Average reward
            avg_episode_length: Average episode length
            step: Global step
            extra_metrics: Additional metrics
        """
        if step is None:
            step = self.step
        
        self.log_scalar("evaluation/win_rate", win_rate, step)
        self.log_scalar("evaluation/avg_reward", avg_reward, step)
        self.log_scalar("evaluation/avg_episode_length", avg_episode_length, step)
        
        if extra_metrics:
            for name, value in extra_metrics.items():
                self.log_scalar(f"evaluation/{name}", value, step)
    
    def log_q_values(
        self,
        q_values: Union[torch.Tensor, np.ndarray],
        step: Optional[int] = None,
    ) -> None:
        """Log Q-value statistics.
        
        Args:
            q_values: Tensor of Q-values
            step: Global step
        """
        if step is None:
            step = self.step
        
        if isinstance(q_values, torch.Tensor):
            q_values = q_values.detach().cpu().numpy()
        
        self.log_scalar("q_values/mean", np.mean(q_values), step)
        self.log_scalar("q_values/max", np.max(q_values), step)
        self.log_scalar("q_values/min", np.min(q_values), step)
        self.log_scalar("q_values/std", np.std(q_values), step)
        self.log_histogram("q_values/distribution", q_values, step)
    
    def increment_step(self, n: int = 1) -> None:
        """Increment the global step counter.
        
        Args:
            n: Number of steps to increment
        """
        self.step += n
    
    def set_step(self, step: int) -> None:
        """Set the global step counter.
        
        Args:
            step: New step value
        """
        self.step = step
    
    def flush(self) -> None:
        """Flush buffered data to disk."""
        self.writer.flush()
    
    def close(self) -> None:
        """Close the TensorBoard writer."""
        self.writer.close()
    
    def __enter__(self) -> "TensorBoardLogger":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()


class TrainingMetricsTracker:
    """Track and aggregate training metrics over windows.
    
    Provides rolling averages and statistics for training metrics.
    """
    
    def __init__(self, window_size: int = 100):
        """Initialize metrics tracker.
        
        Args:
            window_size: Size of rolling window for averages
        """
        self.window_size = window_size
        self.metrics: Dict[str, List[float]] = {}
    
    def add(self, name: str, value: float) -> None:
        """Add a metric value.
        
        Args:
            name: Metric name
            value: Metric value
        """
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append(value)
        
        # Keep only window_size most recent values
        if len(self.metrics[name]) > self.window_size:
            self.metrics[name] = self.metrics[name][-self.window_size:]
    
    def get_mean(self, name: str) -> Optional[float]:
        """Get rolling mean for a metric.
        
        Args:
            name: Metric name
            
        Returns:
            Rolling mean or None if no data
        """
        if name not in self.metrics or not self.metrics[name]:
            return None
        return np.mean(self.metrics[name])
    
    def get_std(self, name: str) -> Optional[float]:
        """Get rolling standard deviation for a metric.
        
        Args:
            name: Metric name
            
        Returns:
            Rolling std or None if no data
        """
        if name not in self.metrics or not self.metrics[name]:
            return None
        return np.std(self.metrics[name])
    
    def get_latest(self, name: str) -> Optional[float]:
        """Get the most recent value for a metric.
        
        Args:
            name: Metric name
            
        Returns:
            Latest value or None if no data
        """
        if name not in self.metrics or not self.metrics[name]:
            return None
        return self.metrics[name][-1]
    
    def get_all_means(self) -> Dict[str, float]:
        """Get rolling means for all metrics.
        
        Returns:
            Dictionary of metric name -> mean
        """
        return {
            name: np.mean(values)
            for name, values in self.metrics.items()
            if values
        }
    
    def reset(self) -> None:
        """Reset all metrics."""
        self.metrics.clear()
