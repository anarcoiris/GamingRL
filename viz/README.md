# Módulo viz - Visualización

## Propósito

Este módulo proporciona herramientas de visualización para análisis de entrenamiento y comportamiento del agente.

## Estructura

```
viz/
├── tb_logger.py        # Logging a TensorBoard
├── hooks.py            # Hooks de PyTorch
├── live_plot.py        # Gráficos en tiempo real
└── board_renderer.py   # Renderizado de tablero
```

## Componentes

### tb_logger.py

Logger para TensorBoard:
- Métricas escalares (reward, loss, win rate)
- Histogramas de pesos y gradientes
- Imágenes del tablero
- Distribuciones de Q-values

**Uso**:
```python
from viz.tb_logger import TensorBoardLogger

logger = TensorBoardLogger(log_dir="logs/")
logger.log_scalar("reward", reward, step)
logger.log_histogram("weights", model.parameters(), step)
```

### hooks.py

Hooks de PyTorch para capturar:
- Activaciones de capas
- Gradientes
- Valores intermedios

**Uso**:
```python
from viz.hooks import register_activation_hooks

hooks = register_activation_hooks(model)
# ... forward pass ...
activations = hooks.get_activations()
```

### live_plot.py

Gráficos en tiempo real:
- Reward por episodio
- Win rate
- Loss
- Q-values

### board_renderer.py

Renderizado de tablero:
- Visualización ASCII
- Visualización con Rich
- Overlay de Q-values
- Resaltado de acciones

## Dependencias

- torch
- tensorboard
- matplotlib
- rich
- numpy

## Documentación Adicional

- Ver `docs/research/WORKFLOW_3_VISUALIZATION_RESEARCH.md` para investigación

