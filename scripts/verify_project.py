"""Script to verify project integrity and list all JSON files."""

import json
import sys
from pathlib import Path
from typing import List, Dict


def verify_json_files() -> Dict:
    """Verify all JSON files in the project.
    
    Returns:
        Dictionary with verification results
    """
    results = {
        "config_files": [],
        "test_files": [],
        "errors": [],
        "total": 0,
        "valid": 0,
    }
    
    # Check config file
    config_path = Path("config/checkers_rules.json")
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            results["config_files"].append({
                "path": str(config_path),
                "size": config_path.stat().st_size,
                "valid": True,
                "keys": list(config.keys()),
            })
            results["total"] += 1
            results["valid"] += 1
        except Exception as e:
            results["errors"].append(f"Config file error: {e}")
            results["total"] += 1
    else:
        results["errors"].append("Config file not found")
    
    # Check test case files
    test_dir = Path("env/tests/test_cases")
    if test_dir.exists():
        test_files = sorted(test_dir.glob("*.json"))
        for test_file in test_files:
            try:
                with open(test_file, "r") as f:
                    test_data = json.load(f)
                results["test_files"].append({
                    "path": str(test_file),
                    "name": test_file.name,
                    "size": test_file.stat().st_size,
                    "valid": True,
                    "test_id": test_data.get("test_id", "unknown"),
                    "description": test_data.get("description", ""),
                })
                results["total"] += 1
                results["valid"] += 1
            except Exception as e:
                results["errors"].append(f"{test_file.name}: {e}")
                results["total"] += 1
    else:
        results["errors"].append(f"Test directory not found: {test_dir}")
    
    return results


def print_verification_report(results: Dict):
    """Print verification report.
    
    Args:
        results: Verification results dictionary
    """
    print("=" * 70)
    print("VERIFICACIÓN DE INTEGRIDAD DEL PROYECTO GamingRL")
    print("=" * 70)
    print()
    
    # Config files
    print("ARCHIVOS DE CONFIGURACION:")
    print("-" * 70)
    if results["config_files"]:
        for cfg in results["config_files"]:
            print(f"  [OK] {cfg['path']}")
            print(f"     Tamano: {cfg['size']} bytes")
            print(f"     Keys: {', '.join(cfg['keys'])}")
    else:
        print("  [ERROR] No se encontraron archivos de configuracion")
    print()
    
    # Test files
    print(f"ARCHIVOS DE TEST ({len(results['test_files'])} archivos):")
    print("-" * 70)
    if results["test_files"]:
        for test in results["test_files"]:
            status = "[OK]" if test["valid"] else "[ERROR]"
            print(f"  {status} {test['name']}")
            print(f"     Path: {test['path']}")
            print(f"     Tamano: {test['size']} bytes")
            print(f"     Test ID: {test['test_id']}")
            print(f"     Descripcion: {test['description'][:60]}...")
            print()
    else:
        print("  [ERROR] No se encontraron archivos de test")
    print()
    
    # Summary
    print("RESUMEN:")
    print("-" * 70)
    print(f"  Total archivos JSON: {results['total']}")
    print(f"  Archivos validos: {results['valid']}")
    print(f"  Archivos con errores: {len(results['errors'])}")
    
    if results["errors"]:
        print()
        print("ERRORES ENCONTRADOS:")
        for error in results["errors"]:
            print(f"  [ERROR] {error}")
    else:
        print()
        print("  [OK] TODOS LOS ARCHIVOS JSON SON VALIDOS")
    
    print()
    print("=" * 70)


def list_all_json_files():
    """List all JSON files with full paths."""
    print("\nLISTADO COMPLETO DE ARCHIVOS JSON:")
    print("=" * 70)
    
    # Config
    config_path = Path("config/checkers_rules.json")
    if config_path.exists():
        print(f"\nCONFIGURACIÓN:")
        print(f"  {config_path.absolute()}")
    
    # Test cases
    test_dir = Path("env/tests/test_cases")
    if test_dir.exists():
        test_files = sorted(test_dir.glob("*.json"))
        print(f"\nCASOS DE TEST ({len(test_files)} archivos):")
        for i, test_file in enumerate(test_files, 1):
            print(f"  {i:2d}. {test_file.absolute()}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    results = verify_json_files()
    print_verification_report(results)
    list_all_json_files()
    
    # Exit with error code if there are issues
    if results["errors"]:
        sys.exit(1)
    else:
        sys.exit(0)

