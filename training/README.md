# Módulo training - Scripts de Entrenamiento

## Propósito

Este módulo contiene scripts para entrenar y evaluar agentes de RL.

## Estructura

```
training/
├── train_dqn.py    # Loop principal de entrenamiento
├── evaluate.py     # Evaluación de agentes
└── utils.py        # Utilidades de entrenamiento
```

## Uso Básico

### Entrenar Agente

```bash
python training/train_dqn.py \
    --config config/training/dqn_basic.json \
    --output_dir checkpoints/ \
    --num_steps 100000
```

### Evaluar Agente

```bash
python training/evaluate.py \
    --checkpoint checkpoints/model_100000.pt \
    --num_episodes 100 \
    --opponent random
```

## Scripts Principales

### train_dqn.py

Script principal de entrenamiento:
- Carga configuración
- Crea entorno y agente
- Loop de entrenamiento
- Guarda checkpoints
- Loggea métricas a TensorBoard

**Parámetros**:
- `--config`: Archivo de configuración
- `--output_dir`: Directorio para checkpoints
- `--num_steps`: Número de pasos de entrenamiento
- `--seed`: Seed para reproducibilidad

### evaluate.py

Script de evaluación:
- Carga modelo entrenado
- Evalúa contra diferentes oponentes
- Calcula métricas (win rate, etc.)
- Genera reporte

**Parámetros**:
- `--checkpoint`: Path al modelo
- `--num_episodes`: Número de episodios
- `--opponent`: Tipo de oponente (random, heuristic, self)

## Dependencias

- torch
- numpy
- tensorboard (para logging)

## Documentación Adicional

- Ver `docs/research/WORKFLOW_2_DQN_RESEARCH.md` para investigación
- Ver configuraciones de ejemplo en `config/training/`

