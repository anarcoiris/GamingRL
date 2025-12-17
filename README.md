# GamingRL - Proyecto Acelerado de Reinforcement Learning

![Status: W0-W3 Complete](https://img.shields.io/badge/Workflow-0--3_Complete-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

Plataforma integral de investigación para agentes de Reinforcement Learning en juegos de mesa, progresando desde Damas (Checkers) hacia entornos de alta complejidad. El proyecto prioriza la arquitectura modular, la reproducibilidad y la instrumentación profunda.

## 🏗 Arquitectura del Sistema

El sistema se compone de tres pilares desacoplados que permiten iteración rápida y aislamiento de responsabilidades.

```
GamingRL/
├── env/                 # Core Lógico
│   ├── checkers_env.py  # Gym compliant wrapper
│   └── rules.py         # Motor de reglas puro y determinista
├── agent/               # Cerebro
│   ├── dqn.py           # Implementación DQN optimizada
│   └── network.py       # Arquitecturas CNN espaciales
├── viz/                 # Ojos e Instrumentación
│   ├── tb_logger.py     # Integración profunda con TensorBoard
│   ├── hooks.py         # Análisis de activaciones/gradientes
│   └── board_renderer.py # Visualización Rich/ASCII
```

### Características Clave
*   **Entorno Vectorizado**: Representación de estado tensor `(4, 8, 8)` ideal para CNNs.
*   **Agente DQN Robusto**: Buffer de repetición circular, target networks, y clipping de gradientes.
*   **Observabilidad Total**: Pipeline de logging que permite inspeccionar la "caja negra" de la red neuronal capa por capa.

## 🚀 Quick Start

### 1. Instalación
```bash
pip install -r requirements.txt
```

### 2. Entrenar Agente (Training Loop)
Entrena un agente DQN desde cero. Los checkpoints se guardan automáticamente.
```bash
python training/train_dqn.py --num_steps 10000 --output_dir checkpoints/demo
```

### 3. Visualizar Progreso
Monitorea métricas de pérdida, recompensa y evolución de pesos en tiempo real.
```bash
tensorboard --logdir logs/
```

### 4. Simulación Rápida
Ejecuta partidas de prueba con agentes aleatorios para validar el entorno.
```bash
python examples/play_random.py
```

## 🗺 Estado del Proyecto

El desarrollo sigue una metodología estricta de Workflows secuenciales.

| Workflow | Estado | Entregables Clave |
|----------|--------|-------------------|
| **W0: Definición** | ✅ Completo | `DESIGN.md`, Specs, Config JSON |
| **W1: Entorno** | ✅ Completo | Gym Env, Motor de Reglas, 21+ Tests |
| **W2: DQN Básico** | ✅ Completo | Agente Funcional, Training Loop, Checkpoints |
| **W3: Visualización** | ✅ Completo | TensorBoard, Hooks de Activación, Rich Renderer |
| **W4: GUI** | 🚧 Pendiente | Interfaz Interactiva Web/PyGame |
| **W5: Experimentos** | 📅 Futuro | Benchmarking masivo |

## 📚 Documentación Técnica

Para profundizar en áreas específicas:

*   **[DESIGN.md](DESIGN.md)**: Racional detrás de las decisiones arquitectónicas (e.g., por qué CNN vs MLP).
*   **[env/README.md](env/README.md)**: Detalles sobre el tensor de estado y reglas de captura forzada.
*   **[agent/README.md](agent/README.md)**: Hiperparámetros del DQN y arquitectura de red.
*   **[viz/README.md](viz/README.md)**: Guía para usar hooks de introspección y logging avanzado.
*   **[STANDARDS.md](STANDARDS.md)**: Guía de estilo de código y convenciones de testing.

## 🤝 Contribución y Desarrollo

El proyecto impone estándares de calidad estrictos:
1.  **Tests Obligatorios**: Todo código nuevo debe incluir tests en `tests/`.
2.  **Linting**: El código debe cumplir con `black` y `ruff`.
3.  **Workflows Atómicos**: No avanzar de fase sin completar los criterios de aceptación previos.

Ver **[RULES.md](RULES.md)** para el protocolo completo de desarrollo.

---
*GamingRL Research Engine - 2025*
