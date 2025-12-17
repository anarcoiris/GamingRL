# GamingRL - Documentación para Claude Code

## Descripción del Proyecto

GamingRL es un proyecto de investigación y desarrollo para construir un agente DQN (Deep Q-Network) que aprenda a jugar damas (checkers), con visualización profunda de pesos, gradientes y dinámica matemática, y escalado progresivo hacia sistemas más complejos tipo StarCraft.

## Estructura de Directorios

```
GamingRL/
├── config/              # Archivos de configuración
│   ├── checkers_rules.json    # Reglas del juego
│   ├── training/              # Configs de entrenamiento
│   └── experiments/           # Configs de experimentos
├── env/                 # Entornos (Gym-like)
│   ├── checkers_env.py        # Entorno principal
│   ├── rules.py               # Lógica de reglas
│   ├── representation.py      # Representación de estado
│   └── tests/                 # Tests del entorno
├── agent/               # Agentes RL
│   ├── dqn.py                 # Agente DQN
│   ├── network.py            # Arquitectura de red
│   └── replay_buffer.py      # Buffer de experiencias
├── training/            # Scripts de entrenamiento
│   ├── train_dqn.py           # Loop de entrenamiento
│   └── evaluate.py            # Evaluación de agentes
├── viz/                 # Visualización
│   ├── tb_logger.py           # TensorBoard logging
│   ├── hooks.py               # Hooks de PyTorch
│   └── board_renderer.py      # Renderizado de tablero
├── ui/                  # Interfaces de usuario
│   ├── cli_rich.py            # CLI con Rich
│   └── pygame_board.py        # GUI con PyGame
├── experiments/         # Experimentos
│   ├── configs/               # Configuraciones
│   ├── results/               # Resultados
│   └── replays/               # Partidas guardadas
├── docs/                # Documentación
│   ├── research/              # Investigación temática
│   ├── guides/               # Guías de uso
│   └── api/                  # Referencia de API
└── tests/               # Tests unitarios e integración
```

## Patrones Comunes de Código

### Representación de Estado

El estado se representa como un tensor numpy de forma `(4, 8, 8)` con dtype `float32`:

```python
obs = np.zeros((4, 8, 8), dtype=np.float32)
# Canal 0: own men (piezas propias normales)
# Canal 1: own kings (reyes propios)
# Canal 2: opp men (piezas oponente normales)
# Canal 3: opp kings (reyes oponente)
```

**Valores del tablero interno**:
- `0`: casilla vacía
- `1`: jugador 1 (men)
- `2`: jugador 1 (king)
- `-1`: jugador -1 (men)
- `-2`: jugador -1 (king)

### Estructura de Acción

Las acciones se representan como diccionarios JSON serializables:

```python
action = {
    "from": [row, col],           # Posición origen
    "to": [row, col],             # Posición destino final
    "captures": [                 # Lista de posiciones capturadas
        [row1, col1],
        [row2, col2],
        ...
    ],
    "promotion": bool,            # Si se corona en este movimiento
    "sequence_length": int        # Número de saltos (1 = movimiento simple)
}
```

### Convenciones de Nomenclatura

- **Clases**: PascalCase (`CheckersEnv`, `DQNAgent`)
- **Funciones/Métodos**: snake_case (`get_legal_actions`, `compute_reward`)
- **Constantes**: UPPER_SNAKE_CASE (`MAX_EPISODE_STEPS`)
- **Variables**: snake_case (`current_player`, `board_state`)

### Manejo de Errores

Siempre validar inputs y proporcionar mensajes de error claros:

```python
def step(self, action: Dict) -> Tuple:
    if action not in self.get_legal_actions():
        raise ValueError(f"Action {action} is not legal in current state")
    # ... resto de la implementación
```

### Determinismo

Todo debe ser reproducible con seed:

```python
def seed(self, seed: Optional[int] = None):
    random.seed(seed)
    np.random.seed(seed)
    self._seed = seed
```

## Errores Comunes a Evitar

### 1. No Validar Acciones Legales

❌ **Mal**:
```python
def step(self, action):
    # Aplicar acción sin validar
    self._apply_action(action)
```

✅ **Bien**:
```python
def step(self, action):
    legal_actions = self.get_legal_actions()
    if action not in legal_actions:
        raise ValueError(f"Action {action} not in legal actions")
    self._apply_action(action)
```

### 2. Olvidar Captura Forzada

❌ **Mal**:
```python
def get_legal_actions(self):
    # Retornar todos los movimientos sin filtrar capturas
    return all_moves
```

✅ **Bien**:
```python
def get_legal_actions(self):
    capture_moves = self._get_capture_moves()
    if capture_moves:
        # Si hay capturas, solo retornar capturas
        if self.config["prefer_longest_capture"]:
            max_len = max(len(m.captures) for m in capture_moves)
            return [m for m in capture_moves if len(m.captures) == max_len]
        return capture_moves
    return self._get_simple_moves()
```

### 3. No Manejar Multi-jump Correctamente

❌ **Mal**:
```python
# Solo buscar capturas de un salto
def _get_captures(self, from_pos):
    # ...
```

✅ **Bien**:
```python
# Buscar capturas recursivamente para multi-jump
def _get_captures_recursive(self, board, from_pos, player, captures_so_far):
    # Implementar backtracking para encontrar todas las secuencias
    # ...
```

### 4. No Actualizar Target Network

❌ **Mal**:
```python
# Entrenar sin actualizar target network
for step in range(num_steps):
    loss = compute_loss(...)
    optimizer.step()
    # Falta actualizar target network
```

✅ **Bien**:
```python
for step in range(num_steps):
    loss = compute_loss(...)
    optimizer.step()
    
    if step % target_update_frequency == 0:
        target_net.load_state_dict(policy_net.state_dict())
```

### 5. No Manejar Acciones Legales Variables

❌ **Mal**:
```python
# Asumir tamaño fijo de acciones
q_values = network(obs)  # Shape: (200,)
action = argmax(q_values)  # Puede elegir acción inválida
```

✅ **Bien**:
```python
# Evaluar solo acciones legales
legal_actions = env.get_legal_actions()
q_values = network(obs, legal_actions)  # Solo evalúa legales
action_idx = argmax(q_values)
action = legal_actions[action_idx]
```

## Cómo Trabajar con Cada Módulo

### Módulo `env/`

**Propósito**: Implementar el entorno del juego de damas compatible con Gym/Gymnasium.

**Archivos principales**:
- `checkers_env.py`: Clase principal `CheckersEnv` con métodos `reset()`, `step()`, `render()`
- `rules.py`: Lógica de reglas del juego (movimientos, capturas, coronación)
- `representation.py`: Conversión entre representaciones internas y observaciones

**Patrones**:
- Siempre validar acciones antes de aplicarlas
- Mantener estado interno consistente
- Implementar `get_legal_actions()` que retorne lista de acciones serializables
- Usar seed para determinismo

**Ejemplo de uso**:
```python
from env.checkers_env import CheckersEnv
import json

with open("config/checkers_rules.json") as f:
    config = json.load(f)

env = CheckersEnv(config)
obs = env.reset()
legal_actions = env.get_legal_actions()
action = legal_actions[0]  # Elegir primera acción legal
obs, reward, done, info = env.step(action)
```

### Módulo `agent/`

**Propósito**: Implementar agentes de RL (DQN y variantes).

**Archivos principales**:
- `dqn.py`: Clase `DQNAgent` con métodos `select_action()`, `train_step()`, `update_target()`
- `network.py`: Arquitectura de red neuronal (CNN para tablero)
- `replay_buffer.py`: Buffer de experiencias para muestreo

**Patrones**:
- Usar acciones dinámicas (evaluar solo acciones legales)
- Implementar epsilon-greedy para exploración
- Actualizar target network periódicamente
- Guardar/load checkpoints

**Ejemplo de uso**:
```python
from agent.dqn import DQNAgent

agent = DQNAgent(
    state_shape=(4, 8, 8),
    learning_rate=1e-4,
    gamma=0.99
)

action = agent.select_action(obs, legal_actions, epsilon=0.1)
agent.store_transition(obs, action, reward, next_obs, done)
if len(agent.replay_buffer) > batch_size:
    loss = agent.train_step()
```

### Módulo `training/`

**Propósito**: Scripts para entrenar y evaluar agentes.

**Archivos principales**:
- `train_dqn.py`: Loop principal de entrenamiento
- `evaluate.py`: Evaluación de agentes entrenados

**Patrones**:
- Usar configuración desde archivos JSON/YAML
- Loggear métricas a TensorBoard
- Guardar checkpoints periódicamente
- Implementar early stopping si es necesario

### Módulo `viz/`

**Propósito**: Visualización de entrenamiento y análisis.

**Archivos principales**:
- `tb_logger.py`: Logging a TensorBoard
- `hooks.py`: Hooks de PyTorch para capturar activaciones
- `board_renderer.py`: Renderizado de tablero

**Patrones**:
- No ralentizar entrenamiento (usar actualizaciones asíncronas)
- Loggear histograms de pesos y gradientes
- Capturar activaciones con forward hooks

### Módulo `ui/`

**Propósito**: Interfaces de usuario para jugar y visualizar.

**Archivos principales**:
- `cli_rich.py`: CLI interactivo con Rich
- `pygame_board.py`: GUI con PyGame

## Ejemplos de Uso de la API

### Crear y Usar Entorno

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

### Entrenar Agente DQN

```python
from agent.dqn import DQNAgent
from env.checkers_env import CheckersEnv
import json

# Setup
with open("config/checkers_rules.json") as f:
    config = json.load(f)
env = CheckersEnv(config)
agent = DQNAgent(state_shape=(4, 8, 8))

# Loop de entrenamiento
obs = env.reset()
for step in range(num_steps):
    legal_actions = env.get_legal_actions()
    action = agent.select_action(obs, legal_actions, epsilon=0.1)
    next_obs, reward, done, info = env.step(action)
    
    agent.store_transition(obs, action, reward, next_obs, done)
    
    if len(agent.replay_buffer) > batch_size:
        loss = agent.train_step()
    
    if done:
        obs = env.reset()
    else:
        obs = next_obs
```

## Configuración

### Archivo de Configuración de Reglas

Ubicación: `config/checkers_rules.json`

```json
{
  "board_size": 8,
  "capture_forced": true,
  "prefer_longest_capture": true,
  "king_on_last_row": true,
  "max_episode_steps": 200,
  "draw_repetition_threshold": 3,
  "reward": {
    "win": 1.0,
    "loss": -1.0,
    "draw": 0.0,
    "capture": 0.01,
    "king_promotion": 0.02,
    "time_penalty": -0.001
  }
}
```

## Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests específicos del entorno
pytest env/tests/

# Con cobertura
pytest --cov=env --cov=agent
```

### Casos de Test

Los casos de test están en `env/tests/test_cases/` en formato JSON. Cada caso incluye:
- `board_state`: Estado del tablero
- `current_player`: Jugador actual
- `expected_legal_moves`: Movimientos legales esperados
- `expected_outcome`: Resultado esperado (win/loss/draw)

## Workflows

El proyecto sigue workflows estrictos. Ver `docs/guides/WORKFLOW_PROTOCOL.md` para detalles.

**Regla importante**: NO avanzar al siguiente workflow sin completar el anterior.

## Referencias Rápidas

- **Documentación de diseño**: `DESIGN.md`
- **Estándares**: `STANDARDS.md`
- **Reglas**: `RULES.md`
- **Investigación**: `docs/research/`
- **Guías**: `docs/guides/`

## Notas para Claude Code

- **Siempre validar acciones** antes de aplicarlas en el entorno
- **Usar acciones dinámicas**, no enumeradas globalmente
- **Implementar captura forzada** correctamente (filtrar movimientos simples si hay capturas)
- **Multi-jump recursivo**: Buscar todas las secuencias posibles
- **Determinismo**: Usar seed consistentemente
- **Documentar decisiones** no obvias en código
- **Tests primero**: Escribir tests antes de implementar features complejas

