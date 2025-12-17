# Índice de Archivos JSON - GamingRL

Este documento lista todos los archivos JSON del proyecto con sus ubicaciones y propósitos.

## Archivos de Configuración

### `config/checkers_rules.json`
**Ubicación**: `config/checkers_rules.json`  
**Tamaño**: 394 bytes  
**Propósito**: Configuración de reglas del juego de damas  
**Contenido**:
- `board_size`: Tamaño del tablero (8)
- `capture_forced`: Si la captura es forzada (true)
- `prefer_longest_capture`: Si se prefiere la captura más larga (true)
- `king_on_last_row`: Si se corona al llegar a la última fila (true)
- `max_episode_steps`: Máximo de pasos por episodio (200)
- `draw_repetition_threshold`: Umbral de repetición para empate (3)
- `draw_move_threshold`: Umbral de movimientos sin captura (100)
- `reward`: Configuración de recompensas

**Cómo acceder**:
```python
import json
with open("config/checkers_rules.json", "r") as f:
    config = json.load(f)
```

## Archivos de Casos de Test

**Ubicación**: `env/tests/test_cases/`  
**Total**: 21 archivos  
**Formato**: JSON con estructura estandarizada

### Estructura de un Caso de Test

```json
{
  "test_id": "test_XXX",
  "description": "Descripción del caso",
  "board_state": [[...], ...],  // 8x8 array
  "current_player": 1 o -1,
  "expected_legal_moves": [...],  // Lista de acciones esperadas
  "expected_outcome": "win" | "loss" | "draw" | null,
  "notes": "Notas adicionales"
}
```

### Lista Completa de Casos de Test

1. **test_001_simple_move.json** (990 bytes)
   - Movimiento simple de pieza normal hacia adelante

2. **test_002_forced_capture.json** (709 bytes)
   - Captura forzada - debe tomarse la captura disponible

3. **test_003_multi_jump.json** (711 bytes)
   - Secuencia de captura múltiple (2 saltos)

4. **test_004_prefer_longest_capture.json** (736 bytes)
   - Preferir captura más larga cuando hay múltiples opciones

5. **test_005_king_promotion_simple.json** (814 bytes)
   - Coronación por movimiento simple

6. **test_006_king_promotion_during_capture.json** (715 bytes)
   - Coronación durante secuencia de captura

7. **test_007_king_movement.json** (1066 bytes)
   - Movimiento de rey en cualquier dirección

8. **test_008_blocked_piece.json** (511 bytes)
   - Pieza bloqueada sin movimientos legales

9. **test_009_no_pieces.json** (550 bytes)
   - Victoria por eliminar todas las piezas del oponente

10. **test_010_complex_multi_jump.json** (691 bytes)
    - Secuencia de captura compleja (3+ saltos)

11. **test_011_king_capture.json** (792 bytes)
    - Rey realizando captura

12. **test_012_multiple_capture_options.json** (724 bytes)
    - Múltiples opciones de captura, elegir la más larga

13. **test_013_initial_board.json** (596 bytes)
    - Tablero inicial - todas las piezas en posición de inicio

14. **test_014_king_backward_capture.json** (675 bytes)
    - Rey capturando hacia atrás

15. **test_015_draw_repetition.json** (1351 bytes)
    - Empate por repetición de posición (3 veces)

16. **test_016_no_legal_moves_both.json** (521 bytes)
    - Empate cuando ambos jugadores no tienen movimientos legales

17. **test_017_king_multi_jump.json** (672 bytes)
    - Rey realizando secuencia de captura múltiple

18. **test_018_edge_board.json** (659 bytes)
    - Movimientos en los bordes del tablero

19. **test_019_blocked_by_own.json** (934 bytes)
    - Pieza bloqueada por piezas propias

20. **test_020_max_steps.json** (712 bytes)
    - Empate por alcanzar máximo de pasos

21. **test_021_complex_endgame.json** (567 bytes)
    - Posición compleja de final de partida

## Cómo Acceder a los Archivos JSON

### Desde Python

```python
from pathlib import Path
import json

# Configuración
config_path = Path("config/checkers_rules.json")
with open(config_path, "r") as f:
    config = json.load(f)

# Casos de test
test_dir = Path("env/tests/test_cases")
for test_file in test_dir.glob("*.json"):
    with open(test_file, "r") as f:
        test_case = json.load(f)
    print(f"Test: {test_case['test_id']}")
```

### Desde Terminal

```bash
# Listar todos los JSON
find . -name "*.json" -type f

# Ver contenido de un archivo
cat config/checkers_rules.json
cat env/tests/test_cases/test_001_simple_move.json

# Validar JSON
python -m json.tool config/checkers_rules.json
```

### Verificación de Integridad

Ejecutar script de verificación:
```bash
python scripts/verify_project.py
```

Este script:
- Verifica que todos los archivos existen
- Valida que son JSON válidos
- Muestra información de cada archivo
- Lista rutas completas

## Valores en Board State

Los archivos JSON usan la siguiente codificación para el tablero:
- `0`: Casilla vacía
- `1`: Jugador 1 (pieza normal)
- `2`: Jugador 1 (rey)
- `-1`: Jugador -1 (pieza normal)
- `-2`: Jugador -1 (rey)

## Valores en Acciones

Las acciones en `expected_legal_moves` tienen la estructura:
```json
{
  "from": [row, col],
  "to": [row, col],
  "captures": [[row1, col1], [row2, col2], ...],
  "promotion": true/false,
  "sequence_length": número_de_saltos
}
```

## Notas Importantes

1. **Solo casillas oscuras son válidas**: Las casillas donde `(row + col) % 2 == 1`
2. **Índices base 0**: Todas las coordenadas usan índices de 0 a 7
3. **Jugador 1**: Siempre juega primero (configurable)
4. **Formato consistente**: Todos los archivos siguen el mismo formato

## Troubleshooting

**Problema**: No puedo encontrar los archivos JSON
**Solución**: 
1. Verificar que estás en el directorio raíz del proyecto
2. Ejecutar `python scripts/verify_project.py`
3. Verificar rutas con `Path("env/tests/test_cases").exists()`

**Problema**: Error al cargar JSON
**Solución**:
1. Verificar que el archivo existe
2. Validar sintaxis JSON: `python -m json.tool archivo.json`
3. Verificar encoding (debe ser UTF-8)

**Problema**: Archivos no aparecen en IDE
**Solución**:
1. Refrescar el explorador de archivos
2. Verificar que no están en .gitignore
3. Verificar permisos de lectura

---

**Última verificación**: 2024-12-17  
**Estado**: ✅ Todos los archivos JSON válidos y accesibles

