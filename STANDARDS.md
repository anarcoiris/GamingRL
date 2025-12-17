# ESTÁNDARES DEL PROYECTO GamingRL

## 1. Estándares de Código

### 1.1 Lenguaje y Versión
- **Python**: 3.10 o superior
- **Type Hints**: Obligatorios para funciones públicas
- **Docstrings**: Formato Google Style

### 1.2 Formato de Código
- **Formatter**: `black` (line length: 100)
- **Linter**: `ruff` o `pylint`
- **Type Checking**: `mypy` (opcional pero recomendado)

### 1.3 Estructura de Archivos

```project/
├── env/           # Entornos (Gym-like)
├── agent/         # Agentes RL
├── training/      # Scripts de entrenamiento
├── viz/           # Visualización
├── ui/            # Interfaces de usuario
├── experiments/   # Configs y experimentos
├── config/        # Archivos de configuración
├── tests/         # Tests unitarios
└── docs/          # Documentación
```

### 1.4 Nomenclatura
- **Clases**: PascalCase (`CheckersEnv`, `DQNAgent`)
- **Funciones/Métodos**: snake_case (`get_legal_actions`, `compute_reward`)
- **Constantes**: UPPER_SNAKE_CASE (`MAX_EPISODE_STEPS`)
- **Variables**: snake_case (`current_player`, `board_state`)

## 2. Estándares de Testing

### 2.1 Framework
- **Framework**: `pytest`
- **Cobertura mínima**: 80% para código crítico (reglas, generación de movimientos)

### 2.2 Tipos de Tests
- **Unit Tests**: Funciones individuales
- **Integration Tests**: Componentes trabajando juntos
- **Property Tests**: Validar invariantes
- **Regression Tests**: Casos que fallaron antes

### 2.3 Estructura de Tests
```python
def test_feature_name_scenario():
    # Arrange
    ...
    # Act
    ...
    # Assert
    ...
```

## 3. Estándares de Documentación

### 3.1 Docstrings
```python
def function_name(param1: Type, param2: Type) -> ReturnType:
    """Breve descripción.
    
    Descripción detallada si es necesaria.
    
    Args:
        param1: Descripción del parámetro.
        param2: Descripción del parámetro.
    
    Returns:
        Descripción del valor de retorno.
    
    Raises:
        ValueError: Cuándo se lanza.
    """
```

### 3.2 README
- Cada módulo debe tener README.md explicando:
  - Propósito
  - Uso básico
  - Ejemplos
  - Dependencias

### 3.3 Documentación de Decisiones
- Decisiones importantes documentadas en DESIGN.md
- Cambios significativos en CHANGELOG.md

## 4. Estándares de Git

### 4.1 Commits
- **Formato**: Conventional Commits
- **Ejemplos**:
  - `feat: add legal moves generation`
  - `fix: correct capture forced rule`
  - `docs: update DESIGN.md`
  - `test: add test for multi-jump`

### 4.2 Branches
- `main`: Código estable
- `develop`: Desarrollo activo
- `feature/name`: Nuevas features
- `fix/name`: Correcciones

### 4.3 Pull Requests
- Descripción clara del cambio
- Tests pasando
- Documentación actualizada
- Revisión requerida

## 5. Estándares de Configuración

### 5.1 Archivos de Config
- **Formato**: JSON o YAML
- **Ubicación**: `config/`
- **Validación**: Schema validation (jsonschema)

### 5.2 Variables de Entorno
- Usar `.env` para secrets
- Documentar en README
- No commitear secrets

## 6. Estándares de Performance

### 6.1 Profiling
- Profile antes de optimizar
- Documentar decisiones de optimización
- Mantener código legible sobre micro-optimizaciones

### 6.2 Memoria
- Limpiar recursos (close(), del)
- Evitar memory leaks en loops largos
- Monitorear uso de memoria en entrenamiento

## 7. Estándares de Reproducibilidad

### 7.1 Seeds
- Todos los entornos deben soportar `seed()`
- Tests deben ser determinísticos
- Documentar seeds usados en experimentos

### 7.2 Dependencias
- `requirements.txt` con versiones fijas
- `environment.yml` para conda (opcional)
- Lock file para reproducibilidad exacta

## 8. Estándares de Logging

### 8.1 Niveles
- `DEBUG`: Información detallada para debugging
- `INFO`: Información general de progreso
- `WARNING`: Situaciones inesperadas pero manejables
- `ERROR`: Errores que impiden operación normal

### 8.2 Formato
- Estructurado (JSON) para parsing
- Incluir timestamp, nivel, módulo, mensaje
- No loggear información sensible

## 9. Estándares de Documentación para IA

### 9.1 Claude.md Files
- **Mantener `.cursor/Claude.md` actualizado**: Documentación específica para Claude Code
- **Incluir contexto del proyecto**: Descripción, estructura, objetivos
- **Documentar patrones comunes**: Código repetitivo, convenciones, anti-patrones
- **Ejemplos de uso**: Mostrar cómo usar APIs y componentes
- **Errores comunes**: Listar errores frecuentes y cómo evitarlos

### 9.2 Patrones Documentados
- **Documentar patrones en Claude.md**: Prevenir errores repetidos
- **Establecer convenciones claras**: Nomenclatura, estructura, flujos
- **Crear templates**: Para código repetitivo o estructuras comunes
- **Documentar anti-patrones**: Qué evitar y por qué

### 9.3 Checkpoints Regulares
- **Commits frecuentes**: Después de cada feature funcional
- **Mensajes descriptivos**: Facilitar identificación de checkpoints útiles
- **Commits atómicos**: Un cambio lógico por commit para rollback fácil
- **Willingness to restart**: Estar dispuesto a volver atrás si algo sale mal

### 9.4 Verificación Automática
- **Configurar loops auto-verificables**: Cuando sea posible
- **Tests automatizados**: Validar que el código funciona
- **Linters y formatters**: Mantener calidad de código automáticamente
- **CI/CD**: Automatizar validación y deployment

### 9.5 Prompts Claros y Detallados
- **Especificidad**: Proporcionar contexto suficiente para trabajo autónomo
- **Ejemplos concretos**: Mostrar qué se espera con ejemplos
- **Restricciones claras**: Definir límites y reglas explícitamente
- **Objetivos explícitos**: Dejar claro qué se quiere lograr

### 9.6 Documentación Visual
- **Usar diagramas**: Mermaid o ASCII para visualizar flujos y arquitectura
- **Screenshots cuando sea útil**: Mostrar estados, visualizaciones, etc.
- **Ejemplos visuales**: Incluir diagramas de estados del tablero, arquitectura, etc.
- **Documentación visual**: Incluir imágenes cuando ayuden a entender

## 10. Checklist Pre-Commit

Antes de hacer commit:
- [ ] Código formateado (`black`)
- [ ] Linter pasa (`ruff check`)
- [ ] Tests pasan (`pytest`)
- [ ] Type hints agregados
- [ ] Docstrings actualizados
- [ ] Sin prints de debug
- [ ] Commits atómicos y descriptivos
- [ ] `.cursor/Claude.md` actualizado si hay cambios relevantes
```

```markdown:RULES.md
# REGLAS DEL PROYECTO GamingRL

## 1. Reglas de Desarrollo

### 1.1 Workflow Estricto
- **NO** avanzar al siguiente workflow sin completar el anterior
- Cada workflow debe tener criterios de aceptación cumplidos
- Documentar decisiones en archivos de investigación correspondientes

### 1.2 Principio de Pequeños Pasos
- Implementar features incrementales
- Tests antes de implementación compleja (TDD cuando sea posible)
- Validar cada componente antes de integrar

### 1.3 No Optimización Prematura
- Primero hacer que funcione correctamente
- Luego medir performance
- Finalmente optimizar si es necesario

## 2. Reglas de Calidad

### 2.1 Código Limpio
- Funciones pequeñas y con responsabilidad única
- Evitar duplicación (DRY)
- Nombres descriptivos
- Comentarios solo cuando el código no es auto-explicativo

### 2.2 Manejo de Errores
- Validar inputs
- Mensajes de error claros y útiles
- No silenciar errores sin razón
- Logging apropiado de errores

### 2.3 Determinismo
- Todo debe ser reproducible con seed
- Evitar operaciones no deterministas
- Documentar cualquier fuente de aleatoriedad

## 3. Reglas de Testing

### 3.1 Tests Obligatorios
- Generación de movimientos legales: >20 casos de test
- Reglas del juego: Tests para cada regla
- Determinismo: Tests de reproducibilidad
- Estados terminales: Tests de victoria/empate/derrota

### 3.2 Edge Cases
- Casos límite deben estar cubiertos
- Errores esperados deben ser testeados
- Validar comportamiento en estados extremos

## 4. Reglas de Documentación

### 4.1 Documentación Actualizada
- Código y documentación deben estar sincronizados
- Actualizar docs cuando se cambia comportamiento
- Documentar decisiones no obvias

### 4.2 Investigación Documentada
- Cada workflow tiene archivo de investigación
- Preguntas abiertas deben estar documentadas
- Referencias y recursos deben estar listados

## 5. Reglas de Configuración

### 5.1 Configuración Externa
- No hardcodear valores configurables
- Usar archivos de config
- Validar configuración al inicio

### 5.2 Valores por Defecto
- Proporcionar valores por defecto sensatos
- Documentar todos los parámetros
- Hacer configurables aspectos críticos

## 6. Reglas de Integración

### 6.1 Compatibilidad
- Mantener compatibilidad con API de Gym/Gymnasium
- No romper interfaces públicas sin versión
- Documentar cambios breaking

### 6.2 Dependencias
- Minimizar dependencias externas
- Fijar versiones para reproducibilidad
- Documentar por qué se necesita cada dependencia

## 7. Reglas de Experimentación

### 7.1 Reproducibilidad
- Cada experimento debe ser reproducible
- Guardar configuración completa
- Loggear hiperparámetros y seeds

### 7.2 Versionado
- Versionar modelos entrenados
- Asociar modelos con configuraciones
- Documentar resultados de experimentos

## 8. Reglas de Visualización

### 8.1 Claridad
- Visualizaciones deben ser auto-explicativas
- Incluir leyendas y labels
- Usar colores consistentes

### 8.2 Performance
- Visualización no debe ralentizar entrenamiento
- Usar actualizaciones asíncronas cuando sea posible
- Permitir desactivar visualización para producción

## 9. Reglas de Seguridad

### 9.1 Validación de Inputs
- Validar todos los inputs del usuario
- Sanitizar datos antes de procesar
- Manejar casos maliciosos o edge cases

### 9.2 Secrets
- No commitear API keys, passwords, etc.
- Usar variables de entorno
- Documentar qué secrets se necesitan

## 10. Reglas de Comunicación

### 10.1 Commits Descriptivos
- Mensajes claros y descriptivos
- Un cambio lógico por commit
- Referenciar issues cuando aplique

### 10.2 Code Review
- Todo código debe ser revisado
- Revisar por funcionalidad y estilo
- Aprobar antes de merge
```

Finalmente, el análisis crítico y preguntas:

```markdown:docs/research/CRITICAL_ANALYSIS.md
# ANÁLISIS CRÍTICO Y PREGUNTAS DE INVESTIGACIÓN

## 1. Análisis Crítico del Diseño Propuesto

### 1.1 Fortalezas del Diseño Actual

#### Representación de Estado (Tensor 4×8×8)
**Fortaleza**: 
- Natural para CNNs, preserva estructura espacial
- Fácil de visualizar y debuggear
- Compatible con arquitecturas estándar

**Debilidad Potencial**:
- ¿Es suficiente para capturar toda la información relevante?
- ¿Necesitamos información adicional (ej. número de movimientos sin captura)?

**Pregunta**: ¿Deberíamos agregar canales adicionales para metadatos (turno, número de movimientos, etc.)?

#### Acciones Dinámicas
**Fortaleza**:
- Eficiente, solo evalúa acciones relevantes
- No desperdicia capacidad de red

**Debilidad Potencial**:
- Requiere arquitectura más compleja
- ¿Cómo manejar cuando el número de acciones legales varía mucho?

**Pregunta**: ¿Es mejor usar acciones enumeradas con masking o acciones dinámicas? ¿Cuál es más estable para DQN?

#### Reward Shaping
**Fortaleza**:
- Facilita aprendizaje inicial
- Señales claras de progreso

**Debilidad Potencial**:
- Riesgo de reward hacking
- ¿El agente aprenderá estrategia o solo optimizará recompensas intermedias?

**Pregunta**: ¿Cómo validar que el agente aprende estrategia real vs. optimización local de recompensas?

### 1.2 Decisiones Controversiales

#### Captura Forzada y Preferencia de Captura Más Larga
**Análisis**:
- Regla estándar en damas, pero añade complejidad
- Generación de movimientos más costosa
- ¿Vale la pena la complejidad adicional?

**Pregunta**: ¿Deberíamos empezar sin esta regla y agregarla después, o es esencial desde el inicio?

#### Coronación a Mitad de Secuencia
**Análisis**:
- Regla que varía entre variantes de damas
- Añade complejidad al algoritmo de generación de movimientos
- Impacto en estrategia del agente

**Pregunta**: ¿Qué variante implementar? ¿Cómo afecta esto al aprendizaje?

#### Empate por Repetición
**Análisis**:
- Necesario para evitar loops infinitos
- Requiere mantener historial de posiciones
- Threshold de 3 repeticiones: ¿es óptimo?

**Pregunta**: ¿Qué threshold es razonable? ¿Debería ser configurable?

### 1.3 Riesgos Identificados

#### Riesgo 1: Complejidad de Generación de Movimientos
**Problema**: Generar movimientos legales, especialmente secuencias de captura, es complejo y propenso a errores.

**Mitigación**:
- Tests exhaustivos (>20 casos)
- Implementación incremental
- Validación contra implementación de referencia

**Pregunta**: ¿Deberíamos usar una librería existente de damas para validar nuestra implementación?

#### Riesgo 2: Inestabilidad del DQN
**Problema**: DQN puede ser inestable, especialmente en espacios de acción grandes y variables.

**Mitigación**:
- Target network
- Gradient clipping
- Learning rate cuidadoso
- Monitoreo de Q-values

**Pregunta**: ¿Deberíamos implementar Double DQN desde el inicio o empezar con DQN básico?

#### Riesgo 3: Reward Shaping Inadecuado
**Problema**: Shaping mal diseñado puede llevar a políticas subóptimas.

**Mitigación**:
- Experimentar con diferentes esquemas
- Comparar con sparse rewards
- Análisis de política aprendida

**Pregunta**: ¿Cómo diseñar experimentos para validar que el shaping es efectivo?

## 2. Preguntas de Investigación Críticas

### 2.1 Sobre Representación

**P1**: ¿El tensor 4×8×8 captura toda la información necesaria para jugar óptimamente?
- **Subpreguntas**:
  - ¿Necesitamos información sobre historial?
  - ¿El turno actual es suficiente o necesitamos más contexto?
  - ¿Deberíamos incluir metadatos como número de movimientos sin captura?

**P2**: ¿Cómo afecta la representación a la capacidad de generalización?
- **Subpreguntas**:
  - ¿El agente aprenderá patrones generalizables?
  - ¿O memorizará posiciones específicas?

### 2.2 Sobre Espacio de Acciones

**P3**: ¿Acciones dinámicas vs. enumeradas: cuál es mejor para estabilidad y aprendizaje?
- **Subpreguntas**:
  - ¿Cómo afecta la variabilidad en número de acciones?
  - ¿Qué arquitectura de red es mejor para cada enfoque?

**P4**: ¿Cómo manejar secuencias de captura múltiple?
- **Subpreguntas**:
  - ¿Tratarlas como una acción compuesta?
  - ¿O como secuencia de acciones simples?
  - ¿Cómo afecta esto al aprendizaje?

### 2.3 Sobre Recompensas

**P5**: ¿Cuál es el balance óptimo entre sparse y dense rewards?
- **Subpreguntas**:
  - ¿Qué valores de recompensas intermedias son efectivos?
  - ¿Cómo evitar reward hacking?
  - ¿Cuándo el shaping interfiere con estrategia a largo plazo?

**P6**: ¿Cómo validar que las recompensas guían hacia estrategia óptima?
- **Subpreguntas**:
  - ¿Qué métricas indican aprendizaje correcto?
  - ¿Cómo detectar optimización local vs. estrategia global?

### 2.4 Sobre Arquitectura de Red

**P7**: ¿CNN vs. MLP: cuál es mejor para este problema?
- **Subpreguntas**:
  - ¿Las CNNs capturan patrones espaciales relevantes?
  - ¿O el problema es demasiado abstracto para CNNs?
  - ¿Qué tamaño de red es apropiado?

**P8**: ¿Cómo manejar eficientemente acciones legales variables?
- **Subpreguntas**:
  - ¿Arquitectura con atención sobre acciones?
  - ¿Embedding de acciones?
  - ¿O simplemente masking?

### 2.5 Sobre Entrenamiento

**P9**: ¿Qué hiperparámetros son críticos y cuáles pueden ser defaults?
- **Subpreguntas**:
  - ¿Learning rate: cómo encontrar el óptimo?
  - ¿Tamaño de buffer: impacto en aprendizaje?
  - ¿Schedule de epsilon: lineal vs. exponencial?

**P10**: ¿Cómo detectar y prevenir problemas comunes de DQN?
- **Subpreguntas**:
  - ¿Cómo identificar divergencia temprano?
  - ¿Qué señales indican que el agente está aprendiendo?
  - ¿Cuándo el agente está sobreajustando?

### 2.6 Sobre Evaluación

**P11**: ¿Cómo evaluar si el agente realmente aprendió a jugar bien?
- **Subpreguntas**:
  - ¿Win rate contra random es suficiente?
  - ¿Necesitamos oponentes heurísticos?
  - ¿Cómo medir "calidad" de juego más allá de win rate?

**P12**: ¿Qué métricas son más informativas para debugging?
- **Subpreguntas**:
  - ¿Q-values, loss, o win rate?
  - ¿Cómo interpretar cada métrica?
  - ¿Qué patrones indican problemas?

## 3. Experimentos Críticos a Realizar

### 3.1 Validación de Reglas
**Experimento**: Implementar generación de movimientos y validar contra casos conocidos.
- **Casos**: 20+ posiciones con soluciones conocidas
- **Métrica**: Precisión en generación de movimientos legales
- **Criterio**: 100% de precisión antes de continuar

### 3.2 Validación de Representación
**Experimento**: Comparar diferentes representaciones de estado.
- **Variantes**: Tensor 4×8×8, vector 32, con/sin metadatos
- **Métrica**: Performance de agente entrenado
- **Criterio**: Identificar representación más efectiva

### 3.3 Validación de Reward Shaping
**Experimento**: Comparar sparse vs. dense rewards.
- **Variantes**: Solo final, con shaping moderado, con shaping agresivo
- **Métrica**: Win rate, tiempo de convergencia, calidad de política
- **Criterio**: Encontrar balance óptimo

### 3.4 Validación de Arquitectura
**Experimento**: Comparar CNN vs. MLP.
- **Variantes**: Diferentes arquitecturas, mismos hiperparámetros
- **Métrica**: Performance final, tiempo de entrenamiento
- **Criterio**: Identificar arquitectura más efectiva

## 4. Decisiones Pendientes

### 4.1 Decisiones Técnicas
- [ ] ¿Usar Gym o Gymnasium?
- [ ] ¿PyTorch o TensorFlow? (PyTorch propuesto)
- [ ] ¿TensorBoard o wandb o ambos?
- [ ] ¿Formato de config: JSON o YAML?

### 4.2 Decisiones de Diseño
- [ ] ¿Implementar todas las reglas desde inicio o incrementalmente?
- [ ] ¿Qué variante exacta de damas implementar?
- [ ] ¿Cómo manejar la GUI: PyGame, web, o solo CLI?

### 4.3 Decisiones de Investigación
- [ ] ¿Qué papers son más relevantes para este proyecto?
- [ ] ¿Debemos comparar con baselines existentes?
- [ ] ¿Qué nivel de profundidad en visualización es necesario?

## 5. Próximos Pasos Inmediatos

1. **Responder preguntas críticas P1-P4** antes de implementar entorno
2. **Validar reglas** con implementación de referencia o casos de test
3. **Prototipar representación** de estado y validar que funciona
4. **Diseñar experimentos** para validar decisiones de diseño
5. **Crear casos de test** exhaustivos antes de implementar

## 6. Recursos para Responder Preguntas

### 6.1 Implementaciones de Referencia
- Buscar implementaciones open-source de damas
- Validar reglas contra estas implementaciones
- Usar como baseline para testing

### 6.2 Papers Relevantes
- DQN original (Mnih et al., 2015)
- Aplicaciones de RL a juegos de tablero
- Reward shaping en RL

### 6.3 Comunidad
- Foros de RL (Reddit r/reinforcementlearning)
- Stack Overflow para preguntas técnicas
- GitHub de proyectos similares
```

Creando el archivo de configuración inicial y estructura base:

```json:config/checkers_rules.json
{
  "board_size": 8,
  "use_32_indexing": false,
  "capture_forced": true,
  "prefer_longest_capture": true,
  "king_on_last_row": true,
  "max_episode_steps": 200,
  "draw_repetition_threshold": 3,
  "draw_move_threshold": 100,
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

```python:requirements.txt
# Core
numpy>=1.24.0
torch>=2.0.0
gymnasium>=0.29.0

# Visualization
matplotlib>=3.7.0
rich>=13.0.0
tensorboard>=2.13.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Development
black>=23.0.0
ruff>=0.0.280
mypy>=1.5.0

# Optional
wandb>=0.15.0
pygame>=2.5.0
```

```:.gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Jupyter
.ipynb_checkpoints/
*.ipynb

# PyTorch
*.pt
*.pth
*.ckpt

# Logs
logs/
*.log
tensorboard/
wandb/

# Data
data/
replays/
checkpoints/
experiments/results/

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db
```

```markdown:README.md
# GamingRL - Proyecto de Reinforcement Learning

Proyecto de investigación y desarrollo para construir un agente DQN que aprenda a jugar damas, con visualización profunda y escalado progresivo hacia sistemas más complejos.

## Estructura del Proyecto

```
GamingRL/
├── config/              # Archivos de configuración
├── env/                 # Entornos (Gym-like)
├── agent/               # Agentes RL
├── training/            # Scripts de entrenamiento
├── viz/                 # Visualización
├── ui/                  # Interfaces de usuario
├── experiments/         # Configs y experimentos
├── docs/                # Documentación
│   └── research/        # Investigación temática por workflow
└── tests/               # Tests unitarios
```

## Workflows

El proyecto sigue un enfoque estricto de workflows:

- **WORKFLOW 0**: Definición y Diseño (DESIGN.md)
- **WORKFLOW 1**: Entorno Gym-like (MVP)
- **WORKFLOW 2**: DQN Básico
- **WORKFLOW 3**: Visualización e Instrumentación
- **WORKFLOW 4**: GUI Interactiva (opcional)
- **WORKFLOW 5**: Experimentos y Evaluación
- **WORKFLOW 6**: Hardening y Escalado

## Documentación

- [DESIGN.md](DESIGN.md) - Decisiones de diseño
- [STANDARDS.md](STANDARDS.md) - Estándares del proyecto
- [RULES.md](RULES.md) - Reglas de desarrollo
- [docs/research/](docs/research/) - Investigación temática por workflow
- [docs/research/CRITICAL_ANALYSIS.md](docs/research/CRITICAL_ANALYSIS.md) - Análisis crítico y preguntas

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

(Próximamente - cuando se complete WORKFLOW 1)

## Desarrollo

Ver [STANDARDS.md](STANDARDS.md) y [RULES.md](RULES.md) para estándares y reglas de desarrollo.

## Roadmap

Ver [roadmap_dqn_checkers_to_star_craft.md](roadmap_dqn_checkers_to_star_craft.md) para el roadmap completo.
```

## Resumen de lo creado

1. DESIGN.md — Decisiones de diseño del Workflow 0
2. docs/research/WORKFLOW_0_DESIGN_RESEARCH.md — Investigación temática del Workflow 0
3. docs/research/WORKFLOW_1_ENVIRONMENT_RESEARCH.md — Investigación temática del Workflow 1
4. docs/research/WORKFLOW_2_DQN_RESEARCH.md — Investigación temática del Workflow 2
5. docs/research/WORKFLOW_3_VISUALIZATION_RESEARCH.md — Investigación temática del Workflow 3
6. docs/research/CRITICAL_ANALYSIS.md — Análisis crítico y preguntas de investigación
7. STANDARDS.md — Estándares del proyecto
8. RULES.md — Reglas de desarrollo
9. config/checkers_rules.json — Configuración inicial
10. requirements.txt — Dependencias
11. .gitignore — Archivos a ignorar
12. README.md — Documentación principal

Estos archivos establecen la base del proyecto. ¿Quieres que continúe con algún workflow específico o que profundice en alguna sección?
