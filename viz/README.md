# Módulo viz - Visualización

## Estado: ✅ IMPLEMENTADO (WORKFLOW 3)

Este módulo proporciona herramientas de visualización completas para análisis de entrenamiento y comportamiento del agente.

## Estructura

```
viz/
├── __init__.py          # Exports y lazy loading
├── tb_logger.py         # Logging a TensorBoard ✅
├── hooks.py             # Hooks de PyTorch ✅
├── board_renderer.py    # Renderizado de tablero ✅
├── live_plot.py         # Gráficos en tiempo real ✅
├── README.md            # Esta documentación
└── tests/               # Tests unitarios ✅
    ├── test_tb_logger.py
    ├── test_hooks.py
    └── test_board_renderer.py
```

## Componentes

### tb_logger.py - TensorBoard Logging

Logger para TensorBoard con soporte para:
- Métricas escalares (reward, loss, win rate)
- Histogramas de pesos y gradientes
- Imágenes del tablero
- Distribuciones de Q-values
- Hiperparámetros

**Uso básico**:
```python
from viz.tb_logger import TensorBoardLogger, TrainingMetricsTracker

# Logger para TensorBoard
logger = TensorBoardLogger(log_dir="logs/experiment_1")

# Log escalar
logger.log_scalar("training/loss", loss_value, step)

# Log de métricas de entrenamiento completas
logger.log_training_metrics(loss=0.5, reward=10.0, epsilon=0.1, step=100)

# Log histogramas de pesos del modelo
logger.log_model_weights(model, step)

# Log Q-values con estadísticas
logger.log_q_values(q_values_tensor, step)

# Cerrar al finalizar
logger.close()

# Tracker para promedios móviles
tracker = TrainingMetricsTracker(window_size=100)
tracker.add("loss", 0.5)
avg_loss = tracker.get_mean("loss")
```

### hooks.py - PyTorch Hooks

Hooks para capturar activaciones y gradientes:
- Análisis de activaciones por capa
- Detección de dead neurons
- Estadísticas de gradientes

**Uso básico**:
```python
from viz.hooks import HookManager, register_activation_hooks

# Con context manager (recomendado)
with HookManager(model) as hooks:
    hooks.register_all_conv_hooks()
    
    output = model(input)
    
    activations = hooks.get_all_activations()
    stats = hooks.get_activation_statistics()
    dead_neurons = hooks.check_dead_neurons()

# Función de conveniencia
manager = register_activation_hooks(model)
manager.remove_all_hooks()  # Limpiar al finalizar
```

### board_renderer.py - Renderizado de Tablero

Visualización del tablero con múltiples formatos:
- ASCII simple (terminal básica)
- Rich (colores, estilos, tablas)
- Overlay de Q-values
- Highlighting de acciones
- Replay de episodios

**Uso básico**:
```python
from viz.board_renderer import BoardRenderer, print_board

# Función de conveniencia
print_board(board, current_player=1, use_rich=True)

# Renderer con más control
renderer = BoardRenderer(use_unicode=True, use_rich=True)

# ASCII rendering
ascii_str = renderer.render_ascii(board, current_player, last_move)
print(ascii_str)

# Rich rendering (directo a consola)
renderer.render_rich(board, current_player, last_move, game_info={"step": 100})

# Q-value overlay
renderer.render_with_q_overlay(board, legal_actions, q_values, current_player)

# Game summary
renderer.render_game_summary(stats={"total_steps": 50}, winner=1)
```

### live_plot.py - Gráficos en Tiempo Real

Visualización en tiempo real con matplotlib:
- Gráficos dinámicos actualizables
- Dashboard completo de entrenamiento
- Generación de gráficos estáticos

**Uso básico**:
```python
from viz.live_plot import TrainingDashboard, create_training_plots

# Dashboard en tiempo real
dashboard = TrainingDashboard(window_size=500)
dashboard.setup()
dashboard.show()

# Durante entrenamiento
for step in range(num_steps):
    # ... training code ...
    dashboard.update(step, loss=loss, reward=reward, epsilon=epsilon)
    if step % 100 == 0:
        dashboard.refresh()

dashboard.save("training_progress.png")
dashboard.close()

# Gráficos estáticos desde historial
metrics_history = {
    "loss": losses,
    "reward": rewards,
}
create_training_plots(metrics_history, save_path="final_plots.png")
```

## Dependencias

- `torch` - PyTorch (requerido)
- `tensorboard` - TensorBoard logging (requerido para tb_logger)
- `numpy` - Operaciones numéricas (requerido)
- `rich` - Terminal styling (opcional, para board_renderer)
- `matplotlib` - Gráficos (opcional, para live_plot)

## Tests

Ejecutar tests:
```bash
pytest viz/tests/ -v
```

Coverage actual: **34 tests pasando** ✅

## Integración con Training Loop

Ejemplo de integración completa:
```python
from viz.tb_logger import TensorBoardLogger, TrainingMetricsTracker
from viz.hooks import HookManager
from viz.board_renderer import BoardRenderer

# Setup
logger = TensorBoardLogger(log_dir="logs/run_001")
tracker = TrainingMetricsTracker(window_size=100)
renderer = BoardRenderer()

# Training loop
for step in range(num_steps):
    # ... training step ...
    
    # Log metrics
    tracker.add("loss", loss)
    tracker.add("reward", reward)
    
    logger.log_training_metrics(loss, reward, epsilon, step)
    
    # Periodic detailed logging
    if step % 1000 == 0:
        logger.log_model_weights(agent.q_network, step)
        logger.log_q_values(q_values, step)
        
        # Capture activations
        with HookManager(agent.q_network) as hooks:
            hooks.register_all_conv_hooks()
            _ = agent.q_network(sample_obs)
            stats = hooks.get_activation_statistics()
            for layer, layer_stats in stats.items():
                logger.log_scalar(f"activations/{layer}/mean", layer_stats["mean"], step)

logger.close()
```

## Documentación Adicional

- Ver `docs/research/WORKFLOW_3_VISUALIZATION_RESEARCH.md` para investigación detallada
- TensorBoard: `python -m tensorboard.main --logdir=logs/`
