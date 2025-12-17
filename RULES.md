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

## 11. Reglas de Desarrollo con IA

### 11.1 Checkpoint Frecuente
- **Commit después de cada feature funcional**: No esperar a completar todo
- **Commits atómicos**: Un cambio lógico por commit para rollback fácil
- **Mensajes descriptivos**: Facilitar identificación de checkpoints útiles
- **Willingness to restart**: Estar dispuesto a volver atrás si algo sale mal

### 11.2 Documentación Detallada
- **Mantener `.cursor/Claude.md` actualizado**: Documentación específica para Claude Code
- **Documentar patrones comunes**: Prevenir errores repetidos
- **Explicar decisiones no obvias**: Ayudar a Claude a entender el contexto
- **Incluir ejemplos de uso**: Facilitar comprensión de APIs

### 11.3 Componentes Especializados
- **Dividir tareas complejas**: Romper en componentes más pequeños y manejables
- **Un componente por responsabilidad**: Facilitar testing y debugging
- **Interfaces claras**: Definir contratos entre componentes
- **Modularidad**: Permitir desarrollo y testing independiente

### 11.4 Inputs Visuales
- **Usar screenshots/diagramas**: Cuando sea más claro que descripción textual
- **Diagramas ASCII o Mermaid**: Para visualizar flujos y arquitectura
- **Ejemplos visuales**: Mostrar estados del tablero, visualizaciones, etc.
- **Documentación visual**: Incluir imágenes cuando ayuden a entender

### 11.5 Patrones Personalizados
- **Documentar patrones en Claude.md**: Evitar errores repetidos
- **Establecer convenciones claras**: Nomenclatura, estructura, etc.
- **Crear templates**: Para código repetitivo
- **Documentar anti-patrones**: Qué evitar y por qué

### 11.6 Workflow Iterativo
- **Colaborar e iterar**: No esperar soluciones one-shot perfectas
- **Revisar y refinar**: Mejorar código basado en feedback
- **Probar incrementos pequeños**: Validar cada paso antes de continuar
- **Aceptar o reiniciar**: Evaluar resultados y decidir si continuar o empezar de nuevo

### 11.7 Planificación Extensa
- **Planear antes de implementar**: Usar Claude.ai para planificación detallada
- **Documentar decisiones**: En archivos de investigación
- **Validar diseño**: Asegurar que el diseño es correcto antes de codificar
- **Considerar alternativas**: Evaluar diferentes enfoques

### 11.8 Trabajo Incremental
- **Un paso a la vez**: No intentar hacer todo de una vez
- **Usar screenshots generosamente**: Para documentar progreso y estado
- **Validar cada paso**: Asegurar que cada incremento funciona
- **Checkpoints frecuentes**: Guardar progreso regularmente

### 11.9 Verificación Automática
- **Configurar loops auto-verificables**: Cuando sea posible
- **Tests automatizados**: Validar que el código funciona
- **Linters y formatters**: Mantener calidad de código automáticamente
- **CI/CD**: Automatizar validación y deployment

### 11.10 Prompts Claros y Detallados
- **Especificidad**: Proporcionar contexto suficiente para trabajo autónomo
- **Ejemplos concretos**: Mostrar qué se espera
- **Restricciones claras**: Definir límites y reglas
- **Objetivos explícitos**: Dejar claro qué se quiere lograr
```

