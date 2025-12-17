"""Tests for PyTorch hooks module."""

import pytest
import torch
import torch.nn as nn
import numpy as np


class TestActivationHook:
    """Test suite for ActivationHook."""
    
    def test_capture_activations(self):
        """Test that hook captures activations."""
        from viz.hooks import ActivationHook
        
        hook = ActivationHook("test_layer")
        
        # Create a simple module and register hook
        layer = nn.Linear(10, 5)
        handle = layer.register_forward_hook(hook)
        
        # Forward pass
        x = torch.randn(2, 10)
        output = layer(x)
        
        # Check activations were captured
        activations = hook.get_activations()
        assert activations is not None
        assert activations.shape == (2, 5)
        
        handle.remove()
    
    def test_clear_activations(self):
        """Test clearing stored activations."""
        from viz.hooks import ActivationHook
        
        hook = ActivationHook("test")
        hook.activations = torch.randn(10)
        
        hook.clear()
        assert hook.get_activations() is None


class TestGradientHook:
    """Test suite for GradientHook."""
    
    def test_capture_gradients(self):
        """Test that hook captures gradients."""
        from viz.hooks import GradientHook
        
        hook = GradientHook("test_layer")
        
        # Create a simple module
        layer = nn.Linear(10, 5)
        handle = layer.register_full_backward_hook(hook)
        
        # Forward and backward pass
        x = torch.randn(2, 10, requires_grad=True)
        output = layer(x)
        loss = output.sum()
        loss.backward()
        
        # Check gradients were captured
        gradients = hook.get_gradients()
        assert gradients is not None
        assert gradients.shape == output.shape
        
        handle.remove()


class TestHookManager:
    """Test suite for HookManager."""
    
    @pytest.fixture
    def simple_model(self):
        """Create a simple model for testing."""
        return nn.Sequential(
            nn.Conv2d(4, 16, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(32 * 8 * 8, 64),
            nn.ReLU(),
            nn.Linear(64, 10),
        )
    
    def test_register_activation_hook(self, simple_model):
        """Test registering a single activation hook."""
        from viz.hooks import HookManager
        
        manager = HookManager(simple_model)
        hook = manager.register_activation_hook("0", simple_model[0])
        
        # Forward pass
        x = torch.randn(1, 4, 8, 8)
        output = simple_model(x)
        
        activations = manager.get_activations("0")
        assert activations is not None
        assert activations.shape == (1, 16, 8, 8)
        
        manager.remove_all_hooks()
    
    def test_register_all_conv_hooks(self, simple_model):
        """Test registering hooks on all conv layers."""
        from viz.hooks import HookManager
        
        manager = HookManager(simple_model)
        registered = manager.register_all_conv_hooks()
        
        assert len(registered) == 2  # Two Conv2d layers
        
        # Forward pass
        x = torch.randn(1, 4, 8, 8)
        simple_model(x)
        
        all_activations = manager.get_all_activations()
        assert len(all_activations) == 2
        
        manager.remove_all_hooks()
    
    def test_register_all_linear_hooks(self, simple_model):
        """Test registering hooks on all linear layers."""
        from viz.hooks import HookManager
        
        manager = HookManager(simple_model)
        registered = manager.register_all_linear_hooks()
        
        assert len(registered) == 2  # Two Linear layers
        
        manager.remove_all_hooks()
    
    def test_context_manager(self, simple_model):
        """Test using HookManager as context manager."""
        from viz.hooks import HookManager
        
        with HookManager(simple_model) as manager:
            manager.register_all_conv_hooks()
            
            x = torch.randn(1, 4, 8, 8)
            simple_model(x)
            
            activations = manager.get_all_activations()
            assert len(activations) > 0
        
        # After context exit, hooks should be removed
        assert len(manager.handles) == 0
    
    def test_activation_statistics(self, simple_model):
        """Test computing activation statistics."""
        from viz.hooks import HookManager
        
        manager = HookManager(simple_model)
        manager.register_all_conv_hooks()
        
        x = torch.randn(1, 4, 8, 8)
        simple_model(x)
        
        stats = manager.get_activation_statistics()
        
        for layer_name, layer_stats in stats.items():
            assert "mean" in layer_stats
            assert "std" in layer_stats
            assert "min" in layer_stats
            assert "max" in layer_stats
            assert "zeros_pct" in layer_stats
        
        manager.remove_all_hooks()
    
    def test_clear_all(self, simple_model):
        """Test clearing all stored values."""
        from viz.hooks import HookManager
        
        manager = HookManager(simple_model)
        manager.register_all_conv_hooks()
        
        x = torch.randn(1, 4, 8, 8)
        simple_model(x)
        
        # Verify activations exist
        assert len(manager.get_all_activations()) > 0
        
        manager.clear_all()
        
        # Verify activations are cleared
        assert len(manager.get_all_activations()) == 0
        
        manager.remove_all_hooks()


class TestActivationVisualizer:
    """Test suite for ActivationVisualizer."""
    
    def test_to_grid(self):
        """Test converting activations to grid."""
        from viz.hooks import ActivationVisualizer
        
        # Create fake activations (batch, channels, height, width)
        activations = torch.randn(1, 16, 8, 8)
        
        grid = ActivationVisualizer.to_grid(activations, max_channels=16)
        
        assert grid is not None
        # Grid should be reshaped appropriately
        assert len(grid.shape) == 2
    
    def test_activation_histogram(self):
        """Test creating histogram from activations."""
        from viz.hooks import ActivationVisualizer
        
        activations = torch.randn(1, 16, 8, 8)
        
        counts, bin_edges = ActivationVisualizer.activation_histogram(activations)
        
        assert len(counts) == 50  # Default bins
        assert len(bin_edges) == 51


class TestRegisterActivationHooks:
    """Test convenience function."""
    
    def test_register_activation_hooks(self):
        """Test the convenience function."""
        from viz.hooks import register_activation_hooks
        
        model = nn.Sequential(
            nn.Linear(10, 5),
            nn.ReLU(),
            nn.Linear(5, 2),
        )
        
        manager = register_activation_hooks(model)
        
        x = torch.randn(2, 10)
        model(x)
        
        activations = manager.get_all_activations()
        assert len(activations) > 0
        
        manager.remove_all_hooks()
