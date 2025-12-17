# Manual del Desarrollador - GamingRL

## Introducción

Este manual proporciona una guía completa para desarrolladores que trabajarán en el proyecto GamingRL. Cubre setup, estructura, workflows, y mejores prácticas.

## Visión General del Proyecto

GamingRL es un proyecto de investigación y desarrollo para construir un agente DQN (Deep Q-Network) que aprenda a jugar damas (checkers), con visualización profunda de pesos, gradientes y dinámica matemática.

**Objetivo Final**: Escalar progresivamente hacia sistemas más complejos tipo StarCraft Brood War.

## Setup Inicial

### Requisitos Previos

- Python 3.10 o superior
- Git
- Editor de código (VS Code, PyCharm, etc.)
- (Opcional) CUDA para aceleración GPU

### Instalación

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd GamingRL
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Verificar instalación**:
```bash
pytest tests/ -v
```

### Configuración del Entorno

1. **Configurar pre-commit hooks** (opcional pero recomendado):
```bash
pre-commit install
```

2. **Configurar variables de entorno** (si es necesario):
```bash
# Crear .env si es necesario
cp .env.example .env
# Editar .env con valores apropiados
```

## Estructura del Proyecto

### Directorios Principales

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
│   └── pygame_board.py       # GUI con PyGame
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

### Archivos Importantes

- `DESIGN.md`: Decisiones de diseño del proyecto
- `STANDARDS.md`: Estándares de código y desarrollo
- `RULES.md`: Reglas de desarrollo y workflow
- `.cursor/Claude.md`: Documentación para Claude Code
- `requirements.txt`: Dependencias del proyecto

## Workflows de Desarrollo

El proyecto sigue un enfoque estricto de workflows. Ver `docs/guides/WORKFLOW_PROTOCOL.md` para detalles completos.

### Workflows Principales

1. **WORKFLOW 0**: Definición y Diseño ✅ (Completado)
2. **WORKFLOW 1**: Entorno Gym-like (MVP) ✅ (Completado)
3. **WORKFLOW 2**: DQN Básico - En progreso
4. **WORKFLOW 3**: Visualización e Instrumentación
5. **WORKFLOW 4**: GUI Interactiva (opcional)
6. **WORKFLOW 5**: Experimentos y Evaluación
7. **WORKFLOW 6**: Hardening y Escalado

**Regla Crítica**: NO avanzar al siguiente workflow sin completar el anterior.

## Proceso de Desarrollo

### Cómo Empezar una Nueva Feature

1. **Revisar documentación relevante**:
   - Leer `DESIGN.md` para decisiones de diseño
   - Revisar archivos de investigación en `docs/research/`
   - Consultar `.cursor/Claude.md` para patrones

2. **Crear branch**:
```bash
git checkout -b feature/nombre-de-feature
```

3. **Escribir tests primero** (TDD):
   - Crear tests que fallen
   - Implementar feature
   - Verificar que tests pasan

4. **Implementar feature**:
   - Seguir estándares de código (ver `STANDARDS.md`)
   - Documentar código con docstrings
   - Mantener código limpio y modular

5. **Validar**:
   - Ejecutar tests: `pytest`
   - Verificar linter: `ruff check`
   - Formatear código: `black .`

6. **Commit**:
```bash
git add .
git commit -m "feat: descripción de la feature"
```

### Cómo Hacer Testing

**Ejecutar todos los tests**:
```bash
pytest
```

**Ejecutar tests específicos**:
```bash
pytest env/tests/test_legal_moves.py
```

**Con cobertura**:
```bash
pytest --cov=env --cov=agent --cov-report=html
```

**Tests de integración**:
```bash
pytest tests/integration/
```

### Cómo Hacer Commits

**Formato**: Conventional Commits

**Tipos**:
- `feat`: Nueva feature
- `fix`: Corrección de bug
- `docs`: Documentación
- `test`: Tests
- `refactor`: Refactorización
- `style`: Formato (sin cambios de lógica)
- `chore`: Tareas de mantenimiento

**Ejemplos**:
```bash
git commit -m "feat: add legal moves generation"
git commit -m "fix: correct capture forced rule"
git commit -m "docs: update DESIGN.md"
git commit -m "test: add test for multi-jump"
```

**Reglas**:
- Un cambio lógico por commit
- Mensajes claros y descriptivos
- Referenciar issues cuando aplique

### Cómo Hacer Code Review

1. **Crear Pull Request**:
   - Descripción clara del cambio
   - Listar cambios principales
   - Referenciar issues relacionados

2. **Revisión**:
   - Verificar que tests pasan
   - Revisar código por funcionalidad
   - Verificar que sigue estándares
   - Comprobar que documentación está actualizada

3. **Aprobar y Merge**:
   - Solo mergear después de aprobación
   - Squash commits si es necesario
   - Eliminar branch después de merge

## Uso de Claude Code

Ver `docs/guides/CLAUDE_CODE_GUIDE.md` para guía detallada.

**Puntos clave**:
- Mantener `.cursor/Claude.md` actualizado
- Usar prompts claros y específicos
- Hacer checkpoints frecuentes
- Iterar y colaborar, no esperar soluciones perfectas

## Debugging

### Debugging del Entorno

**Problema**: Movimientos legales incorrectos
- Verificar casos de test en `env/tests/test_cases/`
- Usar `env.render()` para visualizar estado
- Revisar logs de debug si están habilitados

**Problema**: Determinismo roto
- Verificar que se usa `seed()` correctamente
- Revisar operaciones no deterministas (sets, dicts sin ordenar)

### Debugging del Agente

**Problema**: Q-values divergentes
- Verificar learning rate
- Revisar gradient clipping
- Monitorear target network updates

**Problema**: Agente no aprende
- Verificar reward shaping
- Revisar exploración (epsilon schedule)
- Comprobar que replay buffer se llena

### Herramientas de Debugging

- **pdb**: Debugger de Python
- **TensorBoard**: Visualizar métricas de entrenamiento
- **Rich CLI**: Visualización interactiva del tablero
- **Logs**: Revisar logs de entrenamiento

## Troubleshooting

### Problemas Comunes

**Error**: `ModuleNotFoundError`
- **Solución**: Verificar que entorno virtual está activado y dependencias instaladas

**Error**: Tests fallan aleatoriamente
- **Solución**: Verificar determinismo, usar seeds consistentes

**Error**: Entrenamiento muy lento
- **Solución**: Verificar uso de GPU, optimizar generación de movimientos

**Error**: Q-values explosivos
- **Solución**: Reducir learning rate, agregar gradient clipping

### Obtener Ayuda

1. **Revisar documentación**:
   - `DESIGN.md`
   - `docs/research/`
   - `docs/guides/`

2. **Revisar código existente**:
   - Buscar ejemplos similares
   - Revisar tests para casos de uso

3. **Consultar con el equipo**:
   - Crear issue en GitHub
   - Preguntar en canales de comunicación del equipo

## Mejores Prácticas

### Código

- **Funciones pequeñas**: Una responsabilidad por función
- **Nombres descriptivos**: Código auto-explicativo
- **Type hints**: Obligatorios para funciones públicas
- **Docstrings**: Formato Google Style

### Testing

- **Tests antes de código**: TDD cuando sea posible
- **Cobertura alta**: 80% mínimo para código crítico
- **Tests determinísticos**: Usar seeds
- **Edge cases**: Cubrir casos límite

### Documentación

- **Mantener actualizada**: Sincronizar con código
- **Ejemplos claros**: Mostrar cómo usar APIs
- **Decisiones documentadas**: Explicar por qué, no solo qué

### Git

- **Commits frecuentes**: Después de cada feature funcional
- **Commits atómicos**: Un cambio lógico por commit
- **Mensajes claros**: Descriptivos y específicos

## Recursos Adicionales

- [DESIGN.md](../DESIGN.md): Decisiones de diseño
- [STANDARDS.md](../STANDARDS.md): Estándares del proyecto
- [RULES.md](../RULES.md): Reglas de desarrollo
- [WORKFLOW_PROTOCOL.md](WORKFLOW_PROTOCOL.md): Protocolo de workflows
- [CLAUDE_CODE_GUIDE.md](CLAUDE_CODE_GUIDE.md): Guía de Claude Code
- [API_REFERENCE.md](../api/API_REFERENCE.md): Referencia de API

## Contacto y Soporte

Para preguntas o problemas:
1. Revisar documentación primero
2. Buscar en issues existentes
3. Crear nuevo issue si es necesario
4. Contactar al equipo de desarrollo

