# Módulo agent - Agentes de Reinforcement Learning

## Propósito

Este módulo implementa agentes de RL, comenzando con DQN (Deep Q-Network).

## Estructura

```
agent/
├── dqn.py              # Clase DQNAgent
├── network.py          # Arquitectura de red neuronal
├── replay_buffer.py    # Buffer de experiencias
└── base.py            # Clase base para agentes
```

## Uso Básico

```python
from agent.dqn import DQNAgent
from env.checkers_env import CheckersEnv
import json

# Setup
with open("config/checkers_rules.json") as f:
    config = json.load(f)
env = CheckersEnv(config)

# Crear agente
agent = DQNAgent(
    state_shape=(4, 8, 8),
    learning_rate=1e-4,
    gamma=0.99
)

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

## Componentes

### DQNAgent

Agente DQN principal con:
- Selección de acciones (epsilon-greedy)
- Almacenamiento de experiencias
- Entrenamiento con replay buffer
- Actualización de target network

### QNetwork

Arquitectura CNN para evaluar Q-values:
- Input: (4, 8, 8) tensor del tablero
- Output: Q-values para acciones legales

### ReplayBuffer

Buffer circular de experiencias:
- Almacena (state, action, reward, next_state, done)
- Muestreo uniforme para entrenamiento
- `save()` y `load()` para persistencia

### HeuristicAgent

Agente basado en Minimax con Alpha-Beta pruning:
- Determinista (o casi determinista)
- Evaluación basada en material y control central
- Configurable profundidad de búsqueda (depth)
- Uso ideal: Benchmarkbaseline, oponente para entrenamiento, generación de partidas 
- No requiere entrenamiento

## Dependencias

- torch (PyTorch)
- numpy

## Tests

Ejecutar tests:
```bash
pytest agent/tests/
```

## Documentación Adicional


- Ver `DESIGN.md` para decisiones de diseño

