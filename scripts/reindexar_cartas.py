#!/usr/bin/env python3
"""
Script para reindexar as cartas após limpeza de imagens genéricas.
Regenera o manifest.json e cartas.json apenas com imagens existentes.
"""

import json
import os
import re
from pathlib import Path
from PIL import Image
import pytesseract

# Configurar caminho do Tesseract no Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Diretório base
BASE_DIR = Path(__file__).parent.parent
CARTAS_DIR = BASE_DIR / "assets" / "cartas"
DATA_DIR = BASE_DIR / "data"

# Palavras-chave por assunto
ASSUNTOS_KEYWORDS = {
    "Brasil": ["brasil", "brasileiro", "pátria", "nação", "nacional", "país"],
    "Política": ["governo", "presidente", "eleição", "partido", "político", "congresso", "senado", "deputado", "ministro", "democracia"],
    "Economia": ["economia", "inflação", "dólar", "dinheiro", "emprego", "pib", "banco", "juros", "preço", "salário", "imposto"],
    "Educação": ["educação", "escola", "universidade", "ensino", "professor", "aluno", "estudante"],
    "Ética": ["ética", "moral", "valores", "corrupção", "caráter", "honestidade", "justiça"],
    "Família": ["família", "pai", "mãe", "filho", "filha", "esposa", "casamento", "lar"],
    "Religião": ["deus", "jesus", "igreja", "fé", "bíblia", "religião", "espírito"],
    "Sociedade": ["sociedade", "social", "comunidade", "povo", "cidadão", "direito", "lei"],
    "Cultura": ["cultura", "arte", "música", "teatro", "literatura", "história"],
    "Meio Ambiente": ["ambiente", "natureza", "ecologia", "floresta", "poluição"],
    "Saúde": ["saúde", "hospital", "médico", "doença", "remédio"],
    "Trabalho": ["trabalho", "trabalhador", "emprego", "profissão", "empresa"]
}

def classificar_assuntos(texto):
    texto_lower = texto.lower()
    assuntos = []
    for assunto, keywords in ASSUNTOS_KEYWORDS.items():
        for keyword in keywords:
            if keyword in texto_lower:
                assuntos.append(assunto)
                break
    return assuntos if assuntos else ["Geral"]

def extrair_ano(texto, volume):
    ano_min = 1958 if volume == 1 else 2009
    ano_max = 2008 if volume == 1 else 2025

    patterns = [
        r'\b(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})\b',
        r'\b(\d{4})\b',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, texto)
        for match in matches:
            if isinstance(match, tuple):
                ano = int(match[2]) if len(match) > 2 else int(match[0])
            else:
                ano = int(match)
            if ano_min <= ano <= ano_max:
                return ano
    return None

def extrair_data(texto):
    pattern = r'\b(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})\b'
    match = re.search(pattern, texto)
    if match:
        dia, mes, ano = match.groups()
        return f"{int(dia):02d}/{int(mes):02d}/{ano}"
    return None

def processar_ocr(imagem_path):
    try:
        img = Image.open(imagem_path)
        config = '--psm 6 -l por'
        texto = pytesseract.image_to_string(img, config=config)
        return texto.strip()
    except Exception as e:
        print(f"Erro OCR em {imagem_path}: {e}")
        return ""

def reindexar():
    print("="*60)
    print("REINDEXAÇÃO DE CARTAS")
    print("="*60)

    cartas = []
    manifest = []

    for volume in [1, 2]:
        vol_dir = CARTAS_DIR / f"vol{volume}"
        if not vol_dir.exists():
            continue

        imagens = sorted(vol_dir.glob("*.jpg"))
        print(f"\nVolume {volume}: {len(imagens)} imagens")

        for i, img_path in enumerate(imagens, 1):
            if i % 50 == 0:
                print(f"  Processando {i}/{len(imagens)}...")

            # Extrair info do nome do arquivo
            nome = img_path.stem  # vol1_p028_img1
            partes = nome.split('_')
            pagina = int(partes[1][1:])  # p028 -> 28

            # Processar OCR
            texto = processar_ocr(img_path)

            # Extrair metadados
            ano = extrair_ano(texto, volume)
            data_pub = extrair_data(texto)
            assuntos = classificar_assuntos(texto)

            # Caminho relativo
            caminho_rel = str(img_path.relative_to(BASE_DIR)).replace("\\", "/")

            carta = {
                "id": nome,
                "volume": volume,
                "pagina": pagina,
                "ano": ano,
                "data_publicacao": data_pub,
                "imagem": caminho_rel,
                "texto": texto,
                "assuntos": assuntos
            }
            cartas.append(carta)

            manifest.append({
                "id": nome,
                "volume": volume,
                "pagina": pagina,
                "imagem": caminho_rel
            })

    # Salvar arquivos
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # cartas.json
    cartas_path = DATA_DIR / "cartas.json"
    with open(cartas_path, 'w', encoding='utf-8') as f:
        json.dump({"cartas": cartas}, f, ensure_ascii=False, indent=2)
    print(f"\nSalvo: {cartas_path}")

    # manifest.json
    manifest_path = CARTAS_DIR / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Salvo: {manifest_path}")

    # Estatísticas
    print("\n" + "="*60)
    print("RESUMO")
    print("="*60)
    vol1_count = sum(1 for c in cartas if c['volume'] == 1)
    vol2_count = sum(1 for c in cartas if c['volume'] == 2)
    com_ano = sum(1 for c in cartas if c['ano'])

    print(f"Total de cartas: {len(cartas)}")
    print(f"  - Volume 1: {vol1_count}")
    print(f"  - Volume 2: {vol2_count}")
    print(f"Cartas com ano identificado: {com_ano}")

    # Contagem de assuntos
    assuntos_count = {}
    for carta in cartas:
        for assunto in carta['assuntos']:
            assuntos_count[assunto] = assuntos_count.get(assunto, 0) + 1

    print("\nDistribuição por assunto:")
    for assunto, count in sorted(assuntos_count.items(), key=lambda x: -x[1]):
        print(f"  - {assunto}: {count}")

if __name__ == "__main__":
    reindexar()
