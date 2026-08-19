from pathlib import Path
import re
import xml.etree.ElementTree as ET

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


BASE_DIR = Path(__file__).parent
XML_PATH = BASE_DIR / "catalogo-midias.xml"
OUTPUT_PATH = BASE_DIR.parent / "base-precificacao" / "catalogo-midias.xlsx"

HEADER_FILL = PatternFill("solid", fgColor="0F766E")
HEADER_FONT = Font(color="FFFFFF", bold=True)
EDITABLE_FILL = PatternFill("solid", fgColor="FFF2CC")
CURRENCY_FORMAT = 'R$ #,##0.00'


def text(element, tag):
    child = element.find(tag)
    return child.text.strip() if child is not None and child.text else ""


def attr(element, name):
    return element.get(name, "")


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def create_sheet(workbook, title, headers):
    sheet = workbook.create_sheet(title)
    sheet.append(headers)
    for cell in sheet[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"
    return sheet


def format_sheet(sheet, currency_columns=(), editable_columns=()):
    for row in sheet.iter_rows(min_row=2):
        for column in currency_columns:
            row[column - 1].number_format = CURRENCY_FORMAT
        for column in editable_columns:
            row[column - 1].fill = EDITABLE_FILL
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)

    for column_cells in sheet.columns:
        width = max(len(str(cell.value or "")) for cell in column_cells) + 2
        sheet.column_dimensions[get_column_letter(column_cells[0].column)].width = min(width, 55)

    sheet.row_dimensions[1].height = 24


def main():
    root = ET.parse(XML_PATH).getroot()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    workbook = Workbook()
    workbook.remove(workbook.active)

    midias = create_sheet(
        workbook,
        "Midias",
        [
            "ID", "Tipo", "Cidade", "Nome", "Ativa", "Disponibilidade", "Fonte", "Status do preco",
            "Localizacao", "Largura (m)", "Altura (m)", "Faces maximas",
            "Insercoes/dia", "Horas/dia", "Observacao",
        ],
    )
    precos = create_sheet(
        workbook,
        "Precos",
        [
            "Midia ID", "Categoria", "Codigo", "Descricao", "Unidade", "Quantidade",
            "Meses", "Dias", "Valor (BRL)",
        ],
    )
    pontos = create_sheet(
        workbook,
        "Pontos",
        ["Midia ID", "Ponto ID", "Codigo fornecedor", "Cidade", "Localizacao"],
    )
    fontes = create_sheet(
        workbook,
        "Fontes",
        ["Fonte ID", "Arquivo Markdown", "Duplicada de", "Tipo de extracao"],
    )
    condicoes = create_sheet(
        workbook,
        "Condicoes",
        ["Midia ID", "Condicao"],
    )

    for source in root.findall("./fontes/fonte"):
        fontes.append([
            attr(source, "id"), attr(source, "arquivo"), attr(source, "duplicada-de"),
            attr(source, "extracao"),
        ])

    for media in root.findall("./midias/midia"):
        media_id = attr(media, "id")
        formato = media.find("formato")
        exibicao = media.find("exibicao")
        midias.append([
            media_id, attr(media, "tipo"), attr(media, "cidade"), text(media, "nome"),
            attr(media, "ativo"), attr(media, "disponibilidade"), attr(media, "fonte"),
            attr(media, "preco-status"), text(media, "localizacao"),
            attr(formato, "largura-m") if formato is not None else "",
            attr(formato, "altura-m") if formato is not None else "",
            attr(formato, "faces-maximas") if formato is not None else "",
            attr(exibicao, "insercoes-dia") if exibicao is not None else "",
            attr(exibicao, "horas-dia") if exibicao is not None else "", text(media, "observacao"),
        ])

        for price_group in media.findall("precos"):
            for price in list(price_group):
                value = attr(price, "valor")
                precos.append([
                    media_id, price.tag, attr(price, "codigo"), attr(price, "descricao"),
                    attr(price, "unidade"), attr(price, "quantidade"), attr(price, "meses"),
                    attr(price, "dias"), float(value) if value else None,
                ])

        for point in media.findall("./pontos/ponto"):
            pontos.append([
                media_id, attr(point, "id"), attr(point, "codigo-fornecedor"),
                attr(media, "cidade"), point.text.strip() if point.text else "",
            ])

        for city in media.findall("./cidades/cidade"):
            city_name = city.text.strip() if city.text else ""
            pontos.append([
                media_id, f"{media_id}-{slug(city_name)}", "", city_name,
                "Supermercado Parana",
            ])

        for condition in media.findall("./condicoes/condicao"):
            condicoes.append([media_id, condition.text.strip() if condition.text else ""])

    format_sheet(midias, editable_columns=(2, 3, 4, 5, 6, 8, 9, 15))
    format_sheet(precos, currency_columns=(9,), editable_columns=(4, 5, 6, 7, 8, 9))
    format_sheet(pontos, editable_columns=(3, 4, 5))
    format_sheet(fontes)
    format_sheet(condicoes, editable_columns=(2,))

    workbook.save(OUTPUT_PATH)
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
