"""Visualization module for GamingRL project.

This module provides comprehensive visualization tools for:
- TensorBoard logging (tb_logger)
- PyTorch hooks for activation/gradient capture (hooks)
- Board rendering with Rich/ASCII support (board_renderer)
- Live plotting during training (live_plot)

Example usage:

    # TensorBoard logging
    from viz.tb_logger import TensorBoardLogger
    
    logger = TensorBoardLogger(log_dir="logs/experiment_1")
    logger.log_scalar("loss", loss_value, step)
    logger.log_training_metrics(loss, reward, epsilon, step)
    
    # Activation hooks
    from viz.hooks import HookManager
    
    with HookManager(model) as hooks:
        hooks.register_all_conv_hooks()
        output = model(input)
        activations = hooks.get_all_activations()
    
    # Board rendering
    from viz.board_renderer import BoardRenderer
    
    renderer = BoardRenderer()
    renderer.render_rich(board, current_player=1)
    
    # Live plotting
    from viz.live_plot import TrainingDashboard
    
    dashboard = TrainingDashboard()
    dashboard.setup()
    dashboard.show()
    dashboard.update(step, loss=loss, reward=reward)
    dashboard.refresh()
"""

__version__ = "0.1.0"

# Lazy imports to avoid loading heavy dependencies unless needed
__all__ = [
    # tb_logger
    "TensorBoardLogger",
    "TrainingMetricsTracker",
    # hooks
    "HookManager",
    "ActivationHook",
    "GradientHook",
    "register_activation_hooks",
    "ActivationVisualizer",
    # board_renderer
    "BoardRenderer",
    "EpisodeReplayRenderer",
    "print_board",
    # live_plot
    "LivePlot",
    "TrainingDashboard",
    "create_training_plots",
]


def __getattr__(name):
    """Lazy loading of module components."""
    if name in ("TensorBoardLogger", "TrainingMetricsTracker"):
        from viz.tb_logger import TensorBoardLogger, TrainingMetricsTracker
        return locals()[name]
    
    elif name in ("HookManager", "ActivationHook", "GradientHook", 
                  "register_activation_hooks", "ActivationVisualizer"):
        from viz.hooks import (
            HookManager, ActivationHook, GradientHook,
            register_activation_hooks, ActivationVisualizer
        )
        return locals()[name]
    
    elif name in ("BoardRenderer", "EpisodeReplayRenderer", "print_board"):
        from viz.board_renderer import (
            BoardRenderer, EpisodeReplayRenderer, print_board
        )
        return locals()[name]
    
    elif name in ("LivePlot", "TrainingDashboard", "create_training_plots"):
        from viz.live_plot import (
            LivePlot, TrainingDashboard, create_training_plots
        )
        return locals()[name]
    
    raise AttributeError(f"module 'viz' has no attribute '{name}'")
