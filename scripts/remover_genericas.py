#!/usr/bin/env python3
"""
Remove imagens genéricas (logos, códigos de barras, padrões decorativos)
e atualiza o índice de cartas.
"""

import os
import json

# Diretório base
BASE_DIR = r"C:\dev\Site SC"
CARTAS_DIR = os.path.join(BASE_DIR, "assets", "cartas")
DATA_FILE = os.path.join(BASE_DIR, "data", "cartas.json")
MANIFEST_FILE = os.path.join(CARTAS_DIR, "manifest.json")

# Lista de imagens genéricas identificadas manualmente
IMAGENS_GENERICAS = [
    # Volume 1 - última página (capa traseira)
    "vol1/vol1_p220_img6.jpg",   # Padrão xadrez
    "vol1/vol1_p220_img8.jpg",   # Código de barras ISBN

    # Volume 2 - últimas páginas (capa traseira)
    "vol2/vol2_p363_img1.jpg",   # Logo SC design
    "vol2/vol2_p363_img2.jpg",   # Logo UCL n lab
    "vol2/vol2_p364_img6.jpg",   # Código de barras ISBN
    "vol2/vol2_p364_img9.jpg",   # Padrão xadrez
    "vol2/vol2_p364_img12.jpg",  # Padrão xadrez
]

def remover_imagens():
    """Remove os arquivos de imagem genéricos."""
    removidas = []
    for img_rel in IMAGENS_GENERICAS:
        img_path = os.path.join(CARTAS_DIR, img_rel)
        if os.path.exists(img_path):
            os.remove(img_path)
            removidas.append(img_rel)
            print(f"  Removida: {img_rel}")
        else:
            print(f"  Não encontrada: {img_rel}")
    return removidas

def atualizar_cartas_json(removidas):
    """Remove as entradas do cartas.json."""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Criar set de IDs para remover
    ids_remover = set()
    for img_rel in removidas:
        # Extrair ID do caminho (ex: vol1/vol1_p220_img6.jpg -> vol1_p220_img6)
        filename = os.path.basename(img_rel)
        img_id = os.path.splitext(filename)[0]
        ids_remover.add(img_id)

    # Filtrar cartas
    cartas_antes = len(data['cartas'])
    data['cartas'] = [c for c in data['cartas'] if c['id'] not in ids_remover]
    cartas_depois = len(data['cartas'])

    # Salvar
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nCartas removidas do índice: {cartas_antes - cartas_depois}")
    print(f"Total de cartas agora: {cartas_depois}")

    return cartas_depois

def atualizar_manifest(removidas):
    """Atualiza o manifest.json."""
    with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    # Criar set de caminhos para remover
    paths_remover = set()
    for img_rel in removidas:
        full_path = f"assets/cartas/{img_rel}"
        paths_remover.add(full_path)

    # Filtrar imagens do manifest
    for vol_key in ['vol1', 'vol2']:
        if vol_key in manifest:
            manifest[vol_key] = [img for img in manifest[vol_key]
                                if img['path'] not in paths_remover]

    # Salvar
    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("Manifest atualizado")

def main():
    print("=" * 60)
    print("REMOÇÃO DE IMAGENS GENÉRICAS")
    print("=" * 60)

    print("\n1. Removendo arquivos de imagem...")
    removidas = remover_imagens()

    if removidas:
        print("\n2. Atualizando cartas.json...")
        total = atualizar_cartas_json(removidas)

        print("\n3. Atualizando manifest.json...")
        atualizar_manifest(removidas)

        print("\n" + "=" * 60)
        print(f"CONCLUÍDO: {len(removidas)} imagens genéricas removidas")
        print(f"Total de cartas válidas: {total}")
        print("=" * 60)
    else:
        print("\nNenhuma imagem genérica encontrada para remover.")

if __name__ == "__main__":
    main()
