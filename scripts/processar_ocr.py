#!/usr/bin/env python3
"""
Script para processar OCR nas imagens das cartas e criar o índice.
Usa Tesseract OCR com idioma português.
"""

import json
import os
import re
from pathlib import Path
from PIL import Image
import pytesseract

# Configurar caminho do Tesseract no Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Diretório base do projeto
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "cartas"
DATA_DIR = BASE_DIR / "data"

# Palavras-chave por assunto para classificação automática
ASSUNTOS_KEYWORDS = {
    "Brasil": [
        "brasil", "brasileiro", "brasileiros", "pátria", "nação", "nacional",
        "país", "terra", "verde-amarelo", "bandeira", "hino"
    ],
    "Política": [
        "governo", "presidente", "eleição", "eleições", "partido", "político",
        "políticos", "política", "congresso", "senado", "câmara", "deputado",
        "senador", "ministro", "prefeito", "governador", "voto", "votos",
        "democracia", "república", "estado", "poder"
    ],
    "Economia": [
        "economia", "econômico", "inflação", "dólar", "real", "dinheiro",
        "emprego", "desemprego", "pib", "banco", "juros", "preço", "preços",
        "salário", "imposto", "impostos", "crise", "mercado", "indústria"
    ],
    "Educação": [
        "educação", "escola", "escolas", "universidade", "ensino", "professor",
        "professores", "aluno", "alunos", "estudante", "estudantes", "aula",
        "livro", "livros", "aprender", "conhecimento", "formação"
    ],
    "Ética": [
        "ética", "moral", "valores", "honestidade", "corrupção", "corrupto",
        "caráter", "dignidade", "integridade", "justiça", "verdade", "mentira",
        "honra", "respeito", "decência"
    ],
    "Família": [
        "família", "pai", "mãe", "filho", "filhos", "filha", "esposa", "marido",
        "casamento", "lar", "casa", "amor", "criança", "crianças", "pais"
    ],
    "Religião": [
        "deus", "jesus", "cristo", "igreja", "fé", "bíblia", "oração",
        "religião", "cristão", "católico", "evangélico", "espírito", "santo",
        "pecado", "salvação", "céu"
    ],
    "Sociedade": [
        "sociedade", "social", "comunidade", "povo", "população", "cidadão",
        "cidadãos", "direito", "direitos", "dever", "deveres", "lei", "leis",
        "ordem", "segurança", "violência", "crime"
    ],
    "Cultura": [
        "cultura", "cultural", "arte", "artista", "música", "teatro", "cinema",
        "literatura", "tradição", "história", "histórico", "patrimônio"
    ],
    "Meio Ambiente": [
        "ambiente", "ambiental", "natureza", "ecologia", "floresta", "água",
        "poluição", "sustentável", "preservação", "animais", "plantas"
    ],
    "Saúde": [
        "saúde", "hospital", "médico", "doença", "remédio", "tratamento",
        "paciente", "sus", "medicina", "cura", "prevenção"
    ],
    "Trabalho": [
        "trabalho", "trabalhador", "emprego", "profissão", "carreira",
        "empresa", "negócio", "patrão", "funcionário", "salário"
    ]
}


def classificar_assuntos(texto: str) -> list:
    """
    Classifica o texto em assuntos baseado em palavras-chave.

    Args:
        texto: Texto extraído via OCR

    Returns:
        Lista de assuntos identificados
    """
    texto_lower = texto.lower()
    assuntos_encontrados = []

    for assunto, keywords in ASSUNTOS_KEYWORDS.items():
        for keyword in keywords:
            if keyword in texto_lower:
                assuntos_encontrados.append(assunto)
                break  # Um match por assunto é suficiente

    return assuntos_encontrados if assuntos_encontrados else ["Geral"]


def extrair_ano_do_texto(texto: str, volume: int) -> int:
    """
    Tenta extrair o ano da carta do texto OCR.

    Args:
        texto: Texto extraído via OCR
        volume: Número do volume (usado para estimar range de anos)

    Returns:
        Ano encontrado ou None
    """
    # Range de anos por volume
    if volume == 1:
        ano_min, ano_max = 1958, 2008
    else:
        ano_min, ano_max = 2009, 2025

    # Procurar padrões de data
    # dd/mm/yyyy ou dd-mm-yyyy ou dd.mm.yyyy
    patterns = [
        r'\b(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})\b',  # dd/mm/yyyy
        r'\b(\d{4})\b',  # Ano isolado
    ]

    for pattern in patterns:
        matches = re.findall(pattern, texto)
        for match in matches:
            if isinstance(match, tuple):
                # Data completa - pegar o ano
                ano = int(match[2]) if len(match) > 2 else int(match[0])
            else:
                ano = int(match)

            if ano_min <= ano <= ano_max:
                return ano

    return None


def extrair_data_publicacao(texto: str) -> str:
    """
    Tenta extrair a data de publicação do texto.

    Args:
        texto: Texto extraído via OCR

    Returns:
        Data no formato dd/mm/yyyy ou None
    """
    # Padrão de data completa
    pattern = r'\b(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})\b'
    match = re.search(pattern, texto)

    if match:
        dia, mes, ano = match.groups()
        return f"{int(dia):02d}/{int(mes):02d}/{ano}"

    return None


def processar_imagem_ocr(imagem_path: Path) -> str:
    """
    Processa uma imagem com OCR e retorna o texto extraído.

    Args:
        imagem_path: Caminho da imagem

    Returns:
        Texto extraído da imagem
    """
    try:
        img = Image.open(imagem_path)

        # Configuração do Tesseract para português
        config = '--psm 6 -l por'  # PSM 6: Assume uniform block of text

        texto = pytesseract.image_to_string(img, config=config)

        # Limpar texto
        texto = texto.strip()

        return texto
    except Exception as e:
        print(f"Erro ao processar OCR em {imagem_path}: {e}")
        return ""


def processar_todas_imagens():
    """
    Processa todas as imagens com OCR e cria o índice.
    """
    print("="*60)
    print("PROCESSAMENTO OCR - SILVANO CORRÊA")
    print("="*60)

    # Carregar manifesto de imagens
    manifest_path = ASSETS_DIR / "manifest.json"
    if not manifest_path.exists():
        print("ERRO: Manifesto não encontrado. Execute extrair_cartas.py primeiro.")
        return

    with open(manifest_path, 'r', encoding='utf-8') as f:
        imagens = json.load(f)

    print(f"Total de imagens a processar: {len(imagens)}")

    cartas = []
    processadas = 0

    for img_info in imagens:
        processadas += 1
        imagem_path = BASE_DIR / img_info['imagem']

        if processadas % 50 == 0:
            print(f"Processando imagem {processadas}/{len(imagens)}...")

        # Processar OCR
        texto = processar_imagem_ocr(imagem_path)

        # Extrair metadados do texto
        volume = img_info['volume']
        ano = extrair_ano_do_texto(texto, volume)
        data_pub = extrair_data_publicacao(texto)
        assuntos = classificar_assuntos(texto)

        # Criar entrada da carta
        carta = {
            "id": img_info['id'],
            "volume": volume,
            "pagina": img_info['pagina'],
            "ano": ano,
            "data_publicacao": data_pub,
            "imagem": img_info['imagem'].replace("\\", "/"),
            "texto": texto,
            "assuntos": assuntos
        }

        cartas.append(carta)

    # Criar diretório de dados se não existir
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Salvar índice de cartas
    cartas_path = DATA_DIR / "cartas.json"
    with open(cartas_path, 'w', encoding='utf-8') as f:
        json.dump({"cartas": cartas}, f, ensure_ascii=False, indent=2)

    print("\n" + "="*60)
    print("RESUMO DO PROCESSAMENTO")
    print("="*60)
    print(f"Total de cartas processadas: {len(cartas)}")
    print(f"  - Volume 1: {sum(1 for c in cartas if c['volume'] == 1)}")
    print(f"  - Volume 2: {sum(1 for c in cartas if c['volume'] == 2)}")

    # Estatísticas de assuntos
    assuntos_count = {}
    for carta in cartas:
        for assunto in carta['assuntos']:
            assuntos_count[assunto] = assuntos_count.get(assunto, 0) + 1

    print("\nDistribuição por assunto:")
    for assunto, count in sorted(assuntos_count.items(), key=lambda x: -x[1]):
        print(f"  - {assunto}: {count}")

    # Estatísticas de anos
    anos_count = {}
    for carta in cartas:
        if carta['ano']:
            anos_count[carta['ano']] = anos_count.get(carta['ano'], 0) + 1

    print(f"\nCartas com ano identificado: {sum(anos_count.values())}/{len(cartas)}")
    print(f"Índice salvo em: {cartas_path}")

    return cartas


if __name__ == "__main__":
    processar_todas_imagens()
