# DESIGN.md - Decisiones de Diseño del Proyecto GamingRL

## 1. Objetivo del Workflow

Documentar y decidir antes de programar:
- Reglas exactas del juego
- Formato de observaciones y acciones
- Esquema de recompensas
- Métricas a monitorizar
- Criterios de aceptación
- API y contract testing

## 2. Decisiones de Alto Nivel

### 2.1 Juego Base
- **Variante**: Damas clásicas (8×8, piezas en 32 casillas útiles)
- **Turnos**: Alternos, jugador 1 (agente) siempre inicia (configurable)
- **Captura forzada**: Sí (si hay captura disponible, se debe tomar)
- **Preferir captura más larga**: Sí (configurable)
- **Coronación (kinging)**: Al llegar a la última fila
- **Múltiples saltos**: Permitidos y obligatorios si disponibles
- **Empate**: 
  - Si no hay movimiento legal para ninguno en N pasos
  - Repetición de posición M veces
  - Valores ajustables por config

### 2.2 Observabilidad
- **Tipo**: Full-observable (tablero completo)
- **Formato**: Tensor 4×8×8 (canales: own men, own kings, opp men, opp kings)
- **Justificación**: Conveniente para CNNs y visualización

### 2.3 Entorno
- **Implementación**: Python, Gym-like (compatible con wrappers)
- **Framework**: PyTorch-friendly
- **Determinismo**: Total (seed controlado)

## 3. Representación del Estado (Observación)

### 3.1 Formato Elegido: Tensor 4×8×8

obs = np.float32 array shape (4, 8, 8):
  - canal 0 = own men (1.0 en casilla si own man)
  - canal 1 = own kings
  - canal 2 = opp men
  - canal 3 = opp kings
### 3.2 Metadatos Opcionales
- `current_player`: 1 o -1
- `legal_actions_mask`: vector booleano con dim = N_total_actions

## 4. Espacio de Acciones

### 4.1 Enfoque Elegido: Acciones Dinámicas
- El env expondrá `get_legal_actions()` que devuelve lista de acciones serializables
- El agente manejará masking / mapeo
- Ventaja: Implementación más limpia, evita enumeración fija

### 4.2 Estructura de una Acción (JSON)
{
  "from": [2, 5],      // fila, col
  "to": [3, 4],        // fila, col
  "captures": [[3,4]]  // lista de posiciones capturadas (multi-jump)
}
## 5. Recompensa (Reward Shaping)

### 5.1 Esquema Inicial
- `+1.0` por victoria (al final del episodio)
- `-1.0` por derrota
- `0.0` por empate
- `+0.01` por captura de pieza enemiga (shaping)
- `+0.02` por coronación (hacer un king)
- `-0.001` por cada paso (time penalty)

### 5.2 Justificación
- Shaping moderado para facilitar convergencia inicial
- Time penalty para desalentar partidas infinitas
- Recompensas intermedias vs sparse: balanceado

## 6. Métricas y Logs

### 6.1 Métricas Principales
- `episode_reward` (suma total)
- `win_rate` (por n episodes)
- `avg_reward_per_step`
- `avg_episode_length`
- `loss` (TD loss)
- `avg_q_value`, `max_q_value`
- `gradient_norm` (L2 norm per update)
- `weight_histograms` (por capa)
- `action_distribution` (qué acciones elige el agente)
- `legal_action_count` (por estado)

## 7. Configuración

### 7.1 Archivo: `config/checkers_rules.json`
{
  "board_size": 8,
  "use_32_indexing": false,
  "capture_forced": true,
  "prefer_longest_capture": true,
  "king_on_last_row": true,
  "max_episode_steps": 200,
  "draw_repetition_threshold": 3,
  "draw_move_threshold": 100
}
## 8. Casos Límite y Decisiones Controversiales

### 8.1 Coronar y Seguir Capturando
**Decisión**: Si una pieza corona a mitad de secuencia de capturas, puede seguir capturando como rey en la misma secuencia.

### 8.2 Prefer Longest Capture
**Decisión**: Si hay múltiples secuencias de captura, se debe elegir la que capture más piezas. En caso de empate, se elige la primera encontrada.

### 8.3 Repetición de Posición
**Decisión**: Se registra hash de tableros para detectar repeticiones. Si la misma posición se repite 3 veces, se declara empate.

### 8.4 Regla de 3 Turnos sin Captura
**Decisión**: No implementada inicialmente. Se usa `draw_move_threshold` para evitar loops infinitos.

## 9. Criterios de Aceptación (Workflow 0 → 1)

- [ ] DESIGN.md completado y revisado
- [ ] State y action representation decididos y documentados
- [ ] Config file de reglas con tests unitarios que validen reglas formales
- [ ] Test cases manuales que demuestren que `get_legal_actions()` devuelve la lista correcta en > 20 escenarios críticos
- [ ] Implementación inicial del entorno (Workflow 1) pasa todos tests de legalidad y determinismo

## 10. Checklist Mínimo (Workflow 0)

- [x] Elegir variante de damas (documentado)
- [x] Especificar observación y acción (ejemplo y justificación)
- [x] Definir reward shaping y parámetros iniciales
- [x] Definir métricas a monitorizar
- [ ] Crear archivo `config/checkers_rules.json`
- [ ] Preparar 10 tableros de test con soluciones esperadas (incluidos edge cases)
- [x] Redactar DESIGN.md (incluye todo lo anterior)
```

