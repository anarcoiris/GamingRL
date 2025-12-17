"""Live plotting utilities for real-time training visualization.

This module provides matplotlib-based live plotting for training metrics
with non-blocking updates.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from collections import deque
import threading
import time


try:
    import matplotlib
    matplotlib.use('TkAgg')  # Use non-blocking backend
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    plt = None


class LivePlot:
    """Real-time plotting for training metrics.
    
    Provides non-blocking updates to matplotlib figures during training.
    
    Attributes:
        window_size: Number of data points to display
        update_interval: Milliseconds between plot updates
        metrics: Dictionary of metric name -> values
    """
    
    def __init__(
        self,
        window_size: int = 1000,
        update_interval: int = 100,
        figsize: Tuple[int, int] = (12, 8),
    ):
        """Initialize live plot.
        
        Args:
            window_size: Number of data points to keep
            update_interval: Update interval in milliseconds
            figsize: Figure size (width, height) in inches
        """
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError(
                "Matplotlib not available. Install with: pip install matplotlib"
            )
        
        self.window_size = window_size
        self.update_interval = update_interval
        self.figsize = figsize
        
        self.metrics: Dict[str, deque] = {}
        self.steps: deque = deque(maxlen=window_size)
        
        self.fig = None
        self.axes = None
        self.lines = {}
        self.animation = None
        self._running = False
        self._lock = threading.Lock()
    
    def add_metric(self, name: str) -> None:
        """Register a new metric to track.
        
        Args:
            name: Metric name
        """
        with self._lock:
            if name not in self.metrics:
                self.metrics[name] = deque(maxlen=self.window_size)
    
    def update(self, step: int, **kwargs) -> None:
        """Update metrics with new values.
        
        Args:
            step: Current training step
            **kwargs: Metric name -> value pairs
        """
        with self._lock:
            self.steps.append(step)
            for name, value in kwargs.items():
                if name not in self.metrics:
                    self.metrics[name] = deque(maxlen=self.window_size)
                self.metrics[name].append(value)
    
    def setup_plot(self, layout: Optional[Dict[str, List[str]]] = None) -> None:
        """Set up the plot layout.
        
        Args:
            layout: Dictionary mapping subplot name to list of metrics.
                    Example: {'Loss': ['loss'], 'Performance': ['reward', 'win_rate']}
        """
        if layout is None:
            # Default layout: one subplot per metric
            layout = {name: [name] for name in self.metrics.keys()}
        
        n_subplots = len(layout)
        if n_subplots == 0:
            n_subplots = 1
        
        n_cols = min(2, n_subplots)
        n_rows = (n_subplots + n_cols - 1) // n_cols
        
        self.fig, axes = plt.subplots(n_rows, n_cols, figsize=self.figsize)
        if n_subplots == 1:
            self.axes = [axes]
        else:
            self.axes = axes.flatten()
        
        # Initialize lines
        for idx, (subplot_name, metric_names) in enumerate(layout.items()):
            ax = self.axes[idx]
            ax.set_title(subplot_name)
            ax.set_xlabel('Step')
            ax.set_ylabel('Value')
            ax.grid(True, alpha=0.3)
            
            for metric_name in metric_names:
                line, = ax.plot([], [], label=metric_name)
                self.lines[metric_name] = (line, ax)
            
            if len(metric_names) > 1:
                ax.legend(loc='upper right')
        
        # Hide unused subplots
        for idx in range(len(layout), len(self.axes)):
            self.axes[idx].set_visible(False)
        
        plt.tight_layout()
    
    def _update_plot(self, frame) -> List:
        """Update function for animation.
        
        Args:
            frame: Animation frame number
            
        Returns:
            List of updated line objects
        """
        with self._lock:
            steps = list(self.steps)
            
            for name, (line, ax) in self.lines.items():
                if name in self.metrics:
                    values = list(self.metrics[name])
                    # Pad values if needed
                    while len(values) < len(steps):
                        values.insert(0, np.nan)
                    while len(values) > len(steps):
                        values = values[-len(steps):]
                    
                    line.set_data(steps[:len(values)], values)
            
            # Update axis limits
            for name, (line, ax) in self.lines.items():
                ax.relim()
                ax.autoscale_view()
        
        return [line for (line, _) in self.lines.values()]
    
    def start(self) -> None:
        """Start the live plotting animation."""
        if self.fig is None:
            self.setup_plot()
        
        self._running = True
        self.animation = FuncAnimation(
            self.fig,
            self._update_plot,
            interval=self.update_interval,
            blit=False,
            cache_frame_data=False,
        )
        plt.show(block=False)
        plt.pause(0.1)
    
    def stop(self) -> None:
        """Stop the live plotting animation."""
        self._running = False
        if self.animation is not None:
            self.animation.event_source.stop()
    
    def save_figure(self, filepath: str, dpi: int = 150) -> None:
        """Save the current figure to a file.
        
        Args:
            filepath: Path to save the figure
            dpi: Resolution in dots per inch
        """
        if self.fig is not None:
            self.fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    
    def close(self) -> None:
        """Close the figure window."""
        self.stop()
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None


class TrainingDashboard:
    """Comprehensive dashboard for DQN training visualization.
    
    Provides a multi-panel view of:
    - Loss and training metrics
    - Episode rewards and win rates
    - Q-value statistics
    - Exploration rate (epsilon)
    """
    
    def __init__(
        self,
        window_size: int = 500,
        update_interval: int = 200,
    ):
        """Initialize training dashboard.
        
        Args:
            window_size: Number of data points to display
            update_interval: Update interval in milliseconds
        """
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("Matplotlib not available.")
        
        self.window_size = window_size
        self.update_interval = update_interval
        
        # Metrics storage
        self.steps = deque(maxlen=window_size)
        self.losses = deque(maxlen=window_size)
        self.rewards = deque(maxlen=window_size)
        self.epsilons = deque(maxlen=window_size)
        self.q_means = deque(maxlen=window_size)
        self.q_maxs = deque(maxlen=window_size)
        self.win_rates = deque(maxlen=window_size)
        
        self.fig = None
        self.axes = None
        self.lines = {}
        self._lock = threading.Lock()
    
    def update(
        self,
        step: int,
        loss: Optional[float] = None,
        reward: Optional[float] = None,
        epsilon: Optional[float] = None,
        q_mean: Optional[float] = None,
        q_max: Optional[float] = None,
        win_rate: Optional[float] = None,
    ) -> None:
        """Update dashboard with new values.
        
        Args:
            step: Training step
            loss: Training loss
            reward: Episode reward
            epsilon: Current epsilon value
            q_mean: Mean Q-value
            q_max: Max Q-value
            win_rate: Rolling win rate
        """
        with self._lock:
            self.steps.append(step)
            
            if loss is not None:
                self.losses.append(loss)
            if reward is not None:
                self.rewards.append(reward)
            if epsilon is not None:
                self.epsilons.append(epsilon)
            if q_mean is not None:
                self.q_means.append(q_mean)
            if q_max is not None:
                self.q_maxs.append(q_max)
            if win_rate is not None:
                self.win_rates.append(win_rate)
    
    def setup(self) -> None:
        """Set up the dashboard layout."""
        self.fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        self.axes = axes.flatten()
        
        # Loss plot
        self.axes[0].set_title('Training Loss')
        self.axes[0].set_xlabel('Step')
        self.axes[0].set_ylabel('Loss')
        self.axes[0].grid(True, alpha=0.3)
        self.lines['loss'], = self.axes[0].plot([], [], 'b-', label='Loss')
        
        # Reward plot
        self.axes[1].set_title('Episode Reward')
        self.axes[1].set_xlabel('Step')
        self.axes[1].set_ylabel('Reward')
        self.axes[1].grid(True, alpha=0.3)
        self.lines['reward'], = self.axes[1].plot([], [], 'g-', label='Reward')
        
        # Q-values plot
        self.axes[2].set_title('Q-Values')
        self.axes[2].set_xlabel('Step')
        self.axes[2].set_ylabel('Q-Value')
        self.axes[2].grid(True, alpha=0.3)
        self.lines['q_mean'], = self.axes[2].plot([], [], 'r-', label='Mean Q')
        self.lines['q_max'], = self.axes[2].plot([], [], 'm-', label='Max Q')
        self.axes[2].legend()
        
        # Epsilon and Win Rate plot
        self.axes[3].set_title('Epsilon & Win Rate')
        self.axes[3].set_xlabel('Step')
        self.axes[3].set_ylabel('Value')
        self.axes[3].grid(True, alpha=0.3)
        self.lines['epsilon'], = self.axes[3].plot([], [], 'orange', label='Epsilon')
        self.lines['win_rate'], = self.axes[3].plot([], [], 'cyan', label='Win Rate')
        self.axes[3].legend()
        self.axes[3].set_ylim(0, 1.1)
        
        plt.tight_layout()
    
    def refresh(self) -> None:
        """Refresh the dashboard with current data."""
        with self._lock:
            steps = list(self.steps)
            
            # Update each line
            if self.losses:
                self.lines['loss'].set_data(steps[:len(self.losses)], list(self.losses))
            if self.rewards:
                self.lines['reward'].set_data(steps[:len(self.rewards)], list(self.rewards))
            if self.q_means:
                self.lines['q_mean'].set_data(steps[:len(self.q_means)], list(self.q_means))
            if self.q_maxs:
                self.lines['q_max'].set_data(steps[:len(self.q_maxs)], list(self.q_maxs))
            if self.epsilons:
                self.lines['epsilon'].set_data(steps[:len(self.epsilons)], list(self.epsilons))
            if self.win_rates:
                self.lines['win_rate'].set_data(steps[:len(self.win_rates)], list(self.win_rates))
            
            # Autoscale axes
            for i in range(4):
                self.axes[i].relim()
                self.axes[i].autoscale_view()
        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def show(self) -> None:
        """Display the dashboard window."""
        if self.fig is None:
            self.setup()
        plt.show(block=False)
        plt.pause(0.1)
    
    def save(self, filepath: str, dpi: int = 150) -> None:
        """Save dashboard to file.
        
        Args:
            filepath: Output file path
            dpi: Resolution
        """
        if self.fig is not None:
            self.fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    
    def close(self) -> None:
        """Close the dashboard window."""
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None


def create_training_plots(
    metrics_history: Dict[str, List[float]],
    save_path: Optional[str] = None,
    show: bool = True,
) -> None:
    """Create static training plots from metrics history.
    
    Args:
        metrics_history: Dictionary of metric name -> list of values
        save_path: Optional path to save the figure
        show: Whether to display the plot
    """
    if not MATPLOTLIB_AVAILABLE:
        print("Matplotlib not available for plotting.")
        return
    
    n_metrics = len(metrics_history)
    if n_metrics == 0:
        return
    
    n_cols = min(2, n_metrics)
    n_rows = (n_metrics + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 4 * n_rows))
    if n_metrics == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    for idx, (name, values) in enumerate(metrics_history.items()):
        ax = axes[idx]
        ax.plot(values, label=name)
        ax.set_title(name)
        ax.set_xlabel('Step')
        ax.set_ylabel('Value')
        ax.grid(True, alpha=0.3)
        
        # Add rolling average if enough data points
        if len(values) >= 100:
            window = min(100, len(values) // 5)
            rolling_avg = np.convolve(values, np.ones(window)/window, mode='valid')
            ax.plot(
                range(window-1, len(values)),
                rolling_avg,
                'r-',
                alpha=0.7,
                label=f'{window}-step avg',
            )
            ax.legend()
    
    # Hide unused subplots
    for idx in range(n_metrics, len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()
