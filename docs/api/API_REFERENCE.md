# Referencia de API - GamingRL

## Módulo env

### CheckersEnv

Clase principal del entorno de damas.

#### Métodos

##### `__init__(config: Dict) -> None`

Inicializa el entorno con configuración.

**Parámetros**:
- `config`: Diccionario con configuración de reglas (ver `config/checkers_rules.json`)

##### `reset(seed: Optional[int] = None) -> np.ndarray`

Resetea el entorno a estado inicial.

**Parámetros**:
- `seed`: Seed opcional para reproducibilidad

**Retorna**:
- `obs`: Observación inicial, shape `(4, 8, 8)`

##### `step(action: Dict) -> Tuple[np.ndarray, float, bool, Dict]`

Ejecuta una acción en el entorno.

**Parámetros**:
- `action`: Diccionario con keys: `from`, `to`, `captures`, `promotion`, `sequence_length`

**Retorna**:
- `obs`: Nueva observación
- `reward`: Recompensa del paso
- `done`: Si el episodio terminó
- `info`: Diccionario con información adicional

**Raises**:
- `ValueError`: Si la acción no es legal

##### `get_legal_actions() -> List[Dict]`

Retorna lista de acciones legales en el estado actual.

**Retorna**:
- Lista de diccionarios, cada uno representa una acción legal

##### `render(mode: str = 'ascii') -> Optional[np.ndarray]`

Renderiza el tablero.

**Parámetros**:
- `mode`: Modo de renderizado ('ascii', 'rgb_array')

**Retorna**:
- `None` para modo 'ascii', array numpy para 'rgb_array'

##### `seed(seed: Optional[int] = None) -> None`

Establece seed para reproducibilidad.

**Parámetros**:
- `seed`: Seed para random number generators

## Módulo agent

### DQNAgent

Agente DQN para aprendizaje por refuerzo.

#### Métodos

##### `__init__(state_shape: Tuple, learning_rate: float = 1e-4, gamma: float = 0.99, ...) -> None`

Inicializa el agente DQN.

**Parámetros**:
- `state_shape`: Forma del estado de entrada
- `learning_rate`: Learning rate del optimizer
- `gamma`: Factor de descuento
- `...`: Otros hiperparámetros

##### `select_action(state: np.ndarray, legal_actions: List[Dict], epsilon: float = 0.0) -> Dict`

Selecciona una acción usando epsilon-greedy.

**Parámetros**:
- `state`: Estado actual
- `legal_actions`: Lista de acciones legales
- `epsilon`: Probabilidad de exploración

**Retorna**:
- Acción seleccionada (diccionario)

##### `store_transition(state: np.ndarray, action: Dict, reward: float, next_state: np.ndarray, done: bool) -> None`

Almacena transición en replay buffer.

**Parámetros**:
- `state`: Estado actual
- `action`: Acción tomada
- `reward`: Recompensa recibida
- `next_state`: Estado siguiente
- `done`: Si el episodio terminó

##### `train_step() -> float`

Ejecuta un paso de entrenamiento.

**Retorna**:
- Loss del paso

##### `update_target_network() -> None`

Actualiza la red target con pesos de la red policy.

##### `save_checkpoint(path: str) -> None`

Guarda checkpoint del agente.

**Parámetros**:
- `path`: Path donde guardar

##### `load_checkpoint(path: str) -> None`

Carga checkpoint del agente.

**Parámetros**:
- `path`: Path del checkpoint

## Estructuras de Datos

### Acción

```python
{
    "from": [int, int],        # [row, col] posición origen
    "to": [int, int],          # [row, col] posición destino
    "captures": [[int, int]],  # Lista de [row, col] de piezas capturadas
    "promotion": bool,         # Si se corona en este movimiento
    "sequence_length": int     # Número de saltos (1 = movimiento simple)
}
```

### Observación

Tensor numpy de forma `(4, 8, 8)` con dtype `float32`:
- Canal 0: own men (1.0 si hay pieza propia normal)
- Canal 1: own kings (1.0 si hay rey propio)
- Canal 2: opp men (1.0 si hay pieza oponente normal)
- Canal 3: opp kings (1.0 si hay rey oponente)

### Info Dict

Diccionario retornado en `step()` con información adicional:
```python
{
    "captured": int,              # Número de piezas capturadas
    "current_player": int,        # Jugador actual (1 o -1)
    "legal_actions_count": int,   # Número de acciones legales
    "winner": Optional[int],      # Ganador si hay (1, -1, o None para empate)
}
```

## Ejemplos de Uso

Ver `README.md` de cada módulo para ejemplos detallados.

