#!/usr/bin/env python3
"""
Script para extrair imagens das cartas dos PDFs do Silvano Corrêa.
Extrai imagens válidas (>200x200 pixels) e salva em assets/cartas/vol1 e vol2.
"""

import fitz  # PyMuPDF
import os
from pathlib import Path
from PIL import Image
import io

# Diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "cartas"

# PDFs a processar
PDFS = {
    1: BASE_DIR / "SILAVANO CORRÊA _LIVRO_01_ARQUIVO_FINAL.pdf",
    2: BASE_DIR / "SILVANO CORRÊA _ VOLUME 2_ ARQUIVO FINAL.pdf"
}

# Tamanho mínimo para considerar uma imagem válida
MIN_WIDTH = 200
MIN_HEIGHT = 200

def extrair_imagens_pdf(pdf_path: Path, volume: int, output_dir: Path):
    """
    Extrai imagens de um PDF e salva no diretório especificado.

    Args:
        pdf_path: Caminho do arquivo PDF
        volume: Número do volume (1 ou 2)
        output_dir: Diretório de saída para as imagens
    """
    print(f"\n{'='*60}")
    print(f"Processando Volume {volume}: {pdf_path.name}")
    print(f"{'='*60}")

    if not pdf_path.exists():
        print(f"ERRO: Arquivo não encontrado: {pdf_path}")
        return []

    # Criar diretório de saída
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    imagens_extraidas = []
    total_imagens = 0
    imagens_validas = 0

    print(f"Total de páginas: {len(doc)}")

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_display = page_num + 1  # Página começa em 1 para exibição

        # Extrair lista de imagens na página
        image_list = page.get_images(full=True)

        for img_index, img_info in enumerate(image_list, 1):
            total_imagens += 1
            xref = img_info[0]

            try:
                # Extrair dados da imagem
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # Carregar com PIL para verificar dimensões
                img = Image.open(io.BytesIO(image_bytes))
                width, height = img.size

                # Verificar tamanho mínimo
                if width < MIN_WIDTH or height < MIN_HEIGHT:
                    continue

                imagens_validas += 1

                # Nome do arquivo: vol1_p028_img1.jpg
                filename = f"vol{volume}_p{page_display:03d}_img{img_index}.jpg"
                filepath = output_dir / filename

                # Converter para RGB se necessário e salvar como JPEG
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                img.save(filepath, 'JPEG', quality=90)

                imagens_extraidas.append({
                    'id': f"vol{volume}_p{page_display:03d}_img{img_index}",
                    'volume': volume,
                    'pagina': page_display,
                    'imagem': str(filepath.relative_to(BASE_DIR)),
                    'largura': width,
                    'altura': height
                })

                if imagens_validas % 50 == 0:
                    print(f"  Processadas {imagens_validas} imagens válidas...")

            except Exception as e:
                print(f"  Erro ao extrair imagem {img_index} da página {page_display}: {e}")
                continue

    doc.close()

    print(f"\nResultado Volume {volume}:")
    print(f"  - Total de imagens encontradas: {total_imagens}")
    print(f"  - Imagens válidas (>{MIN_WIDTH}x{MIN_HEIGHT}): {imagens_validas}")
    print(f"  - Salvas em: {output_dir}")

    return imagens_extraidas


def main():
    """Função principal para extrair todas as imagens."""
    print("="*60)
    print("EXTRAÇÃO DE CARTAS - SILVANO CORRÊA")
    print("="*60)

    todas_imagens = []

    for volume, pdf_path in PDFS.items():
        output_dir = ASSETS_DIR / f"vol{volume}"
        imagens = extrair_imagens_pdf(pdf_path, volume, output_dir)
        todas_imagens.extend(imagens)

    print("\n" + "="*60)
    print("RESUMO FINAL")
    print("="*60)
    print(f"Total de imagens extraídas: {len(todas_imagens)}")
    print(f"  - Volume 1: {sum(1 for i in todas_imagens if i['volume'] == 1)}")
    print(f"  - Volume 2: {sum(1 for i in todas_imagens if i['volume'] == 2)}")

    # Salvar lista de imagens para uso posterior
    import json
    manifest_path = ASSETS_DIR / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(todas_imagens, f, ensure_ascii=False, indent=2)
    print(f"\nManifesto salvo em: {manifest_path}")

    return todas_imagens


if __name__ == "__main__":
    main()
