# Roadmap detallado: de DQN en Damas a IA tipo StarCraft Brood War

> **Objetivo**: proporcionar un plan técnico y de investigación, paso a paso, para construir desde cero
> un **DQN sencillo** con visualización profunda (pesos, gradientes, dinámica matemática), escalarlo
> progresivamente y entender **qué se necesita realmente** para llegar a sistemas tipo StarCraft Brood War.
>
> Este roadmap está pensado para trabajar con **Cursor o Google Antigravity**, en iteraciones claras,
> con checkpoints de conocimiento y código impecable.

---

## NIVEL 0 — Fundamentos conceptuales (imprescindible)

### Objetivo
Construir una **comprensión mental sólida** de qué está optimizando el agente y por qué aprende.

### Investigación
- Qué es **Q-learning** y qué aproxima un DQN:
  - Bellman equation:  
    \( Q(s,a) = r + \gamma \max_{a'} Q(s', a') \)
- Diferencia entre:
  - Monte Carlo vs TD-learning
  - On-policy vs Off-policy
- Por qué DQN necesita:
  - Replay Buffer
  - Target Network

### Entregables
- Documento `theory_notes.md`
- Diagrama a mano o digital del flujo: estado → red → acción → entorno → reward

### Validación de comprensión
- Explicar **sin código** por qué entrenar directamente con Q-learning sin replay diverge
- Poder escribir la loss de DQN desde memoria

---

## NIVEL 1 — Juego de Damas: entorno determinista

### Objetivo
Crear un **entorno totalmente controlado**, observable y depurable.

### Investigación
- Reglas formales de damas (elige un subconjunto si quieres):
  - Movimiento
  - Capturas
  - Coronas
  - Finalización
- Cómo modelar juegos de tablero como MDPs

### Decisiones de diseño
- Representación del estado:
  - Tensor `C x 8 x 8` (canales)
  - O vector discreto (32 posiciones)
- Espacio de acciones:
  - Enumerado global
  - O dinámico (lista de acciones legales)

### Entregables
- `checkers_env.py`
- `rules.py`
- Tests de:
  - Legal moves
  - Terminal states
  - Determinismo

### Instrumentación
- Render ASCII
- Render con `rich`

---

## NIVEL 2 — DQN mínimo (aprendizaje real)

### Objetivo
Que el agente **aprenda algo verificable** (ganar a random).

### Investigación
- Arquitectura básica DQN
- Replay Buffer y muestreo uniforme
- Epsilon-greedy exploration

### Diseño técnico
- Red pequeña (MLP o CNN)
- Loss: MSE TD-error
- Optimizador: Adam

### Entregables
- `network.py`
- `replay_buffer.py`
- `dqn_agent.py`
- `train_dqn.py`

### Validación
- Curva de reward creciente
- Q-values no explosivos

---

## NIVEL 3 — Visualización profunda (clave del proyecto)

### Objetivo
**Ver** qué está ocurriendo matemáticamente dentro del agente.

### Investigación
- Qué son:
  - Activaciones
  - Gradientes
  - Saturación
  - Exploding / vanishing gradients

### Instrumentación
- TensorBoard:
  - Scalars: loss, reward, epsilon
  - Histograms: pesos, gradientes
- Hooks en PyTorch:
  - Forward hooks
  - Backward hooks

### Visualizaciones recomendadas
- Evolución de normas de gradiente
- Distribución de Q-values
- PCA / t-SNE de activaciones

### Entregables
- `viz/hooks.py`
- `viz/logger.py`
- Dashboards reproducibles

---

## NIVEL 4 — Juego contra humanos y análisis de política

### Objetivo
Interactuar y **analizar decisiones** del agente.

### Investigación
- Policy interpretability
- Action masking
- Degenerate policies

### Implementación
- GUI con PyGame o CLI avanzado
- Mostrar:
  - Q-values por acción
  - Acción elegida
  - Reward inmediato

### Entregables
- `ui/pygame_board.py`
- Replays serializados

---

## NIVEL 5 — Robustez y mejoras RL

### Objetivo
Evitar trampas típicas del DQN.

### Investigación
- Double DQN
- Dueling Networks
- Prioritized Experience Replay
- Reward shaping vs sparse rewards

### Implementación incremental
- Activar cada mejora **una a una**
- Comparar curvas

### Entregables
- `experiments/ablation_study.md`

---

## NIVEL 6 — Generalización y Self-Play

### Objetivo
Aprender **estrategias**, no memorizar.

### Investigación
- Self-play
- Fictitious play
- Overfitting en RL

### Implementación
- Pool de versiones del agente
- Sampling de oponentes

---

## NIVEL 7 — De tablero a entornos complejos

### Objetivo
Romper las suposiciones simples del tablero.

### Investigación
- Partial observability (POMDP)
- Observaciones ruidosas
- Estados continuos

### Ejercicios
- Ocultar parte del tablero
- Añadir ruido al reward

---

## NIVEL 8 — Transición conceptual hacia StarCraft

### Cambio de paradigma
| Damas | StarCraft |
|------|----------|
| Turn-based | Real-time |
| Fully observable | Partially observable |
| Discrete actions | Massive action space |
| Single agent | Multi-agent |

### Investigación clave
- Hierarchical RL
- Options framework
- Centralized training / decentralized execution

---

## NIVEL 9 — StarCraft Brood War (realismo)

### Qué se necesita realmente
- BWAPI / TorchCraft
- Simulación masiva
- Imitation Learning
- Heurísticas + RL híbrido

### Subproblemas (obligatorios)
- Micro (control de unidades)
- Macro (economía, build order)
- Scouting y memoria

### Arquitecturas reales
- CNN + LSTM
- Attention / Transformers
- Graph Neural Networks

---

## NIVEL 10 — Conclusión honesta

- Un DQN de damas bien instrumentado = **fundación excelente**
- StarCraft-level AI ≠ DQN grande
- El valor está en:
  - Debugging
  - Visualización
  - Comprensión matemática

> Si entiendes profundamente el NIVEL 3, estás mejor preparado que el 90% de implementaciones RL.

---

## Siguiente paso recomendado
1. Implementar **Nivel 1 + 2** completos
2. No avanzar sin **Nivel 3 sólido**
3. Usar este proyecto como laboratorio RL

---

*Documento diseñado para trabajo iterativo con Cursor / Antigravity.*

