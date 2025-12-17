# WORKFLOW 0: Investigación Temática - Definición y Diseño

## 1. Objetivo de Investigación

Antes de escribir código, necesitamos entender profundamente:
- Las reglas formales del juego de damas
- Cómo modelar el juego como MDP (Markov Decision Process)
- Representaciones eficientes de estado y acción
- Diseño de recompensas que guíen el aprendizaje

## 2. Investigación: Reglas Formales de Damas

### 2.1 Variantes de Damas

#### Damas Americanas (8×8) - ELEGIDA
- **Tablero**: 8×8 casillas, solo 32 casillas útiles (negras)
- **Piezas iniciales**: 12 piezas por jugador
- **Posición inicial**: Primeras 3 filas para cada jugador
- **Dirección**: Cada jugador mueve hacia el oponente
- **Coronación**: Al llegar a la última fila del oponente
- **Captura**: Obligatoria si está disponible
- **Multi-jump**: Obligatorio si hay secuencias disponibles

#### Damas Internacionales (10×10)
- Tablero más grande, 20 piezas por jugador
- Reglas similares pero más complejas
- **No elegida**: Demasiado compleja para MVP

#### Damas Inglesas
- Similar a americanas, reglas ligeramente diferentes en detalles
- **No elegida**: Menos estándar que americanas

### 2.2 Reglas Críticas a Implementar

#### 2.2.1 Movimiento Simple

**Piezas Normales (Men)**:
- Solo se mueven hacia adelante (hacia el oponente)
- Diagonalmente, una casilla a la vez
- Solo a casillas vacías
- No pueden retroceder

**Reyes (Kings)**:
- Se mueven en cualquier dirección diagonal
- Una casilla a la vez
- Solo a casillas vacías

**Ejemplo ASCII**:
```
  0 1 2 3 4 5 6 7
0 . b . b . b . b
1 b . b . b . b .
2 . . . . . . . .
3 . . . . . . . .
4 . . . . . . . .
5 r . r . r . r .
6 . r . r . r . r
7 r . r . r . r .

b = black (player -1), r = red (player +1)
```

#### 2.2.2 Capturas

**Regla Fundamental**: Si hay una captura disponible, DEBE ser tomada.

**Proceso de Captura**:
1. Pieza salta sobre pieza enemiga adyacente
2. Aterriza en casilla vacía inmediatamente después
3. Pieza enemiga es removida
4. Si desde la nueva posición hay más capturas, deben continuarse

**Ejemplo de Captura Simple**:
```
Antes:
  . . . .
  . r . .
  . . b .
  . . . .

Después (r captura b):
  . . . .
  . . . .
  . . . r
  . . . .
```

**Captura Múltiple (Multi-jump)**:
- Si después de una captura, la pieza puede capturar otra, DEBE hacerlo
- La secuencia completa es OBLIGATORIA
- Se debe tomar la secuencia más larga si hay múltiples opciones

**Ejemplo de Multi-jump**:
```
Antes:
  . . . . . .
  . r . r . .
  . . b . . .
  . . . r . .
  . . . . . .

Secuencia: r captura b, luego captura r (2 saltos)
```

#### 2.2.3 Preferencia de Captura Más Larga

**Regla**: Si hay múltiples secuencias de captura disponibles, se debe elegir la que capture más piezas.

**Ejemplo**:
- Opción A: Captura 2 piezas
- Opción B: Captura 3 piezas
- **Decisión**: Opción B (3 piezas)

**Empate**: Si múltiples secuencias capturan el mismo número de piezas, se elige la primera encontrada (determinístico).

#### 2.2.4 Coronación (Kinging)

**Condición**: Pieza normal llega a la última fila del oponente.

**Efecto**:
- Pieza se convierte en rey
- Puede moverse en cualquier dirección diagonal
- Si la coronación ocurre durante una secuencia de captura, la pieza puede continuar capturando como rey en la misma secuencia

**Ejemplo de Coronación Durante Captura**:
```
Pieza r en fila 6, captura pieza b y aterriza en fila 0 (última fila).
- Se corona inmediatamente
- Si desde fila 0 puede seguir capturando, DEBE hacerlo como rey
```

#### 2.2.5 Condiciones de Finalización

**Victoria**:
- Oponente sin piezas
- Oponente sin movimientos legales

**Empate**:
- Repetición de posición 3 veces (mismo tablero, mismo turno)
- Sin movimientos legales para ambos jugadores
- Sin capturas en N movimientos (opcional, configurable)
- Límite de pasos alcanzado (max_episode_steps)

### 2.3 Casos Edge Documentados

#### Caso 1: Multi-jump Complejo
```
Situación: Pieza puede capturar en 4 direcciones diferentes, cada una
lleva a más capturas. Debe encontrar la secuencia más larga.
```

#### Caso 2: Coronación a Mitad de Secuencia
```
Situación: Pieza normal captura, llega a última fila, se corona,
y puede seguir capturando como rey en la misma secuencia.
```

#### Caso 3: Empate por Repetición
```
Situación: Misma posición se repite 3 veces. Debe detectarse y
declarar empate.
```

#### Caso 4: Sin Movimientos Legales
```
Situación: Jugador tiene piezas pero todas están bloqueadas.
Debe declararse victoria del oponente.
```

### 2.4 Referencias a Implementaciones de Referencia

- [Python-Checkers](https://github.com/rhgrant10/checkers): Implementación de referencia en Python
- [World Checkers/Draughts Federation Rules](https://www.wcdf.net/rules/): Reglas oficiales
- [Checkers Rules - Wikipedia](https://en.wikipedia.org/wiki/Checkers): Documentación formal

## 3. Investigación: Modelado como MDP

### 3.1 Componentes del MDP

**Estado (S)**:
- Configuración del tablero (8×8)
- Turno actual (jugador 1 o -1)
- Historial de posiciones (para detectar repeticiones)

**Acciones (A)**:
- Movimientos legales desde el estado actual
- Variable en tamaño (depende de posición)
- Incluye movimientos simples y secuencias de captura

**Transición (P)**:
- Determinística: dado estado y acción, siguiente estado único
- Sin aleatoriedad en transiciones
- Reglas del juego definen transición exacta

**Recompensa (R)**:
- Definida en cada transición
- Recompensas intermedias (capturas, coronaciones)
- Recompensas finales (victoria, derrota, empate)

**Factor de Descuento (γ)**:
- 0.99 (valor estándar)
- Balance entre recompensas inmediatas y futuras

### 3.2 Propiedades del MDP de Damas

**Determinístico**: ✅
- No hay aleatoriedad en transiciones
- Mismo estado + misma acción = mismo siguiente estado

**Fully Observable**: ✅
- Tablero completo visible para ambos jugadores
- No hay información oculta

**Turn-based**: ✅
- Alternancia estricta de turnos
- Un jugador mueve, luego el otro

**Episódico**: ✅
- Cada partida termina (victoria, derrota, empate)
- Episodios independientes

**Discreto**: ✅
- Estados discretos (configuraciones de tablero)
- Acciones discretas (movimientos específicos)

### 3.3 Análisis del Espacio de Estados

**Tamaño Teórico**:
- 32 casillas útiles
- Cada casilla puede estar: vacía, pieza jugador 1 (men/king), pieza jugador 2 (men/king)
- Teóricamente: 5^32 ≈ 2.3 × 10^22 estados posibles

**Estados Alcanzables**:
- Mucho menor debido a reglas de movimiento
- Solo 24 piezas inicialmente
- Movimientos legales limitan estados alcanzables
- Estimación: ~10^20 estados alcanzables (aún enorme)

**Representación Práctica**:
- Tensor 4×8×8 = 256 valores float32
- Compacto y eficiente para redes neuronales
- Preserva estructura espacial

### 3.4 Justificación Matemática de Representación

**Tensor 4×8×8**:
- **Canal 0**: Own men (piezas propias normales)
- **Canal 1**: Own kings (reyes propios)
- **Canal 2**: Opponent men (piezas oponente normales)
- **Canal 3**: Opponent kings (reyes oponente)

**Ventajas**:
1. **Estructura Espacial**: CNNs pueden capturar patrones locales
2. **Separación de Información**: Diferentes tipos de piezas en canales separados
3. **Simetría**: Fácil de rotar/invertir para data augmentation
4. **Eficiencia**: Solo 256 valores vs. representaciones más complejas

**Alternativa Considerada: Vector 32**:
- Más compacto (32 valores)
- Pero pierde estructura espacial
- Requiere mapeo adicional para CNNs
- **Rechazada**: Menos natural para aprendizaje

## 4. Investigación: Representación de Estado

### 4.1 Comparación Detallada

#### Opción A: Tensor 4×8×8 (ELEGIDA)

**Estructura**:
```python
obs = np.zeros((4, 8, 8), dtype=np.float32)
# Canal 0: own men
# Canal 1: own kings
# Canal 2: opp men
# Canal 3: opp kings
```

**Ventajas**:
- Natural para CNNs (preserva estructura 2D)
- Fácil visualización y debugging
- Separación clara de información
- Compatible con arquitecturas estándar (ResNet, etc.)
- Permite data augmentation (rotaciones, simetrías)

**Desventajas**:
- Más memoria que vector compacto (256 vs 32 valores)
- Incluye casillas no utilizables (blancas)

**Información Capturada**:
- ✅ Posición de todas las piezas
- ✅ Tipo de cada pieza (men vs king)
- ✅ Propiedad de cada pieza (own vs opponent)
- ❌ Turno actual (debe agregarse como metadato)
- ❌ Historial de movimientos (no necesario para MDP)

#### Opción B: Vector 32 (Rechazada)

**Estructura**:
```python
obs = np.zeros(32, dtype=np.int8)
# Valores: 0=empty, 1=own_man, 2=own_king, -1=opp_man, -2=opp_king
```

**Ventajas**:
- Muy compacto (32 valores)
- Solo casillas útiles
- Rápido para operaciones

**Desventajas**:
- Pierde estructura espacial
- Requiere embedding adicional para CNNs
- Menos intuitivo para visualización
- Dificulta captura de patrones espaciales

### 4.2 Análisis de Información Perdida/Ganada

**Información Perdida en Tensor 4×8×8**:
- Casillas blancas (no utilizables) siempre en 0
- No afecta aprendizaje (red puede aprender a ignorarlas)

**Información Ganada**:
- Estructura espacial preservada
- Relaciones de vecindad claras
- Patrones locales detectables por CNNs

### 4.3 Experimentos Conceptuales de Generalización

**Hipótesis**: Tensor 4×8×8 permite mejor generalización porque:
1. CNNs aprenden patrones locales (agrupaciones, amenazas, defensas)
2. Estos patrones son invariantes a posición exacta
3. Red puede reconocer configuraciones similares en diferentes posiciones

**Vector 32**:
- Requiere aprender mapeo posición → significado
- Menos capacidad de generalizar patrones espaciales
- Más propenso a memorización

### 4.4 Decisión Final con Justificación Técnica

**Decisión**: Tensor 4×8×8

**Justificación**:
1. **Compatibilidad con CNNs**: Arquitectura natural para tableros
2. **Generalización**: Mejor capacidad de aprender patrones generalizables
3. **Visualización**: Fácil de visualizar y debuggear
4. **Estándar**: Formato común en RL para juegos de tablero
5. **Costo aceptable**: 256 valores es mínimo para redes modernas

### 4.5 Consideración de Metadatos Adicionales

**Turno Actual**:
- **Opción 1**: Canal adicional (5×8×8)
- **Opción 2**: Metadato separado en info dict
- **Decisión**: Metadato separado (más limpio, no aumenta tamaño de tensor)

**Historial Parcial**:
- No necesario para MDP (estado actual es suficiente)
- Repeticiones se detectan con hash de tablero
- **Decisión**: No incluir en observación

## 5. Investigación: Espacio de Acciones

### 5.1 Análisis de Complejidad del Espacio

**Movimientos Simples**:
- Por pieza: 1-4 movimientos posibles (depende de posición y tipo)
- Total inicial: ~12 piezas × 2-4 movimientos = 24-48 acciones

**Secuencias de Captura**:
- Variable: 1-10+ saltos en secuencia
- Complejidad: O(b^d) donde b=branching, d=profundidad
- Total teórico: Miles de secuencias posibles

**Espacio Total**:
- No fijo: depende de posición actual
- Rango típico: 5-50 acciones legales por estado
- Pico: 100+ en posiciones complejas con múltiples secuencias

### 5.2 Comparación: Acciones Enumeradas vs. Dinámicas

#### Enfoque A: Acciones Enumeradas Globalmente

**Concepto**:
- Pre-enumerar todas las acciones posibles en el tablero
- Tamaño fijo: ~200-500 acciones (estimación)
- Máscara booleana para acciones inválidas

**Ventajas**:
- Tamaño fijo: fácil para redes con salida fija
- Simple de implementar
- Compatible con DQN estándar

**Desventajas**:
- Muchas acciones nunca usadas (desperdicio)
- Espacio de acción muy grande
- Red debe aprender a ignorar acciones inválidas
- Menos eficiente

**Ejemplo**:
```python
# 200 acciones pre-enumeradas
action_space = Discrete(200)
# Máscara: [True, False, True, ...] para acciones legales
q_values = network(obs)  # Shape: (200,)
masked_q = q_values * legal_mask
action = argmax(masked_q)
```

#### Enfoque B: Acciones Dinámicas (ELEGIDO)

**Concepto**:
- Generar acciones legales en cada estado
- Red evalúa solo acciones relevantes
- Tamaño variable

**Ventajas**:
- Eficiente: solo evalúa acciones relevantes
- No desperdicia capacidad de red
- Más natural para el problema
- Mejor uso de recursos

**Desventajas**:
- Requiere arquitectura más compleja
- Tamaño variable puede complicar batching
- Necesita manejo especial de acciones

**Ejemplo**:
```python
legal_actions = env.get_legal_actions()  # Lista variable
q_values = network(obs, legal_actions)  # Solo evalúa legales
action_idx = argmax(q_values)
action = legal_actions[action_idx]
```

### 5.3 Diseño de Estructura de Acción Serializable

**Formato JSON**:
```json
{
  "from": [row, col],           // Posición origen
  "to": [row, col],             // Posición destino final
  "captures": [                  // Lista de posiciones capturadas
    [row1, col1],
    [row2, col2],
    ...
  ],
  "promotion": false,            // Si se corona en este movimiento
  "sequence_length": 1          // Número de saltos (1 = movimiento simple)
}
```

**Ejemplo Movimiento Simple**:
```json
{
  "from": [5, 0],
  "to": [4, 1],
  "captures": [],
  "promotion": false,
  "sequence_length": 1
}
```

**Ejemplo Secuencia de Captura**:
```json
{
  "from": [5, 0],
  "to": [2, 3],
  "captures": [[4, 1], [3, 2]],
  "promotion": true,
  "sequence_length": 2
}
```

### 5.4 Manejo de Secuencias de Captura Múltiple

**Estrategia**: Tratar secuencia completa como una acción

**Razón**:
- Secuencia es obligatoria (no se puede parar a mitad)
- Más eficiente que múltiples acciones
- Preserva semántica del juego

**Implementación**:
- Generar todas las secuencias posibles recursivamente
- Filtrar por longitud máxima si `prefer_longest_capture`
- Cada secuencia es una acción única

### 5.5 Estrategias de Masking y Mapeo

**Para Acciones Dinámicas**:
- No se necesita masking (solo se evalúan legales)
- Mapeo: índice en lista → acción serializable

**Para Acciones Enumeradas** (si se usa en futuro):
- Máscara booleana del mismo tamaño que espacio de acción
- Aplicar antes de argmax
- Setear Q-values de inválidas a -inf

## 6. Investigación: Diseño de Recompensas

### 6.1 Análisis de Trade-offs: Sparse vs. Dense Rewards

#### Sparse Rewards (Solo Final)

**Esquema**:
- +1.0 por victoria
- -1.0 por derrota
- 0.0 por empate
- 0.0 en todos los pasos intermedios

**Ventajas**:
- Simple y claro
- No introduce bias
- Agente aprende estrategia pura
- No riesgo de reward hacking

**Desventajas**:
- Aprendizaje muy lento
- Señal débil (solo al final)
- Dificulta exploración temprana
- Puede no converger en tiempo razonable

#### Dense Rewards (Shaping)

**Esquema**:
- Recompensas finales: ±1.0
- Recompensas intermedias: +0.01 (captura), +0.02 (coronación)
- Penalización temporal: -0.001 por paso

**Ventajas**:
- Aprendizaje más rápido
- Señales claras de progreso
- Facilita exploración
- Convergencia más rápida

**Desventajas**:
- Riesgo de reward hacking
- Agente puede optimizar recompensas intermedias en lugar de victoria
- Requiere tuning cuidadoso
- Puede llevar a políticas subóptimas

### 6.2 Diseño de Esquema Balanceado

**Esquema Propuesto**:
```python
rewards = {
    "win": 1.0,              # Final: victoria
    "loss": -1.0,            # Final: derrota
    "draw": 0.0,             # Final: empate
    "capture": 0.01,          # Intermedia: captura
    "king_promotion": 0.02,   # Intermedia: coronación
    "time_penalty": -0.001   # Penalización por paso
}
```

**Justificación**:
1. **Recompensas finales grandes**: Dominan sobre intermedias (ratio 100:1)
2. **Recompensas intermedias pequeñas**: Guían sin dominar
3. **Time penalty pequeña**: Desalienta partidas infinitas sin afectar estrategia

**Balance**:
- Shaping moderado: suficiente para acelerar aprendizaje
- No demasiado agresivo: evita reward hacking
- Recompensas finales dominan: asegura objetivo correcto

### 6.3 Análisis de Riesgo de Reward Hacking

**Riesgo 1: Optimización de Capturas**
- **Problema**: Agente puede priorizar capturas sobre victoria
- **Mitigación**: Recompensa de captura muy pequeña (0.01) vs. victoria (1.0)
- **Validación**: Monitorear si agente sacrifica piezas por capturas innecesarias

**Riesgo 2: Optimización de Coronaciones**
- **Problema**: Agente puede priorizar coronar sobre estrategia
- **Mitigación**: Recompensa pequeña (0.02), solo una vez por pieza
- **Validación**: Verificar que coronaciones ocurren en contexto estratégico

**Riesgo 3: Evitar Time Penalty**
- **Problema**: Agente puede apresurarse innecesariamente
- **Mitigación**: Penalización muy pequeña (-0.001)
- **Validación**: Monitorear longitud promedio de partidas

### 6.4 Estrategias de Validación de Shaping Efectivo

**Métricas de Validación**:
1. **Win Rate**: ¿Mejora con el tiempo?
2. **Calidad de Juego**: ¿Juega estratégicamente o solo optimiza recompensas?
3. **Análisis de Política**: ¿Decisiones tienen sentido estratégico?
4. **Comparación**: ¿Mejor que sparse rewards?

**Experimentos de Validación**:
- Entrenar con sparse rewards (baseline)
- Entrenar con shaping propuesto
- Comparar convergencia y calidad final
- Analizar políticas aprendidas

### 6.5 Referencias a Papers sobre Reward Shaping

- **Ng, Harada, Russell (1999)**: "Policy Invariance Under Reward Transformations"
- **Wiewiora et al. (2003)**: "Principled Methods for Advising Reinforcement Learning Agents"
- **Devlin & Kudenko (2012)**: "Dynamic Potential-Based Reward Shaping"

**Principios Clave**:
- Shaping debe preservar ordenamiento óptimo de políticas
- Recompensas intermedias deben ser pequeñas comparadas con finales
- Validar que shaping no cambia política óptima

## 7. Casos de Test Preparados

### 7.1 Formato de Casos de Test

**Estructura JSON**:
```json
{
  "test_id": "test_001",
  "description": "Movimiento simple de pieza normal",
  "board_state": [[...], ...],
  "current_player": 1,
  "expected_legal_moves": [
    {
      "from": [5, 0],
      "to": [4, 1],
      "captures": [],
      "promotion": false
    }
  ],
  "expected_outcome": null,
  "notes": "Caso básico de movimiento simple"
}
```

### 7.2 Categorías de Casos de Test

**Categoría 1: Movimientos Básicos** (5 casos)
- Movimiento simple hacia adelante
- Movimiento de rey en cualquier dirección
- Movimiento bloqueado
- Múltiples movimientos disponibles

**Categoría 2: Capturas** (5 casos)
- Captura simple
- Captura obligatoria (debe tomarse)
- Múltiples capturas disponibles
- Captura más larga preferida

**Categoría 3: Secuencias de Captura** (5 casos)
- Multi-jump simple (2 saltos)
- Multi-jump complejo (3+ saltos)
- Múltiples secuencias, elegir más larga
- Secuencia con coronación a mitad

**Categoría 4: Coronación** (3 casos)
- Coronación por movimiento simple
- Coronación durante captura
- Continuar capturando después de coronación

**Categoría 5: Estados Terminales** (3 casos)
- Victoria por eliminar oponente
- Victoria por bloquear oponente
- Empate por repetición

**Total**: 21 casos de test (más del mínimo de 20)

## 8. Próximos Pasos

1. **Validar reglas** con implementación de referencia
2. **Crear casos de test** en formato JSON
3. **Prototipar representación** de estado
4. **Diseñar experimentos** para validar decisiones
5. **Documentar decisiones finales** en DESIGN.md

## 9. Referencias y Recursos

### 9.1 Reglas de Juego
- [World Checkers/Draughts Federation](https://www.wcdf.net/rules/)
- [Wikipedia - Checkers](https://en.wikipedia.org/wiki/Checkers)
- [US Checkers Association Rules](https://www.usacheckers.com/rules.php)

### 9.2 Implementaciones de Referencia
- [Python-Checkers by rhgrant10](https://github.com/rhgrant10/checkers)
- [Checkers Engine in Python](https://github.com/rhgrant10/checkers)

### 9.3 Papers de RL
- Mnih et al. (2015): "Human-level control through deep reinforcement learning"
- Van Hasselt et al. (2016): "Deep Reinforcement Learning with Double Q-learning"
- Wang et al. (2016): "Dueling Network Architectures"

### 9.4 Reward Shaping
- Ng, Harada, Russell (1999): "Policy Invariance Under Reward Transformations"
- Devlin & Kudenko (2012): "Dynamic Potential-Based Reward Shaping"

## 10. Decisiones Finales Documentadas

### 10.1 Representación de Estado
- **Decisión**: Tensor 4×8×8 (float32)
- **Justificación**: Natural para CNNs, preserva estructura espacial
- **Metadatos**: Turno actual como info separado

### 10.2 Espacio de Acciones
- **Decisión**: Acciones dinámicas (lista variable)
- **Justificación**: Eficiente, solo evalúa acciones relevantes
- **Formato**: JSON serializable con from, to, captures, promotion

### 10.3 Recompensas
- **Decisión**: Shaping moderado con recompensas finales dominantes
- **Justificación**: Balance entre velocidad de aprendizaje y calidad
- **Valores**: win=1.0, loss=-1.0, capture=0.01, promotion=0.02, time=-0.001

### 10.4 Reglas Implementadas
- **Variante**: Damas Americanas (8×8)
- **Captura forzada**: Sí
- **Preferir captura más larga**: Sí
- **Coronación durante captura**: Sí, puede continuar como rey
- **Empate por repetición**: 3 veces

---

**Estado**: Investigación completa. Listo para implementación.
