# Módulo ui - Interfaces de Usuario

## Propósito

Este módulo implementa interfaces de usuario para interactuar con el juego y el agente.

## Estructura

```
ui/
├── cli_rich.py         # CLI interactivo con Rich
├── pygame_board.py    # GUI con PyGame
└── game_controller.py # Controlador de juego
```

## Componentes

### cli_rich.py

CLI interactivo usando Rich para:
- Renderizado de tablero en terminal
- Visualización de Q-values
- Interacción por teclado
- Métricas en tiempo real

**Uso**:
```bash
python ui/cli_rich.py --agent checkpoints/model.pt
```

### pygame_board.py

GUI gráfica con PyGame para:
- Tablero visual interactivo
- Click para jugar
- Visualización de política del agente
- Replays de partidas

**Uso**:
```bash
python ui/pygame_board.py --agent checkpoints/model.pt
```

### game_controller.py

Controlador que maneja:
- Flujo de juego
- Interacción humano vs. agente
- Guardado de replays
- Estadísticas de partida

## Dependencias

- rich (para CLI)
- pygame (para GUI)
- numpy

## Documentación Adicional

- Ver `docs/research/WORKFLOW_4_GUI_RESEARCH.md` para investigación (cuando esté disponible)

