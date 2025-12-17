# 🚀 QUICK START / GUÍA RÁPIDA

Brief guide to get started with the GamingRL project.
*Guía breve para comenzar con el proyecto GamingRL.*

---

## 🇬🇧 English

### 1. Installation
Ensure you have Python 3.10+ installed.
```bash
pip install -r requirements.txt
```

### 2. Train the Agent
Train a Deep Q-Network (DQN) agent from scratch.
```bash
# Train for 10,000 steps and save to 'checkpoints/demo'
python training/train_dqn.py --num_steps 10000 --output_dir checkpoints/demo
```

### 3. Visualize Training
Monitor loss, reward, and agent internals using TensorBoard.
```bash
tensorboard --logdir logs/
```
*Open http://localhost:6006 in your browser.*

### 4. Run a Simulation
Run a quick simulation with random agents to verify the environment.
```bash
python examples/play_random.py
```

### 5. Run Tests
Verify system integrity.
```bash
pytest
```

---

## 🇪🇸 Español

### 1. Instalación
Asegúrate de tener Python 3.10+ instalado.
```bash
pip install -r requirements.txt
```

### 2. Entrenar al Agente
Entrena un agente Deep Q-Network (DQN) desde cero.
```bash
# Entrenar por 10,000 pasos y guardar en 'checkpoints/demo'
python training/train_dqn.py --num_steps 10000 --output_dir checkpoints/demo
```

### 3. Visualizar Entrenamiento
Monitorea la pérdida, recompensa y métricas internas usando TensorBoard.
```bash
tensorboard --logdir logs/
```
*Abre http://localhost:6006 en tu navegador.*

### 4. Ejecutar Simulación
Ejecuta una simulación rápida con agentes aleatorios para verificar el entorno.
```bash
python examples/play_random.py
```

### 5. Ejecutar Pruebas
Verifica la integridad del sistema.
```bash
pytest
```
