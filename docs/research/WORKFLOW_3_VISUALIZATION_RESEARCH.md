# WORKFLOW 3: Investigación Temática - Visualización e Instrumentación

## 1. Objetivo de Investigación

Crear herramientas de visualización que permitan:
- Entender qué está aprendiendo el agente
- Debuggear problemas de entrenamiento
- Analizar la política aprendida
- Visualizar la dinámica interna de la red neuronal

## 2. Investigación: Métricas Clave a Visualizar

### 2.1 Métricas de Rendimiento
- **Episode Reward**: Recompensa acumulada por episodio
- **Win Rate**: Porcentaje de victorias
- **Average Episode Length**: Duración promedio
- **Reward per Step**: Recompensa promedio por paso

### 2.2 Métricas de Aprendizaje
- **TD Loss**: Error de la función Q
- **Q-values**: Promedio, máximo, distribución
- **Gradient Norm**: Norma L2 de gradientes
- **Learning Rate**: Valor actual (si usa schedule)

### 2.3 Métricas de Política
- **Action Distribution**: Qué acciones elige el agente
- **Exploration Rate (epsilon)**: Tasa de exploración
- **Legal Actions Count**: Número de acciones legales por estado

## 3. Investigación: Visualización de Pesos y Gradientes

### 3.1 Histogramas de Pesos
- **Propósito**: Detectar inicialización incorrecta, saturación
- **Cuándo**: Cada N updates (ej. cada 100)
- **Qué mostrar**: Distribución de valores por capa

### 3.2 Histogramas de Gradientes
- **Propósito**: Detectar vanishing/exploding gradients
- **Cuándo**: Cada update
- **Qué mostrar**: Norma y distribución de gradientes por capa

### 3.3 Visualización Espacial (CNNs)
- **Filtros de convolución**: Visualizar qué patrones detecta cada filtro
- **Feature maps**: Activaciones de capas intermedias
- **Grad-CAM**: Visualizar qué partes del tablero influyen más

## 4. Investigación: Visualización de Activaciones

### 4.1 Hooks en PyTorchython
def forward_hook(name):
    def hook(module, input, output):
        activations[name] = output.detach().cpu()
    return hook

model.conv1.register_forward_hook(forward_hook('conv1'))### 4.2 Análisis de Activaciones
- **Distribución**: Histogramas de valores
- **Dimensionality Reduction**: PCA, t-SNE de activaciones
- **Clustering**: Agrupar estados similares

### 4.3 Interpretación
- Estados similares deberían tener activaciones similares
- Cambios bruscos pueden indicar overfitting
- Patrones en activaciones revelan qué aprende la red

## 5. Investigación: Visualización del Tablero

### 5.1 Render Básico
- **ASCII**: Simple, rápido, portable
- **Rich**: Colores, tablas, mejor UX en terminal
- **PyGame**: Interactivo, para GUI

### 5.2 Overlays de Información
- **Q-values**: Mostrar Q-value de cada acción legal
- **Política**: Heatmap de probabilidades
- **Última acción**: Resaltar movimiento realizado
- **Amenazas**: Resaltar piezas en peligro

### 5.3 Visualización en Tiempo Real
- **Live updates**: Actualizar tablero durante entrenamiento
- **Replay**: Reproducir episodios guardados
- **Step-by-step**: Avanzar manualmente

## 6. Investigación: Herramientas de Logging

### 6.1 TensorBoard
- **Ventajas**: Integrado con PyTorch, potente
- **Uso**: Scalars, histograms, images
- **Limitaciones**: Solo local (a menos que uses TensorBoard.dev)

### 6.2 Weights & Biases (wandb)
- **Ventajas**: Dashboard en la nube, comparaciones, sweeps
- **Uso**: Similar a TensorBoard pero más features
- **Limitaciones**: Requiere cuenta (gratis para proyectos)

### 6.3 CSV/JSON Logging
- **Ventajas**: Simple, portable, fácil de analizar
- **Uso**: Para análisis custom con pandas/matplotlib
- **Limitaciones**: Menos interactivo

### 6.4 Decisión
- **TensorBoard**: Para desarrollo local
- **wandb**: Para experimentos y comparaciones (opcional)
- **CSV**: Para análisis detallado custom

## 7. Investigación: Visualización de Q-values

### 7.1 Distribución de Q-values
- **Histograma**: Distribución de todos los Q-values
- **Evolución temporal**: Cómo cambian Q-values con el tiempo
- **Por acción**: Q-values promedio por tipo de acción

### 7.2 Q-values en el Tablero
- **Heatmap**: Mostrar Q-value de mover cada pieza
- **Arrows**: Flechas indicando mejores movimientos
- **Color coding**: Verde (alto Q) a rojo (bajo Q)

## 8. Investigación: Análisis de Política

### 8.1 Action Distribution
- **Histograma**: Frecuencia de cada acción
- **Evolución**: Cómo cambia la política con el tiempo
- **Por estado**: Acciones elegidas en estados similares

### 8.2 Trajectory Analysis
- **Episodios completos**: Visualizar secuencia de decisiones
- **Decisiones críticas**: Identificar momentos clave
- **Errores**: Analizar decisiones subóptimas

## 9. Investigación: Debugging Tools

### 9.1 Checkpoints
- **Modelo**: Guardar pesos periódicamente
- **Estado completo**: Incluir optimizer, step count, etc.
- **Metadata**: Hiperparámetros, configuración

### 9.2 Replays
- **Formato**: JSON o pickle con estados y acciones
- **Reproducibilidad**: Poder reproducir episodios exactos
- **Análisis**: Analizar decisiones post-mortem

### 9.3 Logging Detallado
- **Niveles**: DEBUG, INFO, WARNING, ERROR
- **Contexto**: Incluir estado, acción, reward en logs
- **Filtrado**: Poder filtrar por tipo de evento

## 10. Referencias

- [TensorBoard Tutorial](https://www.tensorflow.org/tensorboard)
- [PyTorch Hooks](https://pytorch.org/tutorials/beginner/former_torchies/nn_tutorial.html#forward-and-backward-function-hooks)
- [Visualizing CNNs](https://distill.pub/2017/feature-visualization/)

## 11. Próximos Pasos

1. Implementar logger básico (TensorBoard)
2. Agregar hooks para activaciones
3. Implementar visualización de tablero con Rich
4. Crear dashboard de métricas en tiempo real
5. Implementar sistema de replays
```

