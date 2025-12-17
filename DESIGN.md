# DESIGN.md - Decisiones de Diseño del Proyecto GamingRL

## 1. Visión General y Arquitectura

Este documento centraliza las decisiones de diseño arquitectónico para todos los workflows del proyecto. Se mantiene actualizado para reflejar la implementación real.

### Arquitectura Modular
El sistema se divide en tres componentes desacoplados:
1.  **Environment (`env/`)**: Lógica pura, reglas y representación de estado.
2.  **Agent (`agent/`)**: Redes neuronales y algoritmos de aprendizaje.
3.  **Visualization (`viz/`)**: Instrumentación, logging y renderizado.

---

## 2. Entorno y Reglas (Workflow 1)

### 2.1 Juego Base
- **Variante**: Damas clásicas (8×8, US rules).
- **Captura forzada**: Sí (obligatorio tomar capturas si existen).
- **Preferir captura más larga**: Sí (regla de cantidad, no calidad).
- **Coronación**: Al detenerse en la última fila.
- **Empate**: Por límite de turnos o repetición de posiciones.

### 2.2 Observabilidad (State Representation)
- **Formato**: Tensor `(4, 8, 8)` tipo `float32`.
- **Canales**:
  0. `own_men`: Piezas normales propias (1.0).
  1. `own_kings`: Reyes propios (1.0).
  2. `opp_men`: Piezas normales oponentes (1.0).
  3. `opp_kings`: Reyes oponentes (1.0).
- **Justificación**: Representación espacial óptima para CNNs, separando semánticamente los tipos de piezas.

### 2.3 Espacio de Acciones
- **Tipo**: Dinámico (lista variable de acciones legales).
- **Formato de Acción (JSON)**:
  ```json
  {
    "from": [row, col],
    "to": [row, col],
    "captures": [[r,c], ...],
    "promotion": bool
  }
  ```
- **Encoding para Red**: Vector de 5 floats normalizados `[from_r, from_c, to_r, to_c, n_captures]`.

---

## 3. Agente y Red Neuronal (Workflow 2)

### 3.1 Arquitectura: Action-Value Network
A diferencia de DQN tradicional (que saca un Q para cada acción fija), usamos una arquitectura que evalúa pares `(estado, acción)`. Esto permite manejar un espacio de acciones variable y grande.

**A. State Encoder (CNN)**
Procesa el tablero para extraer features espaciales.
- `Conv2d(4 -> 32, 3x3)` + ReLU
- `Conv2d(32 -> 64, 3x3)` + ReLU
- `Flatten`
- `Linear` -> `Hidden Dim (256)` -> `Latent Dim (128)`

**B. Action Encoder (MLP)**
Procesa las características de la acción candidata.
- Input: 5 features espaciales normalizadas.
- `Linear(5 -> 32)` + ReLU

**C. Q-Head (Fusion)**
Combina estado y acción para estimar Q.
- Concatena `[State Features (128), Action Features (32)]`.
- `Linear(160 -> 256)` + ReLU.
- `Linear(256 -> 1)` (Q-value escalar).

### 3.2 Algoritmo DQN
- **Policy**: Epsilon-Greedy con decay lineal.
- **Buffer**: Replay Buffer circular (`deque`).
- **Storage**: Transiciones `(state, action_dict, reward, next_state, done)`.
- **Target Network**: Actualización periódica (copia "hard" de pesos).
- **Loss**: MSE entre `Q(s,a)` y `r + gamma * max_a' Q_target(s', a')`.

### 3.3 Aproximación de Target
Para calcular `max_a' Q(s', a')` en un espacio de acciones dinámico, idealmente se evaluarían todas las acciones legales reales de `s'`.
- **Simplificación Actual**: Se aproxima usando las features de la acción original si es necesario, o evaluación completa si el entorno lo permite en el loop de entrenamiento.
- **Decisión**: El training loop actual soporta evaluación real si se le pasa el env, o aproximación.

---

## 4. Visualización e Instrumentación (Workflow 3)

### 4.1 Estrategia de Logging
La observabilidad es "first-class citizen". No se entrena a ciegas.

- **TB Logger**: Wrapper sobre `SummaryWriter` de TensorBoard.
- **Métricas**:
  - `Escalars`: Loss, Reward, Epsilon, Win Rate.
  - `Histograms`: Distribución de pesos y gradientes (detectar saturación).
  - `Images`: Snapshots del tablero en momentos críticos.

### 4.2 Introspección (PyTorch Hooks)
Para entender la "caja negra" de la CNN.
- **Activation Hooks**: Capturan el output de capas `Conv2d` y `Linear`.
- **Uso**: Detección de "dead neurons" (activación cero constante) y visualización de feature maps.
- **Gradient Hooks**: Monitorean el flujo hacia atrás para detectar vanishing/exploding gradients.

### 4.3 Renderizado
- **BoardRenderer**: Clase agnóstica de backend.
- **Backends**: 
  - `ASCII`: Para logs de texto y debugging rápido.
  - `Rich`: Para terminales modernas, con colores y tablas.
- **Overlays**: Capacidad de superponer Q-values sobre las casillas para visualizar la "intuición" del agente.

---

## 5. Recompensa (Reward Shaping)

El esquema actual busca equilibrar la señal densa (capturas) con el objetivo final (ganar).

| Evento | Reward | Justificación |
|--------|--------|---------------|
| **Win** | `+1.0` | Objetivo principal. |
| **Loss**| `-1.0` | Castigo simétrico. |
| **Draw**| `0.0` | Neutral. |
| **Capture** | `+0.01` | Incentivo táctico pequeño (shaping). |
| **King** | `+0.02` | Incentivo estratégico. |
| **Step** | `-0.001` | Penalización por tiempo (evitar loops). |

---

## 6. Configuración

Todo el comportamiento se define en `config/checkers_rules.json`.
- `capture_forced`: `true` (Regla estándar).
- `max_episode_steps`: `200` (Evitar juegos infinitos).
- `draw_repetition_threshold`: `3` (Regla estándar).

---

## 7. Próximos Pasos de Diseño
- **Curriculum Learning**: Introducir oponentes progresivamente más difíciles.
- **Self-Play**: Entrenar agente contra versiones pasadas de sí mismo.
- **MCTS**: Explorar Monte Carlo Tree Search para mejorar la selección de acciones (Workflow futuro).
