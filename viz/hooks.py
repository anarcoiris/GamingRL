"""PyTorch hooks for capturing activations, gradients, and intermediate values.

This module provides utilities to attach hooks to PyTorch models for
monitoring and debugging neural network training.
"""

import torch
import torch.nn as nn
from typing import Dict, List, Optional, Callable, Any, Tuple
from collections import defaultdict
import numpy as np


class ActivationHook:
    """Hook for capturing layer activations during forward pass."""
    
    def __init__(self, name: str):
        """Initialize activation hook.
        
        Args:
            name: Name identifier for this hook
        """
        self.name = name
        self.activations: Optional[torch.Tensor] = None
    
    def __call__(
        self,
        module: nn.Module,
        input: Tuple[torch.Tensor, ...],
        output: torch.Tensor,
    ) -> None:
        """Hook callback for forward pass.
        
        Args:
            module: The module being hooked
            input: Input tensors
            output: Output tensor
        """
        self.activations = output.detach().cpu()
    
    def get_activations(self) -> Optional[torch.Tensor]:
        """Get captured activations.
        
        Returns:
            Captured activations tensor or None
        """
        return self.activations
    
    def clear(self) -> None:
        """Clear stored activations."""
        self.activations = None


class GradientHook:
    """Hook for capturing gradients during backward pass."""
    
    def __init__(self, name: str):
        """Initialize gradient hook.
        
        Args:
            name: Name identifier for this hook
        """
        self.name = name
        self.gradients: Optional[torch.Tensor] = None
    
    def __call__(
        self,
        module: nn.Module,
        grad_input: Tuple[Optional[torch.Tensor], ...],
        grad_output: Tuple[torch.Tensor, ...],
    ) -> None:
        """Hook callback for backward pass.
        
        Args:
            module: The module being hooked
            grad_input: Input gradients
            grad_output: Output gradients
        """
        if grad_output[0] is not None:
            self.gradients = grad_output[0].detach().cpu()
    
    def get_gradients(self) -> Optional[torch.Tensor]:
        """Get captured gradients.
        
        Returns:
            Captured gradients tensor or None
        """
        return self.gradients
    
    def clear(self) -> None:
        """Clear stored gradients."""
        self.gradients = None


class HookManager:
    """Manager for attaching and removing hooks from PyTorch models.
    
    Provides a clean interface for:
    - Registering forward hooks to capture activations
    - Registering backward hooks to capture gradients
    - Retrieving and analyzing captured data
    - Cleaning up hooks when done
    
    Attributes:
        model: The PyTorch model being monitored
        forward_hooks: Dictionary of activation hooks
        backward_hooks: Dictionary of gradient hooks
        handles: List of hook handles for cleanup
    """
    
    def __init__(self, model: nn.Module):
        """Initialize hook manager.
        
        Args:
            model: PyTorch model to attach hooks to
        """
        self.model = model
        self.forward_hooks: Dict[str, ActivationHook] = {}
        self.backward_hooks: Dict[str, GradientHook] = {}
        self.handles: List[torch.utils.hooks.RemovableHandle] = []
    
    def register_activation_hook(
        self,
        layer_name: str,
        layer: Optional[nn.Module] = None,
    ) -> ActivationHook:
        """Register a forward hook to capture activations.
        
        Args:
            layer_name: Name for this hook (for retrieval)
            layer: Layer to hook. If None, uses layer_name to find layer.
            
        Returns:
            The created activation hook
            
        Raises:
            ValueError: If layer cannot be found
        """
        if layer is None:
            layer = self._get_layer_by_name(layer_name)
        
        hook = ActivationHook(layer_name)
        handle = layer.register_forward_hook(hook)
        
        self.forward_hooks[layer_name] = hook
        self.handles.append(handle)
        
        return hook
    
    def register_gradient_hook(
        self,
        layer_name: str,
        layer: Optional[nn.Module] = None,
    ) -> GradientHook:
        """Register a backward hook to capture gradients.
        
        Args:
            layer_name: Name for this hook (for retrieval)
            layer: Layer to hook. If None, uses layer_name to find layer.
            
        Returns:
            The created gradient hook
            
        Raises:
            ValueError: If layer cannot be found
        """
        if layer is None:
            layer = self._get_layer_by_name(layer_name)
        
        hook = GradientHook(layer_name)
        handle = layer.register_full_backward_hook(hook)
        
        self.backward_hooks[layer_name] = hook
        self.handles.append(handle)
        
        return hook
    
    def register_all_conv_hooks(self) -> List[str]:
        """Register activation hooks on all convolutional layers.
        
        Returns:
            List of registered layer names
        """
        registered = []
        for name, module in self.model.named_modules():
            if isinstance(module, (nn.Conv2d, nn.Conv1d, nn.Conv3d)):
                self.register_activation_hook(name, module)
                registered.append(name)
        return registered
    
    def register_all_linear_hooks(self) -> List[str]:
        """Register activation hooks on all linear layers.
        
        Returns:
            List of registered layer names
        """
        registered = []
        for name, module in self.model.named_modules():
            if isinstance(module, nn.Linear):
                self.register_activation_hook(name, module)
                registered.append(name)
        return registered
    
    def register_all_hooks(self) -> List[str]:
        """Register activation hooks on all layers with parameters.
        
        Returns:
            List of registered layer names
        """
        registered = []
        for name, module in self.model.named_modules():
            if list(module.parameters()):
                # Skip if it's the root module or has no params
                if name and name not in self.forward_hooks:
                    try:
                        self.register_activation_hook(name, module)
                        registered.append(name)
                    except Exception:
                        pass  # Skip layers that can't be hooked
        return registered
    
    def get_activations(self, layer_name: str) -> Optional[torch.Tensor]:
        """Get activations for a specific layer.
        
        Args:
            layer_name: Name of the layer
            
        Returns:
            Activations tensor or None
        """
        if layer_name in self.forward_hooks:
            return self.forward_hooks[layer_name].get_activations()
        return None
    
    def get_all_activations(self) -> Dict[str, torch.Tensor]:
        """Get activations from all hooked layers.
        
        Returns:
            Dictionary of layer name -> activations
        """
        return {
            name: hook.get_activations()
            for name, hook in self.forward_hooks.items()
            if hook.get_activations() is not None
        }
    
    def get_gradients(self, layer_name: str) -> Optional[torch.Tensor]:
        """Get gradients for a specific layer.
        
        Args:
            layer_name: Name of the layer
            
        Returns:
            Gradients tensor or None
        """
        if layer_name in self.backward_hooks:
            return self.backward_hooks[layer_name].get_gradients()
        return None
    
    def get_all_gradients(self) -> Dict[str, torch.Tensor]:
        """Get gradients from all hooked layers.
        
        Returns:
            Dictionary of layer name -> gradients
        """
        return {
            name: hook.get_gradients()
            for name, hook in self.backward_hooks.items()
            if hook.get_gradients() is not None
        }
    
    def get_activation_statistics(self) -> Dict[str, Dict[str, float]]:
        """Compute statistics for all activations.
        
        Returns:
            Dictionary of layer name -> {mean, std, min, max, zeros_pct}
        """
        stats = {}
        for name, activations in self.get_all_activations().items():
            arr = activations.numpy()
            stats[name] = {
                "mean": float(np.mean(arr)),
                "std": float(np.std(arr)),
                "min": float(np.min(arr)),
                "max": float(np.max(arr)),
                "zeros_pct": float((arr == 0).mean() * 100),
            }
        return stats
    
    def check_dead_neurons(
        self,
        threshold: float = 0.95,
    ) -> Dict[str, float]:
        """Check for dead neurons (always zero activations).
        
        Args:
            threshold: Percentage threshold to consider a neuron dead
            
        Returns:
            Dictionary of layer name -> dead neuron percentage
        """
        dead_neurons = {}
        for name, activations in self.get_all_activations().items():
            arr = activations.numpy()
            # For each neuron (channel in conv, unit in linear)
            if len(arr.shape) >= 2:
                # Flatten all but first dimension
                flat = arr.reshape(arr.shape[0], -1)
                # Check if each neuron is always zero
                zero_ratio = (flat == 0).mean(axis=0)
                dead_pct = (zero_ratio > threshold).mean() * 100
                dead_neurons[name] = dead_pct
        return dead_neurons
    
    def clear_all(self) -> None:
        """Clear all stored activations and gradients."""
        for hook in self.forward_hooks.values():
            hook.clear()
        for hook in self.backward_hooks.values():
            hook.clear()
    
    def remove_all_hooks(self) -> None:
        """Remove all registered hooks."""
        for handle in self.handles:
            handle.remove()
        self.handles.clear()
        self.forward_hooks.clear()
        self.backward_hooks.clear()
    
    def _get_layer_by_name(self, name: str) -> nn.Module:
        """Get a layer from the model by name.
        
        Args:
            name: Layer name (dot-separated for nested modules)
            
        Returns:
            The requested module
            
        Raises:
            ValueError: If layer cannot be found
        """
        for module_name, module in self.model.named_modules():
            if module_name == name:
                return module
        raise ValueError(f"Layer '{name}' not found in model")
    
    def __enter__(self) -> "HookManager":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - removes all hooks."""
        self.remove_all_hooks()


def register_activation_hooks(
    model: nn.Module,
    layer_names: Optional[List[str]] = None,
) -> HookManager:
    """Convenience function to set up activation hooks.
    
    Args:
        model: PyTorch model
        layer_names: Optional list of layer names to hook.
                     If None, hooks all layers with parameters.
    
    Returns:
        HookManager with registered hooks
    """
    manager = HookManager(model)
    
    if layer_names is None:
        manager.register_all_hooks()
    else:
        for name in layer_names:
            manager.register_activation_hook(name)
    
    return manager


class ActivationVisualizer:
    """Utility for visualizing captured activations.
    
    Provides methods to create visualization-ready representations
    of neural network activations.
    """
    
    @staticmethod
    def to_grid(
        activations: torch.Tensor,
        normalize: bool = True,
        max_channels: int = 64,
    ) -> np.ndarray:
        """Convert activation tensor to a grid of feature maps.
        
        Args:
            activations: Activation tensor of shape (B, C, H, W)
            normalize: Whether to normalize values to [0, 1]
            max_channels: Maximum number of channels to include
            
        Returns:
            2D numpy array suitable for visualization
        """
        if activations is None:
            return None
        
        # Get first sample from batch
        if len(activations.shape) == 4:
            act = activations[0]  # (C, H, W)
        elif len(activations.shape) == 3:
            act = activations
        else:
            return None
        
        act = act.numpy()
        n_channels = min(act.shape[0], max_channels)
        
        # Calculate grid dimensions
        n_cols = int(np.ceil(np.sqrt(n_channels)))
        n_rows = int(np.ceil(n_channels / n_cols))
        
        # Normalize if requested
        if normalize:
            vmin, vmax = act.min(), act.max()
            if vmax > vmin:
                act = (act - vmin) / (vmax - vmin)
            else:
                act = act - vmin
        
        # Create grid
        h, w = act.shape[1], act.shape[2]
        grid = np.zeros((n_rows * h, n_cols * w))
        
        for i in range(n_channels):
            row = i // n_cols
            col = i % n_cols
            grid[row*h:(row+1)*h, col*w:(col+1)*w] = act[i]
        
        return grid
    
    @staticmethod
    def activation_histogram(
        activations: torch.Tensor,
        bins: int = 50,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Create histogram of activation values.
        
        Args:
            activations: Activation tensor
            bins: Number of histogram bins
            
        Returns:
            Tuple of (counts, bin_edges)
        """
        arr = activations.numpy().flatten()
        return np.histogram(arr, bins=bins)
