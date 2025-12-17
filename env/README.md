# Módulo env - Entorno de Damas

## Propósito

Este módulo implementa el entorno del juego de damas compatible con la API de Gym/Gymnasium.

## Estructura

```
env/
├── checkers_env.py      # Clase principal CheckersEnv
├── rules.py             # Lógica de reglas del juego
├── representation.py    # Conversión de representaciones
├── utils.py            # Utilidades auxiliares
└── tests/              # Tests unitarios
    ├── test_legal_moves.py
    ├── test_terminal_states.py
    ├── test_rewards.py
    └── test_cases/     # Casos de test en JSON
```

## Uso Básico

```python
from env.checkers_env import CheckersEnv
import json

# Cargar configuración
with open("config/checkers_rules.json") as f:
    config = json.load(f)

# Crear entorno
env = CheckersEnv(config)
env.seed(42)  # Para reproducibilidad

# Resetear
obs = env.reset()
print(f"Observation shape: {obs.shape}")  # (4, 8, 8)

# Obtener acciones legales
legal_actions = env.get_legal_actions()
print(f"Legal actions: {len(legal_actions)}")

# Hacer un paso
action = legal_actions[0]
obs, reward, done, info = env.step(action)

# Renderizar
env.render(mode='ascii')
```

## API Principal

### CheckersEnv

**Métodos principales**:
- `reset()`: Resetea el entorno a estado inicial
- `step(action)`: Ejecuta una acción y retorna (obs, reward, done, info)
- `render(mode)`: Renderiza el tablero (ascii, rgb_array)
- `get_legal_actions()`: Retorna lista de acciones legales
- `seed(seed)`: Establece seed para reproducibilidad

## Representación de Estado

El estado se representa como tensor numpy de forma `(4, 8, 8)`:
- Canal 0: own men (piezas propias normales)
- Canal 1: own kings (reyes propios)
- Canal 2: opp men (piezas oponente normales)
- Canal 3: opp kings (reyes oponente)

## Estructura de Acción

```python
action = {
    "from": [row, col],      # Posición origen
    "to": [row, col],       # Posición destino
    "captures": [[r1, c1], [r2, c2], ...],  # Piezas capturadas
    "promotion": bool,      # Si se corona
    "sequence_length": int  # Número de saltos
}
```

## Dependencias

- numpy
- gymnasium

## Tests

Ejecutar tests:
```bash
pytest env/tests/
```

Con cobertura:
```bash
pytest env/tests/ --cov=env
```

## Documentación Adicional

- Ver `DESIGN.md` para decisiones de diseño
- Ver `docs/research/WORKFLOW_1_ENVIRONMENT_RESEARCH.md` para investigación
- Ver casos de test en `env/tests/test_cases/`

