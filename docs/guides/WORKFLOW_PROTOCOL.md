# Protocolo de Workflows - GamingRL

## Introducción

Este documento define el protocolo estricto de workflows del proyecto GamingRL. **Es crítico seguir este protocolo** para asegurar desarrollo ordenado y de calidad.

## Regla Fundamental

**NO avanzar al siguiente workflow sin completar el anterior.**

Cada workflow tiene criterios de aceptación que DEBEN cumplirse antes de avanzar.

## Estructura de Workflows

### WORKFLOW 0: Definición y Diseño ✅

**Estado**: Completado

**Objetivo**: Documentar y decidir todas las decisiones de diseño antes de implementar.

**Entregables**:
- [x] `DESIGN.md` completado
- [x] `docs/research/WORKFLOW_0_DESIGN_RESEARCH.md` con investigación exhaustiva
- [x] `config/checkers_rules.json` con configuración de reglas
- [x] 20+ casos de test documentados
- [x] Estructura de workspace establecida
- [x] Documentación para desarrolladores creada

**Criterios de Aceptación**:
- [x] Todas las decisiones de diseño documentadas
- [x] Representación de estado y acciones definidas
- [x] Esquema de recompensas documentado
- [x] Casos de test preparados
- [x] Estructura del proyecto establecida

**Transición a WORKFLOW 1**: ✅ Aprobado

---

### WORKFLOW 1: Entorno Gym-like (MVP) ✅

**Estado**: Completado

**Objetivo**: Implementar entorno de damas compatible con Gym/Gymnasium.

**Entregables Requeridos**:
- [x] `env/checkers_env.py` con clase `CheckersEnv`
- [x] `env/rules.py` con lógica de reglas
- [x] `env/representation.py` con conversión de estados
- [x] Tests unitarios pasando (>20 casos)
- [x] `env/README.md` con documentación
- [x] `examples/play_random.py` con ejemplo funcional

**Criterios de Aceptación**:
- [x] `reset()` y `step()` funcionan sin errores
- [x] `get_legal_actions()` implementado y funcional
- [x] `render('ascii')` produce tablero legible
- [x] Determinismo: mismo seed produce misma secuencia (tests pasan)
- [x] Serialización/deserialización funciona (tests pasan)
- [x] Documentación completa

**Checklist de Validación**:
- [x] Todos los tests pasan: `pytest env/tests/`
- [x] Tests de recompensas pasan (3/3)
- [x] Tests de determinismo pasan (2/2)
- [x] Documentación actualizada
- [x] Ejemplo de uso funciona (100 partidas random ejecutadas)

**Transición a WORKFLOW 2**: ✅ Aprobado

---

### WORKFLOW 2: DQN Básico ✅

**Estado**: Completado

**Objetivo**: Implementar agente DQN funcional que aprenda a jugar.

**Entregables Requeridos**:
- [x] `agent/dqn.py` con clase `DQNAgent`
- [x] `agent/network.py` con arquitectura CNN (ActionValueNetwork)
- [x] `agent/replay_buffer.py` con buffer de experiencias
- [x] `training/train_dqn.py` con loop principal de entrenamiento
- [x] Tests unitarios pasando
- [x] Agente puede entrenar sin errores
- [x] `examples/train_minimal.py` con ejemplo funcional

**Criterios de Aceptación**:
- [x] Agente puede seleccionar acciones (epsilon-greedy)
- [x] Replay buffer funciona correctamente (tests pasan)
- [x] Entrenamiento funciona (loss calculado, epsilon decay)
- [x] Q-values no divergen (gradient clipping implementado)
- [x] Checkpoints se guardan y cargan correctamente (tests pasan)
- [x] Documentación completa

**Checklist de Validación**:
- [x] Tests pasan: `pytest agent/tests/` (4/4 tests pasan)
- [x] Entrenamiento básico funciona (ejemplo ejecutado exitosamente)
- [x] Métricas básicas funcionan (loss, epsilon, buffer size)
- [x] Agente puede entrenar sin errores
- [x] Documentación actualizada

**Transición a WORKFLOW 3**: ✅ Aprobado

---

### WORKFLOW 3: Visualización e Instrumentación

**Estado**: Pendiente

**Objetivo**: Implementar visualización profunda de entrenamiento.

**Entregables Requeridos**:
- [ ] `viz/tb_logger.py` con logging a TensorBoard
- [ ] `viz/hooks.py` con hooks de PyTorch
- [ ] `viz/board_renderer.py` con renderizado
- [ ] Visualizaciones funcionando

**Criterios de Aceptación**:
- [ ] TensorBoard muestra métricas correctamente
- [ ] Histogramas de pesos y gradientes funcionan
- [ ] Activaciones se capturan correctamente
- [ ] Renderizado de tablero funciona
- [ ] No ralentiza entrenamiento significativamente

---

### WORKFLOW 4: GUI Interactiva (Opcional)

**Estado**: Opcional

**Objetivo**: Crear interfaz gráfica para jugar contra el agente.

**Entregables Requeridos**:
- [ ] `ui/pygame_board.py` con GUI
- [ ] Interacción humano vs. agente funciona
- [ ] Replays se pueden visualizar

---

### WORKFLOW 5: Experimentos y Evaluación

**Estado**: Pendiente

**Objetivo**: Sistema completo de experimentos y evaluación.

**Entregables Requeridos**:
- [ ] Scripts de evaluación
- [ ] Configuración de experimentos
- [ ] Análisis de resultados

---

### WORKFLOW 6: Hardening y Escalado

**Estado**: Pendiente

**Objetivo**: Preparar proyecto para producción y escalado.

**Entregables Requeridos**:
- [ ] CI/CD configurado
- [ ] Packaging completo
- [ ] Documentación final
- [ ] Optimizaciones de performance

---

## Checklist por Workflow

### Antes de Empezar un Workflow

- [ ] Workflow anterior completado y validado
- [ ] Criterios de aceptación del workflow anterior cumplidos
- [ ] Documentación del workflow anterior revisada
- [ ] Branch creado para el nuevo workflow

### Durante el Workflow

- [ ] Implementar features incrementales
- [ ] Tests escritos antes o junto con código
- [ ] Commits frecuentes y descriptivos
- [ ] Documentación actualizada continuamente
- [ ] Revisar progreso regularmente

### Antes de Completar un Workflow

- [ ] Todos los entregables completados
- [ ] Todos los criterios de aceptación cumplidos
- [ ] Todos los tests pasando
- [ ] Cobertura de tests adecuada
- [ ] Linter y formatter pasan
- [ ] Documentación completa y actualizada
- [ ] Code review realizado (si aplica)

### Transición Entre Workflows

1. **Validar completitud**:
   - Revisar checklist de criterios de aceptación
   - Ejecutar todos los tests
   - Verificar documentación

2. **Crear resumen**:
   - Documentar lo completado
   - Listar decisiones tomadas
   - Notar problemas encontrados

3. **Actualizar estado**:
   - Marcar workflow como completado
   - Actualizar documentación principal
   - Crear branch para siguiente workflow

4. **Aprobar transición**:
   - Revisión final
   - Aprobación explícita antes de avanzar

## Rollback Procedures

### Si un Workflow Falla

1. **Identificar el problema**:
   - Revisar tests que fallan
   - Analizar errores
   - Documentar el problema

2. **Decidir acción**:
   - **Opción A**: Corregir en el workflow actual
   - **Opción B**: Rollback a checkpoint anterior
   - **Opción C**: Reiniciar workflow desde cero

3. **Ejecutar rollback si es necesario**:
```bash
# Encontrar commit del checkpoint
git log --oneline

# Volver a checkpoint
git checkout <commit-hash>

# Crear nuevo branch desde checkpoint
git checkout -b workflow-X-restart
```

4. **Documentar lecciones aprendidas**:
   - Qué salió mal
   - Por qué
   - Cómo evitar en el futuro

### Checkpoints Recomendados

- Después de cada feature funcional
- Después de pasar tests importantes
- Antes de cambios grandes
- Al completar cada sección del workflow

## Validación de Workflows

### Validación Automática

```bash
# Ejecutar todos los tests
pytest

# Verificar cobertura
pytest --cov=. --cov-report=html

# Verificar linter
ruff check .

# Verificar formatter
black --check .
```

### Validación Manual

- [ ] Revisar código por calidad
- [ ] Verificar que documentación está actualizada
- [ ] Probar funcionalidad manualmente
- [ ] Revisar que sigue estándares

## Notas Importantes

1. **No saltar workflows**: Cada uno construye sobre el anterior
2. **Completar antes de avanzar**: Criterios de aceptación son obligatorios
3. **Documentar siempre**: Decisiones y cambios deben documentarse
4. **Tests primero**: Escribir tests antes o junto con código
5. **Checkpoints frecuentes**: Commits regulares para rollback fácil

## Preguntas Frecuentes

**P: ¿Puedo trabajar en múltiples workflows simultáneamente?**
R: No. Debes completar un workflow antes de avanzar al siguiente.

**P: ¿Qué pasa si encuentro un bug en un workflow anterior?**
R: Puedes corregirlo, pero asegúrate de que no rompe el workflow actual.

**P: ¿Puedo modificar decisiones de diseño durante implementación?**
R: Solo si es crítico. Debe documentarse en DESIGN.md y justificarse.

**P: ¿Cuándo puedo considerar un workflow "completo"?**
R: Cuando TODOS los criterios de aceptación están cumplidos y validados.

---

**Última actualización**: WORKFLOW 2 completado. Listo para WORKFLOW 3.

