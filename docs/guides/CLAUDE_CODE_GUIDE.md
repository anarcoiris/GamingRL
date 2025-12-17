# Guía de Uso de Claude Code - GamingRL

## Introducción

Esta guía proporciona mejores prácticas específicas para trabajar efectivamente con Claude Code en el proyecto GamingRL.

## Fundamentos

### ¿Qué es Claude Code?

Claude Code es una herramienta de IA que ayuda en el desarrollo de software. Para obtener los mejores resultados, es importante:

- Proporcionar contexto claro
- Usar documentación detallada
- Iterar y colaborar
- Hacer checkpoints frecuentes

## Mejores Prácticas para Este Proyecto

### 1. Usar Claude.md Efectivamente

**Ubicación**: `.cursor/Claude.md`

**Contenido clave**:
- Descripción del proyecto
- Estructura de directorios
- Patrones comunes de código
- Errores comunes a evitar
- Ejemplos de uso

**Cuándo actualizar**:
- Al agregar nuevos patrones
- Al encontrar errores comunes
- Al cambiar estructura del proyecto
- Al establecer nuevas convenciones

**Ejemplo de actualización**:
```markdown
## Nuevo Patrón: Manejo de Acciones Legales

Cuando implementar get_legal_actions():
1. Primero buscar capturas (si hay, solo retornar capturas)
2. Si prefer_longest_capture, filtrar por longitud máxima
3. Si no hay capturas, retornar movimientos simples
```

### 2. Patrones de Prompts que Funcionan Bien

#### Prompt para Nueva Feature

**Bueno**:
```
Implementa la función get_legal_moves() en env/rules.py que:
- Toma board (np.array 8x8) y current_player (int)
- Retorna lista de acciones legales
- Debe implementar captura forzada según config
- Ver casos de test en env/tests/test_cases/test_002_forced_capture.json
- Seguir patrones en .cursor/Claude.md
```

**Malo**:
```
Implementa get_legal_moves
```

#### Prompt para Debugging

**Bueno**:
```
El test test_002_forced_capture está fallando. 
El error dice: "AssertionError: Expected 1 legal move, got 3"
Revisa env/rules.py línea 45-60 donde se filtran capturas.
El caso de test espera que solo haya una acción legal (captura).
```

**Malo**:
```
Arregla el test que falla
```

#### Prompt para Refactorización

**Bueno**:
```
Refactoriza la función _generate_captures_recursive() en env/rules.py:
- Actualmente tiene 80 líneas, dividir en funciones más pequeñas
- Extraer lógica de validación de captura a función separada
- Mantener misma funcionalidad (tests deben seguir pasando)
- Agregar type hints a nuevas funciones
```

**Malo**:
```
Refactoriza esta función
```

### 3. Cómo Estructurar Requests para Mejores Resultados

#### Estructura Recomendada

1. **Contexto**:
   - ¿Qué estás tratando de hacer?
   - ¿En qué parte del proyecto?
   - ¿Qué archivos están involucrados?

2. **Especificaciones**:
   - ¿Qué debe hacer exactamente?
   - ¿Qué restricciones hay?
   - ¿Qué patrones seguir?

3. **Ejemplos**:
   - ¿Hay casos de test relevantes?
   - ¿Hay código similar que seguir?
   - ¿Hay documentación que consultar?

4. **Validación**:
   - ¿Cómo verificar que funciona?
   - ¿Qué tests deben pasar?
   - ¿Qué comportamiento esperado?

#### Ejemplo Completo

```
CONTEXTO:
Estoy trabajando en WORKFLOW 1, implementando get_legal_actions() 
en env/checkers_env.py.

ESPECIFICACIONES:
- Debe retornar lista de acciones en formato dict con keys: 
  from, to, captures, promotion, sequence_length
- Si hay capturas disponibles, solo retornar capturas
- Si prefer_longest_capture=True, solo retornar secuencias más largas
- Usar env/rules.py para lógica de reglas

EJEMPLOS:
- Ver casos de test en env/tests/test_cases/
- Seguir estructura de acción documentada en DESIGN.md sección 4.2
- Usar patrones de .cursor/Claude.md

VALIDACIÓN:
- Tests en env/tests/test_legal_moves.py deben pasar
- Específicamente test_002_forced_capture debe pasar
- Debe retornar acciones serializables (JSON)
```

### 4. Cuándo Usar Checkpoints

**Usar checkpoints cuando**:
- ✅ Feature funcional completada
- ✅ Tests importantes pasan
- ✅ Antes de cambios grandes o riesgosos
- ✅ Al completar sección significativa
- ✅ Después de debugging exitoso

**No usar checkpoints para**:
- ❌ Cada línea de código
- ❌ Cambios menores de formato
- ❌ Comentarios o documentación menor

**Ejemplo de checkpoint útil**:
```
He completado la implementación de get_legal_actions() básico.
- Funciona para movimientos simples
- Tests test_001_simple_move pasan
- Documentación actualizada
Checkpoint aquí antes de implementar capturas.
```

### 5. Cómo Iterar Efectivamente

#### Proceso Iterativo Recomendado

1. **Primera iteración**: Implementación básica
   - Hacer que funcione
   - Tests básicos pasan
   - Documentación inicial

2. **Segunda iteración**: Mejoras y refinamiento
   - Optimizar código
   - Agregar más tests
   - Mejorar documentación

3. **Tercera iteración**: Pulido final
   - Revisar edge cases
   - Optimizar performance si es necesario
   - Documentación completa

#### Ejemplo de Iteración

**Iteración 1**:
```
Implementa función básica get_legal_moves() que retorna 
movimientos simples. No preocuparse por capturas aún.
```

**Iteración 2**:
```
Ahora agrega soporte para capturas. Debe detectar si hay 
capturas disponibles y retornar solo capturas si las hay.
```

**Iteración 3**:
```
Agrega soporte para multi-jump y prefer_longest_capture.
Asegúrate de que todos los tests pasen.
```

### 6. Colaboración vs. One-Shot

#### Cuándo Colaborar (Iterativo)

- ✅ Features complejas
- ✅ Cambios que afectan múltiples archivos
- ✅ Refactorizaciones grandes
- ✅ Cuando no estás seguro del enfoque

#### Cuándo One-Shot Puede Funcionar

- ✅ Cambios simples y claros
- ✅ Correcciones de bugs obvios
- ✅ Agregar tests para código existente
- ✅ Actualizaciones de documentación

### 7. Uso de Screenshots y Visualizaciones

**Cuándo usar screenshots**:
- Mostrar estado del tablero
- Visualizar errores en TensorBoard
- Mostrar resultados de tests
- Ilustrar problemas de UI

**Cómo usar**:
```
Aquí está un screenshot del tablero después del movimiento.
El test espera que la pieza esté en (4,1) pero está en (3,2).
Revisa la lógica de aplicación de movimiento en _apply_action().
```

### 8. Manejo de Errores Comunes

#### Error: Claude no entiende el contexto

**Solución**:
- Proporcionar más contexto
- Referenciar archivos específicos
- Incluir ejemplos concretos
- Actualizar `.cursor/Claude.md`

#### Error: Claude sugiere código que no sigue patrones

**Solución**:
- Ser más específico sobre patrones
- Referenciar código existente similar
- Actualizar `.cursor/Claude.md` con patrones
- Revisar y corregir manualmente

#### Error: Claude hace cambios no deseados

**Solución**:
- Ser más específico sobre qué cambiar
- Usar checkpoints antes de cambios grandes
- Revisar cambios antes de aceptar
- Rollback si es necesario

## Ejemplos de Uso Común

### Ejemplo 1: Implementar Nueva Función

**Prompt**:
```
Implementa la función compute_reward() en env/checkers_env.py:
- Debe retornar reward según esquema en DESIGN.md sección 5
- Valores: win=1.0, loss=-1.0, capture=0.01, promotion=0.02, time=-0.001
- Ver casos de test en env/tests/test_rewards.py
- Agregar type hints y docstring Google Style
```

### Ejemplo 2: Debugging

**Prompt**:
```
El test test_003_multi_jump está fallando con:
"AssertionError: Expected sequence_length=2, got 1"

Revisa env/rules.py función _generate_captures_recursive().
El caso de test tiene pieza en (5,0) que debe capturar en (4,1) 
y luego en (3,2), pero solo está capturando una pieza.
```

### Ejemplo 3: Refactorización

**Prompt**:
```
Refactoriza checkers_env.py método step():
- Extraer lógica de validación a método _validate_action()
- Extraer cálculo de reward a método _compute_reward()
- Extraer verificación de terminal a método _check_terminal()
- Mantener misma funcionalidad (todos los tests deben pasar)
```

## Checklist para Requests a Claude

Antes de hacer un request, verifica:

- [ ] Contexto claro proporcionado
- [ ] Especificaciones detalladas
- [ ] Referencias a archivos/documentación relevantes
- [ ] Ejemplos o casos de test mencionados
- [ ] Criterios de validación especificados
- [ ] `.cursor/Claude.md` actualizado si es necesario

## Recursos

- `.cursor/Claude.md`: Documentación del proyecto para Claude
- `DESIGN.md`: Decisiones de diseño
- `STANDARDS.md`: Estándares de código
- `RULES.md`: Reglas de desarrollo
- `docs/research/`: Investigación temática

## Notas Finales

- **Iterar, no esperar perfección**: Claude Code funciona mejor con iteración
- **Checkpoints frecuentes**: Facilita rollback si algo sale mal
- **Documentar patrones**: Ayuda a Claude a entender el proyecto
- **Ser específico**: Más contexto = mejores resultados
- **Revisar siempre**: No aceptar código sin revisar

---

**Última actualización**: WORKFLOW 1 completado. Entorno funcional implementado.

