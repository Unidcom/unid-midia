from pathlib import Path
from shutil import copy2
from io import BytesIO

import pypdfium2 as pdfium
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs" / "referencias"
OUTPUT = ROOT / "assets" / "midias"
IMAGES = ROOT / "assets" / "images"

PDF_PAGES = [
    ("Outdoor Umuarama.pdf", 1, "outdoor-umuarama-pontos-pagina-01.png"),
    ("PARANÁ _ PROPOSTA_Mídia_goioerê.pdf", 9, "trade-parana-goioere-investimento-pagina-09.png"),
]

PDF_EMBEDDED_IMAGES = [
    ("Outdoor Cianorte Bissemana.pdf", 1, 5, "outdoor-cianorte-cia-403-rodovia-pr-323-sentido-cianorte.jpg"),
    ("Outdoor Cianorte Bissemana.pdf", 1, 9, "outdoor-cianorte-cia-404-rodovia-pr-323-sentido-maringa.jpg"),
    ("Outdoor Cianorte Bissemana.pdf", 1, 14, "outdoor-cianorte-cia-405-av-america-av-brasil.jpg"),
]

UMUARAMA_OUTDOOR_IMAGES = [
    (1, "ponto-01-rodovia-saida-serra-dourados-sentido-umuarama.jpg"),
    (2, "ponto-02-avenida-aracaju-mercado-atacadao.jpg"),
    (3, "ponto-03-rodovia-pr-323-levo-alimentos-sentido-mariluz.jpg"),
    (4, "ponto-04-avenida-parigot-de-souza-feira-domingo.jpg"),
    (5, "ponto-05-rua-arapongas-deposito-sao-jose.jpg"),
    (6, "ponto-06-avenida-ariovaldo-sentido-cidade.jpg"),
    (7, "ponto-07-avenida-manaus-mercado-amigao.jpg"),
    (8, "ponto-08-avenida-jose-dias-lopes-sentido-uopecan.jpg"),
    (9, "ponto-09-avenida-antonio-ostrenski-hospital-cemil.jpg"),
    (10, "ponto-10-avenida-ariovaldo-rodrigues-max-atacado-sentido-centro.jpg"),
    (11, "ponto-11-avenida-parana-lago-municipal-sentido-uopecan.jpg"),
    (12, "ponto-12-avenida-ariovaldo-rodrigues-max-atacado-sentido-rodovia.jpg"),
    (13, "ponto-13-avenida-angelo-moreira-delegacia-upa-sicoob.jpg"),
    (14, "ponto-14-avenida-parigot-de-souza-avenida-guanabara.jpg"),
    (15, "ponto-15-avenida-paranapanema-tiro-de-guerra.jpg"),
    (16, "ponto-16-avenida-parana-lago-municipal-sentido-faculdade-alfa.jpg"),
    (17, "ponto-17-rotatoria-aceu-guri-entrada-cidade.jpg"),
    (18, "ponto-18-avenida-paulo-pedrosa-sorveteria-ditalia.jpg"),
    (19, "ponto-19-rodovia-serra-umuarama-parque-jaboticabeira.jpg"),
    (20, "ponto-20-avenida-parigot-de-souza-alfinha-mont-blant.jpg"),
    (21, "ponto-21-avenida-ariovaldo-rodrigues-max-atacado.jpg"),
    (22, "ponto-22-avenida-celso-garcia-cid-hospital-cemil.jpg"),
    (23, "ponto-23-avenida-angelo-moreira-uopecan.jpg"),
    (24, "ponto-24-avenida-maringa-sentido-unipar-lamore.jpg"),
    (25, "ponto-25-rua-arapongas-colegio-alfa-posto-portuga.jpg"),
    (26, "ponto-26-avenida-pirapo-avenida-rolandia-unipar.jpg"),
    (27, "ponto-27-estrada-xambre-aceu-sorvetes-guri.jpg"),
    (28, "ponto-28-avenida-parana-shopping-centro-xambre.jpg"),
]

PDV_MERCADO_IMAGES = [
    (5, 4, "faixa-gradil.jpg"),
    (5, 5, "totem-entrada.jpg"),
    (6, 4, "display-manopla.jpg"),
    (6, 5, "adesivo-cesta-compras.jpg"),
    (7, 4, "adesivo-saida-piso.jpg"),
    (7, 5, "adesivo-mesa-cafeteria.jpg"),
]

SUPER_TELA_IMAGES = [
    (2, 0, "super-tela-av-parana-foto-01.jpg"),
    (2, 1, "super-tela-av-parana-foto-02.jpg"),
]

LEBLON_IMAGES = [
    (2, 0, "painel-led-posto-leblon-foto-01.jpg"),
    (2, 1, "painel-led-posto-leblon-foto-02.jpg"),
    (2, 2, "painel-led-posto-leblon-foto-03.jpg"),
    (2, 3, "painel-led-posto-leblon-foto-04.jpg"),
    (2, 4, "painel-led-posto-leblon-foto-05.jpg"),
]

AVENIDA_IMAGES = [
    (2, 0, "painel-led-posto-avenida-foto-01.jpg"),
    (2, 1, "painel-led-posto-avenida-foto-02.jpg"),
    (2, 2, "painel-led-posto-avenida-foto-03.jpg"),
    (2, 3, "painel-led-posto-avenida-foto-04.jpg"),
]

ITAMARATY_IMAGES = [
    (2, 0, "painel-led-posto-itamaraty-foto-01.jpg"),
    (2, 1, "painel-led-posto-itamaraty-foto-02.jpg"),
    (2, 2, "painel-led-posto-itamaraty-foto-03.jpg"),
]

IMAGE_COPIES = [
    ("busdoor Umuarama .png", "busdoor-umuarama-orcamento.png"),
    ("Outdoor Cianorte 1.jpeg", "outdoor-cianorte-av-makio-sato.jpeg"),
    ("Outdoor Cianorte 2.jpeg", "outdoor-cianorte-av-espirito-santo.jpeg"),
    ("Outdoor Cianorte 3.jpeg", "outdoor-cianorte-av-parana-banco-do-brasil-indisponivel.jpeg"),
    ("Outdoor Cianorte 4.jpeg", "outdoor-cianorte-av-genei-uehara-indisponivel.jpeg"),
    ("Outdoor Cianorte 5.jpeg", "outdoor-cianorte-praca-makio-sato-indisponivel.jpeg"),
]


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    umuarama_outdoor = IMAGES / "umuarama" / "outdoor"
    umuarama_outdoor.mkdir(parents=True, exist_ok=True)
    for source_name, output_name in IMAGE_COPIES:
        copy2(SOURCE / source_name, OUTPUT / output_name)

    for source_name, page_number, image_index, output_name in PDF_EMBEDDED_IMAGES:
        page = PdfReader(SOURCE / source_name).pages[page_number - 1]
        (OUTPUT / output_name).write_bytes(list(page.images)[image_index].data)

    umuarama = PdfReader(SOURCE / "Outdoor Umuarama.pdf")
    for page_number, output_name in UMUARAMA_OUTDOOR_IMAGES:
        image = list(umuarama.pages[page_number - 1].images)[1]
        (umuarama_outdoor / output_name).write_bytes(image.data)

    pdv_mercado = IMAGES / "pdv-mercado"
    pdv_mercado.mkdir(parents=True, exist_ok=True)
    pdv_pdf = PdfReader(next(SOURCE.glob("*PROPOSTA*goioer*.pdf")))
    for page_number, image_index, output_name in PDV_MERCADO_IMAGES:
        image = list(pdv_pdf.pages[page_number - 1].images)[image_index]
        with Image.open(BytesIO(image.data)) as source_image:
            source_image.convert("RGB").save(pdv_mercado / output_name, quality=95)

    super_tela = IMAGES / "umuarama" / "painel-led"
    super_tela.mkdir(parents=True, exist_ok=True)
    super_tela_pdf = PdfReader(next(SOURCE.glob("*LED SUPER TELA*2025*.pdf")))
    for page_number, image_index, output_name in SUPER_TELA_IMAGES:
        image = list(super_tela_pdf.pages[page_number - 1].images)[image_index]
        with Image.open(BytesIO(image.data)) as source_image:
            source_image.convert("RGB").save(super_tela / output_name, quality=95)

    leblon_pdf = PdfReader(next(SOURCE.glob("*LED SUPER TELA*Posto Leblon*.pdf")))
    for page_number, image_index, output_name in LEBLON_IMAGES:
        image = list(leblon_pdf.pages[page_number - 1].images)[image_index]
        with Image.open(BytesIO(image.data)) as source_image:
            source_image.convert("RGB").save(super_tela / output_name, quality=95)

    avenida_pdf = PdfReader(next(SOURCE.glob("*PAINEL DE LED*Posto Avenida*2024*.pdf")))
    for page_number, image_index, output_name in AVENIDA_IMAGES:
        image = list(avenida_pdf.pages[page_number - 1].images)[image_index]
        with Image.open(BytesIO(image.data)) as source_image:
            source_image.convert("RGB").save(super_tela / output_name, quality=95)

    itamaraty_pdf = PdfReader(next(SOURCE.glob("*PAINEL DE LED*Posto Itamaraty*2024*.pdf")))
    for page_number, image_index, output_name in ITAMARATY_IMAGES:
        image = list(itamaraty_pdf.pages[page_number - 1].images)[image_index]
        with Image.open(BytesIO(image.data)) as source_image:
            source_image.convert("RGB").save(super_tela / output_name, quality=95)

    for source_name, page_number, output_name in PDF_PAGES:
        document = pdfium.PdfDocument(str(SOURCE / source_name))
        document[page_number - 1].render(scale=2).to_pil().save(OUTPUT / output_name)
        document.close()


if __name__ == "__main__":
    main()
