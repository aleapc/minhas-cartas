#!/usr/bin/env python3
"""
Script para remover imagens genéricas/duplicadas e manter apenas as cartas reais.
Remove imagens menores que 50KB (ícones genéricos) e imagens duplicadas.
"""

import os
import hashlib
from pathlib import Path

# Diretório base
BASE_DIR = Path(__file__).parent.parent
CARTAS_DIR = BASE_DIR / "assets" / "cartas"

# Tamanho mínimo em bytes (50KB)
MIN_SIZE = 50 * 1024

def get_file_hash(filepath):
    """Calcula hash MD5 do arquivo."""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def limpar_volume(vol_dir, volume_num):
    """Remove imagens genéricas de um volume."""
    print(f"\n{'='*60}")
    print(f"Processando Volume {volume_num}: {vol_dir}")
    print(f"{'='*60}")

    if not vol_dir.exists():
        print(f"Diretório não encontrado: {vol_dir}")
        return

    imagens = list(vol_dir.glob("*.jpg"))
    print(f"Total de imagens: {len(imagens)}")

    removidas = 0
    hashes_vistos = {}

    for img_path in sorted(imagens):
        tamanho = img_path.stat().st_size

        # Remover se menor que o tamanho mínimo
        if tamanho < MIN_SIZE:
            print(f"  Removendo (pequena): {img_path.name} ({tamanho/1024:.1f}KB)")
            img_path.unlink()
            removidas += 1
            continue

        # Verificar duplicatas por hash
        img_hash = get_file_hash(img_path)
        if img_hash in hashes_vistos:
            print(f"  Removendo (duplicata): {img_path.name}")
            img_path.unlink()
            removidas += 1
            continue

        hashes_vistos[img_hash] = img_path.name

    restantes = len(list(vol_dir.glob("*.jpg")))
    print(f"\nResultado Volume {volume_num}:")
    print(f"  - Removidas: {removidas}")
    print(f"  - Restantes: {restantes}")

    return restantes

def main():
    print("="*60)
    print("LIMPEZA DE IMAGENS GENÉRICAS")
    print("="*60)
    print(f"Tamanho mínimo: {MIN_SIZE/1024:.0f}KB")

    total_vol1 = limpar_volume(CARTAS_DIR / "vol1", 1)
    total_vol2 = limpar_volume(CARTAS_DIR / "vol2", 2)

    print("\n" + "="*60)
    print("RESUMO FINAL")
    print("="*60)
    print(f"Volume 1: {total_vol1} cartas")
    print(f"Volume 2: {total_vol2} cartas")
    print(f"Total: {total_vol1 + total_vol2} cartas")

if __name__ == "__main__":
    main()
