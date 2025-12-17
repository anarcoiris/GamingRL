# Guía para Contribuidores - GamingRL

Gracias por tu interés en contribuir a GamingRL. Esta guía te ayudará a entender cómo contribuir efectivamente.

## Código de Conducta

Este proyecto sigue un código de conducta. Al participar, se espera que mantengas este código.

## Cómo Contribuir

### Reportar Bugs

1. Verifica que el bug no haya sido reportado ya
2. Crea un issue con:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs. actual
   - Información del entorno (OS, Python version, etc.)

### Sugerir Features

1. Verifica que la feature no haya sido sugerida ya
2. Crea un issue con:
   - Descripción clara de la feature
   - Justificación (por qué es útil)
   - Posible implementación (si tienes ideas)

### Contribuir Código

1. **Fork el repositorio**
2. **Crea un branch**:
   ```bash
   git checkout -b feature/nombre-de-feature
   ```
3. **Sigue los estándares**:
   - Lee `STANDARDS.md` y `RULES.md`
   - Sigue el protocolo de workflows
   - Escribe tests para nuevo código
   - Actualiza documentación
4. **Haz commits descriptivos**:
   - Usa formato Conventional Commits
   - Un cambio lógico por commit
5. **Ejecuta tests**:
   ```bash
   pytest
   ruff check .
   black --check .
   ```
6. **Crea Pull Request**:
   - Descripción clara del cambio
   - Referencia issues relacionados
   - Lista cambios principales

## Estándares de Código

Ver `STANDARDS.md` para detalles completos. Resumen:

- **Python 3.10+**
- **Type hints** para funciones públicas
- **Docstrings** formato Google Style
- **Black** para formateo (line length 100)
- **Ruff** para linting
- **Tests** con pytest

## Proceso de Desarrollo

1. **Sigue workflows estrictos**: Ver `docs/guides/WORKFLOW_PROTOCOL.md`
2. **No avanzar sin completar**: Cada workflow debe completarse antes del siguiente
3. **Tests primero**: Escribir tests antes o junto con código
4. **Documentar**: Mantener documentación actualizada

## Estructura de Commits

Usa formato Conventional Commits:

- `feat`: Nueva feature
- `fix`: Corrección de bug
- `docs`: Documentación
- `test`: Tests
- `refactor`: Refactorización
- `style`: Formato
- `chore`: Mantenimiento

Ejemplo:
```
feat: add legal moves generation
fix: correct capture forced rule
docs: update DESIGN.md
```

## Pull Requests

1. **Descripción clara**: Explica qué y por qué
2. **Tests pasando**: Todos los tests deben pasar
3. **Cobertura**: Mantener cobertura >80% para código crítico
4. **Documentación**: Actualizar docs si es necesario
5. **Revisión**: Esperar aprobación antes de merge

## Preguntas

Si tienes preguntas:
1. Revisa documentación primero
2. Busca en issues existentes
3. Crea nuevo issue si es necesario

## Agradecimientos

Gracias por contribuir a GamingRL.

