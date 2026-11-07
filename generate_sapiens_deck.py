import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree

def apply_morph_transition(slide):
    morph_xml = (
        '<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">\n'
        '  <mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">\n'
        '    <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="slow" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" p14:dur="1200">\n'
        '      <p159:morph option="byObject"/>\n'
        '    </p:transition>\n'
        '  </mc:Choice>\n'
        '  <mc:Fallback xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">\n'
        '    <p:transition spd="slow">\n'
        '      <p:fade/>\n'
        '    </p:transition>\n'
        '  </mc:Fallback>\n'
        '</mc:AlternateContent>'
    )
    elem = etree.fromstring(morph_xml)
    slide._element.append(elem)

def set_slide_background(slide, color_rgb):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color_rgb

def create_sapiens_deck():
    output_dir = r"C:\Users\hugov\.gemini\antigravity\scratch\sapiens-presentation-poc"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "Revolucao_Industrial_Sapiens_Oficial.pptx")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Paleta Oficial Coleção Traço & Saber (Sapiens.IA v3.5)
    COLOR_BG = RGBColor(0xF7, 0xF3, 0xE8)          # Bege Claro (#F7F3E8)
    COLOR_CARD = RGBColor(0xEA, 0xDC, 0xCB)        # Areia (#EADCCB)
    COLOR_TERRACOTA = RGBColor(0xC2, 0x8A, 0x57)   # Terracota (#C28A57)
    COLOR_AZUL_ACINZ = RGBColor(0x6E, 0x8A, 0x9D)  # Azul Acinzentado (#6E8A9D)
    COLOR_MARROM = RGBColor(0xA8, 0x87, 0x6D)      # Marrom Claro (#A8876D)
    COLOR_OLIVA = RGBColor(0x8A, 0x9B, 0x7E)       # Verde Oliva (#8A9B7E)
    COLOR_TEXT_MAIN = RGBColor(0x38, 0x2D, 0x27)   # Marrom Escuro Nobre (#382D27 - sem preto puro)
    COLOR_TEXT_MUTED = RGBColor(0x6A, 0x58, 0x4D)  # Suporte (#6A584D)
    FONT_FAMILY = "Segoe UI"

    # ==========================================
    # SLIDE 1: CAPA EDITORIAL SAPIENS.IA
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, COLOR_BG)

    # Moldura Decorativa Sutil Traço Fino
    frame = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    frame.fill.background()
    frame.line.color.rgb = COLOR_MARROM
    frame.line.width = Pt(1)

    # Badge Sapiens.IA Traço & Saber
    badge_box = s1.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10.33), Inches(0.5))
    tf = badge_box.text_frame
    p = tf.paragraphs[0]
    p.text = "SAPIENS.IA  •  COLEÇÃO TRAÇO & SABER  •  8º ANO"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TERRACOTA

    # Título Principal
    title_box = s1.shapes.add_textbox(Inches(1.5), Inches(2.1), Inches(10.33), Inches(1.6))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "A Grande Transformação:\nDa Oficina à Fábrica"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Subtítulo com Palavra-Chave Contextualizada
    sub_box = s1.shapes.add_textbox(Inches(1.5), Inches(3.9), Inches(9.8), Inches(1.2))
    tf = sub_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "A Revolução Industrial inglesa alterou profundamente as relações sociais, substituindo a manufatura doméstica pelo trabalho fabril assalariado."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(18)
    p.font.color.rgb = COLOR_TEXT_MUTED

    # Habilidade BNCC
    bncc_box = s1.shapes.add_textbox(Inches(1.5), Inches(5.4), Inches(10.33), Inches(0.6))
    tf = bncc_box.text_frame
    p = tf.paragraphs[0]
    run_bncc = p.add_run()
    run_bncc.text = "OBJETO DE CONHECIMENTO • BNCC EF08HI03: "
    run_bncc.font.name = FONT_FAMILY
    run_bncc.font.bold = True
    run_bncc.font.size = Pt(11)
    run_bncc.font.color.rgb = COLOR_AZUL_ACINZ

    run_desc = p.add_run()
    run_desc.text = "Os impactos da tecnologia na organização do trabalho."
    run_desc.font.name = FONT_FAMILY
    run_desc.font.size = Pt(11)
    run_desc.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================
    # SLIDE 2: O CENÁRIO 1 (O ANTES - EM DESTAQUE)
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, COLOR_BG)
    apply_morph_transition(s2)

    # Cabeçalho
    header_box = s2.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.33), Inches(1.0))
    tf = header_box.text_frame
    p = tf.paragraphs[0]
    p.text = "COMPARAÇÃO VISUAL  •  ÁRVORE DE DECISÃO SAPIENS"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_AZUL_ACINZ

    p2 = tf.add_paragraph()
    p2.text = "1750: A Manufatura e o Tempo da Natureza"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_MAIN

    # Card "Antes" Centralizado e Grande (Nomeado para Morph)
    card1_s2 = s2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(2.5), Inches(1.8), Inches(8.33), Inches(4.8)
    )
    card1_s2.name = "!!CardAntes"
    card1_s2.fill.solid()
    card1_s2.fill.fore_color.rgb = COLOR_CARD
    card1_s2.line.color.rgb = COLOR_TERRACOTA
    card1_s2.line.width = Pt(1.5)

    tf = card1_s2.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.6)
    tf.margin_right = Inches(0.6)
    tf.margin_top = Inches(0.5)

    p = tf.paragraphs[0]
    p.text = "CENÁRIO HISTÓRICO 1  •  O MUNDO ARTESANAL"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TERRACOTA

    p = tf.add_paragraph()
    p.text = "Produção Familiar e Ritmo Natural"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MAIN
    p.space_after = Pt(20)

    pontos_antes = [
        ("Tempo da Natureza:", " As tarefas diárias eram ditadas pelo nascer do sol e pelas colheitas agrícolas, sem horários rígidos de relógio."),
        ("Autonomia Produtiva:", " O artesão conhecia e realizava sozinho todas as etapas, desde a escolha da matéria-prima até a costura final."),
        ("Espaço Doméstico:", " As oficinas funcionavam dentro das próprias casas nas aldeias rurais, unindo trabalho e vida em família.")
    ]

    for titulo, desc in pontos_antes:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + titulo
        run1.font.name = FONT_FAMILY
        run1.font.bold = True
        run1.font.size = Pt(14)
        run1.font.color.rgb = COLOR_TERRACOTA

        run2 = p.add_run()
        run2.text = desc
        run2.font.name = FONT_FAMILY
        run2.font.size = Pt(14)
        run2.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(14)

    # ==========================================
    # SLIDE 3: O CONTRASTE (MORPH SUAVE SAPIENS!)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, COLOR_BG)
    apply_morph_transition(s3)

    header_box = s3.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(1.0))
    tf = header_box.text_frame
    p = tf.paragraphs[0]
    p.text = "COMPARAÇÃO VISUAL  •  ÁRVORE DE DECISÃO SAPIENS"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_AZUL_ACINZ

    p2 = tf.add_paragraph()
    p2.text = "O Contraste Pedagógico: 1750 vs 1850"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_MAIN

    # Card "Antes" Deslocado para Esquerda com Morph
    card1_s3 = s3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8)
    )
    card1_s3.name = "!!CardAntes"
    card1_s3.fill.solid()
    card1_s3.fill.fore_color.rgb = COLOR_CARD
    card1_s3.line.color.rgb = COLOR_TERRACOTA
    card1_s3.line.width = Pt(1.5)

    tf = card1_s3.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_right = Inches(0.4)
    tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "ANTES  •  SÉCULO XVIII (1750)"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TERRACOTA

    p = tf.add_paragraph()
    p.text = "O Mundo da Oficina"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MAIN
    p.space_after = Pt(14)

    for titulo, desc in pontos_antes:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + titulo
        run1.font.name = FONT_FAMILY
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = COLOR_TERRACOTA

        run2 = p.add_run()
        run2.text = desc
        run2.font.name = FONT_FAMILY
        run2.font.size = Pt(13)
        run2.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(10)

    # Card "Depois" Emergindo à Direita
    card2_s3 = s3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8)
    )
    card2_s3.name = "!!CardDepois"
    card2_s3.fill.solid()
    card2_s3.fill.fore_color.rgb = COLOR_CARD
    card2_s3.line.color.rgb = COLOR_AZUL_ACINZ
    card2_s3.line.width = Pt(2)

    tf = card2_s3.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_right = Inches(0.4)
    tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "DEPOIS  •  SÉCULO XIX (1850)"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_AZUL_ACINZ

    p = tf.add_paragraph()
    p.text = "O Mundo da Fábrica"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MAIN
    p.space_after = Pt(14)

    pontos_depois = [
        ("Tempo do Relógio:", " Os turnos passaram a ser rigorosamente cronometrados pelo apito das fábricas e pelos supervisores."),
        ("Divisão do Trabalho:", " O operário virou uma peça da máquina, executando um único movimento repetitivo ao longo do dia."),
        ("Cidades Fabris:", " Milhares de famílias migraram para centros industriais insalubres e poluídos, como a cidade de Manchester.")
    ]

    for titulo, desc in pontos_depois:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + titulo
        run1.font.name = FONT_FAMILY
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = COLOR_AZUL_ACINZ

        run2 = p.add_run()
        run2.text = desc
        run2.font.name = FONT_FAMILY
        run2.font.size = Pt(13)
        run2.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(10)

    prs.save(output_path)
    print(f"Sucesso! Apresentação Oficial Sapiens gerada em: {output_path}")

if __name__ == "__main__":
    create_sapiens_deck()
