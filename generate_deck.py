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

def create_deck():
    output_dir = r"C:\Users\hugov\.gemini\antigravity\scratch\sapiens-presentation-poc"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "Revolucao_Industrial_Antes_Depois.pptx")

    prs = Presentation()
    # 16:9 Aspect Ratio
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Paleta de Cores
    COLOR_BG = RGBColor(15, 23, 42)        # Slate 900
    COLOR_CARD = RGBColor(30, 41, 59)      # Slate 800
    COLOR_BORDER_ANTES = RGBColor(245, 158, 11) # Amber 500
    COLOR_BORDER_DEPOIS = RGBColor(34, 211, 238) # Cyan 400
    COLOR_TEXT_MAIN = RGBColor(248, 250, 252)
    COLOR_TEXT_MUTED = RGBColor(148, 163, 184)
    COLOR_TEXT_AMBER = RGBColor(251, 191, 36)
    COLOR_TEXT_CYAN = RGBColor(103, 232, 249)

    # ==========================================
    # SLIDE 1: CAPA DE ABERTURA
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, COLOR_BG)

    # Badge Sapiens.IA
    badge_box = s1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.33), Inches(0.5))
    tf = badge_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SAPIENS.IA  •  MOTOR DE APRESENTAÇÕES DIDÁTICAS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_AMBER

    # Título Principal
    title_box = s1.shapes.add_textbox(Inches(1.5), Inches(2.3), Inches(10.33), Inches(1.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "A Grande Transformação"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MAIN

    # Subtítulo
    sub_box = s1.shapes.add_textbox(Inches(1.5), Inches(3.8), Inches(9.5), Inches(1.2))
    tf = sub_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Como a Revolução Industrial reconfigurou o trabalho, o tempo e a sociedade: um estudo de caso comparativo entre 1750 e 1850."
    p.font.size = Pt(18)
    p.font.color.rgb = COLOR_TEXT_MUTED

    # Instrução para o usuário
    hint_box = s1.shapes.add_textbox(Inches(1.5), Inches(5.8), Inches(10.33), Inches(0.8))
    tf = hint_box.text_frame
    p = tf.paragraphs[0]
    p.text = "👉 Pressione F5 no PowerPoint e avance os slides com a barra de espaço para ver a mágica do Morph acontecer!"
    p.font.size = Pt(14)
    p.font.italic = True
    p.font.color.rgb = COLOR_TEXT_CYAN

    # ==========================================
    # SLIDE 2: O CENÁRIO 1 (ANTES - EM DESTAQUE)
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, COLOR_BG)
    apply_morph_transition(s2)

    # Cabeçalho
    header_box = s2.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.33), Inches(1.0))
    tf = header_box.text_frame
    p = tf.paragraphs[0]
    p.text = "METODOLOGIA DE ENSINO • ARQUÉTIPO ANTES & DEPOIS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MUTED

    p2 = tf.add_paragraph()
    p2.text = "Passo 1: Compreendendo o Cenário Inicial (1750)"
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_MAIN

    # Card "Antes" Centralizado e Grande
    card1_s2 = s2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(2.5), Inches(1.8), Inches(8.33), Inches(4.8)
    )
    card1_s2.name = "!!CardAntes"  # Nome chave para o Morph!
    card1_s2.fill.solid()
    card1_s2.fill.fore_color.rgb = COLOR_CARD
    card1_s2.line.color.rgb = COLOR_BORDER_ANTES
    card1_s2.line.width = Pt(2)

    tf = card1_s2.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.6)
    tf.margin_right = Inches(0.6)
    tf.margin_top = Inches(0.5)

    p = tf.paragraphs[0]
    p.text = "CENÁRIO 1  •  O MUNDO ARTESANAL"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_AMBER

    p = tf.add_paragraph()
    p.text = "A Vida Rural e o Ritmo da Natureza"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MAIN
    p.space_after = Pt(20)

    pontos_antes = [
        ("Tempo Natural:", " O ritmo do trabalho era ditado pelo sol e pelas estações do ano, sem apitos ou relógios rígidos."),
        ("Controle da Produção:", " O artesão dominava todas as etapas, desde a matéria-prima até a venda final."),
        ("Sociedade Descentralizada:", " Mais de 80% das famílias viviam em aldeias agrícolas, integrando vida doméstica e trabalho.")
    ]

    for titulo, desc in pontos_antes:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + titulo
        run1.font.bold = True
        run1.font.size = Pt(15)
        run1.font.color.rgb = COLOR_TEXT_AMBER

        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(15)
        run2.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(14)

    # ==========================================
    # SLIDE 3: O CENÁRIO COMPARATIVO (MORPH ATIVADO!)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, COLOR_BG)
    apply_morph_transition(s3)  # <-- Aqui o PowerPoint calcula o movimento!

    # Cabeçalho
    header_box = s3.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(1.0))
    tf = header_box.text_frame
    p = tf.paragraphs[0]
    p.text = "METODOLOGIA DE ENSINO • ARQUÉTIPO ANTES & DEPOIS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MUTED

    p2 = tf.add_paragraph()
    p2.text = "Passo 2: O Contraste Histórico (1750 vs 1850)"
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_MAIN

    # Card "Antes" ENCOLHIDO E DESLOCADO PARA A ESQUERDA
    # Mesmo nome !!CardAntes para o PowerPoint fazer o deslizamento suave!
    card1_s3 = s3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8)
    )
    card1_s3.name = "!!CardAntes"  # Mesmo nome!
    card1_s3.fill.solid()
    card1_s3.fill.fore_color.rgb = COLOR_CARD
    card1_s3.line.color.rgb = COLOR_BORDER_ANTES
    card1_s3.line.width = Pt(1.5)

    tf = card1_s3.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_right = Inches(0.4)
    tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "ANTES  •  1750"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_AMBER

    p = tf.add_paragraph()
    p.text = "O Trabalho Artesanal"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MAIN
    p.space_after = Pt(14)

    for titulo, desc in pontos_antes:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + titulo
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = COLOR_TEXT_AMBER

        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(13)
        run2.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(10)

    # Card "Depois" SURGINDO À DIREITA
    card2_s3 = s3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8)
    )
    card2_s3.name = "!!CardDepois"
    card2_s3.fill.solid()
    card2_s3.fill.fore_color.rgb = COLOR_CARD
    card2_s3.line.color.rgb = COLOR_BORDER_DEPOIS
    card2_s3.line.width = Pt(2)

    tf = card2_s3.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.4)
    tf.margin_right = Inches(0.4)
    tf.margin_top = Inches(0.4)

    p = tf.paragraphs[0]
    p.text = "DEPOIS  •  1850"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_CYAN

    p = tf.add_paragraph()
    p.text = "A Revolução das Fábricas"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MAIN
    p.space_after = Pt(14)

    pontos_depois = [
        ("Tempo do Relógio:", " Turnos exaustivos de 14h regulados rigidamente por apitos e supervisores."),
        ("Divisão do Trabalho:", " O operário virou peça da máquina, repetindo uma única tarefa mecânica."),
        ("Explosão Urbana:", " Migração em massa para cidades industriais insalubres como Manchester.")
    ]

    for titulo, desc in pontos_depois:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + titulo
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = COLOR_TEXT_CYAN

        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(13)
        run2.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(10)

    prs.save(output_path)
    print(f"Sucesso! Apresentação gerada em: {output_path}")

if __name__ == "__main__":
    create_deck()
