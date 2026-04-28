import streamlit as st
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import io

# ─────────────────────────────────────────────────────────────
#  REGISTRACE FONTU
# ─────────────────────────────────────────────────────────────
FONT_SEARCH_PATHS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    "/Library/Fonts/Liberation Sans.ttf",
    "C:/Windows/Fonts/LiberationSans-Regular.ttf",
]
FONT_BOLD_SEARCH_PATHS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    "/Library/Fonts/Liberation Sans Bold.ttf",
    "C:/Windows/Fonts/LiberationSans-Bold.ttf",
]

def find_font(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None

font_regular_path = find_font(FONT_SEARCH_PATHS)
font_bold_path    = find_font(FONT_BOLD_SEARCH_PATHS)

if font_regular_path and font_bold_path:
    pdfmetrics.registerFont(TTFont("AppFont",      font_regular_path))
    pdfmetrics.registerFont(TTFont("AppFont-Bold", font_bold_path))
    FONT_NORMAL = "AppFont"
    FONT_BOLD   = "AppFont-Bold"
else:
    import urllib.request, tempfile
    FONT_DIR = tempfile.gettempdir()
    NOTO_URLS = {
        "AppFont":      "https://fonts.gstatic.com/s/notosans/v36/o-0IIpQlx3QUlC5A4PNb4j5Ba_2c7A.ttf",
        "AppFont-Bold": "https://fonts.gstatic.com/s/notosans/v36/o-0NIpQlx3QUlC5A4PNjXhFVadyB1Wk.ttf",
    }
    for name, url in NOTO_URLS.items():
        path = os.path.join(FONT_DIR, f"{name}.ttf")
        if not os.path.exists(path):
            urllib.request.urlretrieve(url, path)
        pdfmetrics.registerFont(TTFont(name, path))
    FONT_NORMAL = "AppFont"
    FONT_BOLD   = "AppFont-Bold"

# ─────────────────────────────────────────────────────────────
#  NASTAVENÍ STRÁNKY
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Karta klienta UNIQA", layout="wide")

POJISTOVNY = ["-", "UNIQA", "Allianz", "Generali ČP", "Kooperativa", "ČPP", "ČSOB", "Pillow", "Direct", "MetLife", "KB"]
STATUSY    = ["-", "Mám / OK", "Chci řešit", "Chci revizi", "Nezájem"]

UNIQA_BLUE  = colors.HexColor("#003399")
UNIQA_LIGHT = colors.HexColor("#e8edf7")
UNIQA_GRAY  = colors.HexColor("#f5f7f9")
WHITE       = colors.white
BLACK       = colors.black

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    h1 { color: #003399; }
    .stCheckbox { margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 Digitální Karta Klienta UNIQA")

# ─────────────────────────────────────────────────────────────
#  FORMULÁŘ
# ─────────────────────────────────────────────────────────────
with st.form("hlavni_formular"):
    st.subheader("👤 Osobní údaje a Plán")
    c1, c2, c3 = st.columns(3)
    with c1:
        jmeno   = st.text_input("Jméno a příjmení")
        email   = st.text_input("E-mail klienta")
    with c2:
        mobil    = st.text_input("Mobilní telefon")
        povolani = st.text_input("Povolání / Zaměstnavatel")
    with c3:
        datum_schuzky  = st.date_input("Datum schůzky", value=datetime.now())
        datum_kontaktu = st.date_input("Datum následného kontaktu", value=datetime.now() + timedelta(days=90))
        poradce        = st.text_input("Poradce / Kód", value="Jan Miksa")

    st.divider()
    st.subheader("🎯 Hlavní témata k řešení")
    ct1, ct2, ct3 = st.columns(3)
    with ct1:
        t_vlastni = st.checkbox("Vlastní zajištění (příjem)")
        t_rodina  = st.checkbox("Zajištění rodiny")
        t_deti    = st.checkbox("Zajištění dětí / Start do života")
    with ct2:
        t_bydleni = st.checkbox("Vlastní bydlení / Rekonstrukce")
        t_renta   = st.checkbox("Renta / Budoucí rezerva")
        t_majetek = st.checkbox("Ochrana majetku a auta")
    with ct3:
        t_podnik = st.checkbox("Podnikatelská rizika")
        t_dane   = st.checkbox("Daňové úspory a efektivita")
        t_uvery  = st.checkbox("Optimalizace úvěrů / Dluhů")

    st.divider()
    st.subheader("📋 Analýza portfolia")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Ochrana osob:**")
        r1, r2, r3 = st.columns([2,1,1])
        ziv   = r1.checkbox("Životní pojištění")
        ziv_p = r2.selectbox("Poj.", POJISTOVNY, key="p1")
        ziv_s = r3.selectbox("Stat.", STATUSY, key="s1")
        r1, r2, r3 = st.columns([2,1,1])
        ura   = r1.checkbox("Úraz / Nemoc")
        ura_p = r2.selectbox("Poj.", POJISTOVNY, key="p2")
        ura_s = r3.selectbox("Stat.", STATUSY, key="s2")
        r1, r2, r3 = st.columns([2,1,1])
        inv   = r1.checkbox("Invalidita / Péče")
        inv_p = r2.selectbox("Poj.", POJISTOVNY, key="p3")
        inv_s = r3.selectbox("Stat.", STATUSY, key="s3")
        st.write("**Majetek a Auto:**")
        r1, r2, r3 = st.columns([2,1,1])
        maj   = r1.checkbox("Dům / Byt / Odp.")
        maj_p = r2.selectbox("Poj.", POJISTOVNY, key="p4")
        maj_s = r3.selectbox("Stat.", STATUSY, key="s4")
        r1, r2, r3 = st.columns([2,1,1])
        aut   = r1.checkbox("Auto (POV/HAV)")
        aut_p = r2.selectbox("Poj.", POJISTOVNY, key="p5")
        aut_s = r3.selectbox("Stat.", STATUSY, key="s5")
    with col2:
        st.write("**Finance a Podnikání:**")
        r1, r2, r3 = st.columns([2,1,1])
        ins   = r1.checkbox("Investice / DIP")
        ins_p = r2.selectbox("Inst.", POJISTOVNY, key="p6")
        ins_s = r3.selectbox("Stat.", STATUSY, key="s6")
        r1, r2, r3 = st.columns([2,1,1])
        dps   = r1.checkbox("Penzijko (DPS/PP)")
        dps_p = r2.selectbox("Fond", POJISTOVNY, key="p7")
        dps_s = r3.selectbox("Stat.", STATUSY, key="s7")
        r1, r2, r3 = st.columns([2,1,1])
        pod   = r1.checkbox("Podnikatelské poj.")
        pod_p = r2.selectbox("Poj.", POJISTOVNY, key="p8")
        pod_s = r3.selectbox("Stat.", STATUSY, key="s8")
        prispevek = st.text_input("Příspěvek zaměstnavatele:")
        r1, r2, r3 = st.columns([2,1,1])
        hyp   = r1.checkbox("Hypotéka / Úvěr")
        hyp_p = r2.selectbox("Banka", POJISTOVNY, key="p9")
        hyp_s = r3.selectbox("Stat.", STATUSY, key="s9")

    st.divider()
    st.subheader("🏁 Závěr a další kroky")
    cx1, cx2 = st.columns(2)
    with cx1:
        k_nabidka = st.checkbox("Připravit srovnávací nabídku")
        k_smlouva = st.checkbox("Sjednat/Dopojistit produkty")
    with cx2:
        k_revize = st.checkbox("Prověřit stávající smlouvy (audit)")
        k_servis = st.checkbox("Servisní schůzka / Aktualizace údajů")

    poznamky = st.text_area("Detailní poznámky k řešení...", height=100)
    odeslat  = st.form_submit_button("💾 ULOŽIT KOMPLETNÍ ZÁZNAM")


# ─────────────────────────────────────────────────────────────
#  GENEROVÁNÍ PDF — JEDNOSTRÁNKOVÝ LAYOUT
# ─────────────────────────────────────────────────────────────
def generuj_pdf(data: dict) -> bytes:
    buffer = io.BytesIO()

    # Velmi malé okraje pro maximum prostoru
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=8*mm, rightMargin=8*mm,
        topMargin=8*mm,  bottomMargin=6*mm,
        title="Karta klienta UNIQA",
    )

    styles = getSampleStyleSheet()

    def style(name, parent="Normal", **kw):
        kw.setdefault("fontName", FONT_NORMAL)
        return ParagraphStyle(name, parent=styles[parent], **kw)

    # Kompaktní velikosti fontů
    s_title      = style("TI", fontSize=13, textColor=WHITE,
                         fontName=FONT_BOLD, leading=16, alignment=TA_LEFT)
    s_subtitle   = style("ST", fontSize=7.5, textColor=UNIQA_LIGHT,
                         leading=10, alignment=TA_LEFT)
    s_sec        = style("SC", fontSize=7.5, textColor=WHITE,
                         fontName=FONT_BOLD, leading=10)
    s_label      = style("LB", fontSize=6.5,
                         textColor=colors.HexColor("#888888"), leading=8)
    s_value      = style("VA", fontSize=7.5, textColor=BLACK,
                         fontName=FONT_BOLD, leading=9)
    s_cell_hdr   = style("CH", fontSize=7, textColor=WHITE,
                         fontName=FONT_BOLD, alignment=TA_CENTER, leading=9)
    s_cell       = style("CC", fontSize=7, textColor=BLACK,
                         alignment=TA_CENTER, leading=9)
    s_cell_l     = style("CL", fontSize=7, textColor=BLACK,
                         alignment=TA_LEFT, leading=9)
    s_group      = style("GH", fontSize=7, textColor=UNIQA_BLUE,
                         fontName=FONT_BOLD, leading=9)
    s_notes      = style("NT", fontSize=7, textColor=BLACK,
                         leading=9, leftIndent=3)
    s_footer     = style("FT", fontSize=6, textColor=colors.gray,
                         alignment=TA_CENTER)

    W = A4[0] - 16*mm   # šířka obsahu
    SP = Spacer(1, 2)   # mini mezera — pouze 2pt

    story = []

    # ── ZÁHLAVÍ ──────────────────────────────────────────────
    ts = datetime.now().strftime("%d.%m.%Y %H:%M")
    header_tbl = Table([[
        Paragraph("DIGITÁLNÍ KARTA KLIENTA  —  UNIQA pojišťovna, a.s.", s_title),
        Paragraph(
            f"Poradce: {data['poradce']}<br/>Vygenerováno: {ts}",
            s_subtitle
        ),
    ]], colWidths=[W*0.70, W*0.30])
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), UNIQA_BLUE),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",   (0,0), (0,0),   8),
        ("TOPPADDING",    (0,0), (-1,-1),  5),
        ("BOTTOMPADDING", (0,0), (-1,-1),  5),
        ("ALIGN",         (1,0), (1,0),   "RIGHT"),
        ("RIGHTPADDING",  (1,0), (1,0),    8),
    ]))
    story.append(header_tbl)
    story.append(SP)

    def sec_header(text):
        t = Table([[Paragraph(text, s_sec)]], colWidths=[W])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), UNIQA_BLUE),
            ("TOPPADDING",    (0,0), (-1,-1), 2),
            ("BOTTOMPADDING", (0,0), (-1,-1), 2),
            ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ]))
        return t

    def lv(label, value):
        return [
            Paragraph(label, s_label),
            Paragraph(str(value) if value else "—", s_value),
        ]

    def ano_ne(val):
        text  = "ANO" if val else "NE"
        hex_c = "#1a7a3c" if val else "#b00020"
        return Paragraph(f'<font color="{hex_c}"><b>{text}</b></font>', s_cell)

    STATUS_COLORS = {
        "Mám / OK":    "#1a7a3c",
        "Chci řešit":  "#e65c00",
        "Chci revizi": "#8b0000",
        "Nezájem":     "#888888",
        "-":           "#555555",
    }

    def status_par(s):
        hex_c = STATUS_COLORS.get(s, "#000000")
        return Paragraph(f'<font color="{hex_c}"><b>{s}</b></font>', s_cell)

    TP = 2   # top/bottom padding buněk
    LP = 4   # left padding buněk
    LINE = ("LINEBELOW", (0,0), (-1,-1), 0.25, colors.HexColor("#dddddd"))
    BASE_STYLE = [
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, UNIQA_GRAY]),
        ("TOPPADDING",     (0,0), (-1,-1), TP),
        ("BOTTOMPADDING",  (0,0), (-1,-1), TP),
        ("LEFTPADDING",    (0,0), (-1,-1), LP),
        ("VALIGN",         (0,0), (-1,-1), "MIDDLE"),
        LINE,
    ]

    # ── BLOK A: Osobní údaje + Témata (vedle sebe) ───────────
    # Levá část: osobní údaje
    os_rows = [
        lv("Jméno a příjmení",         data["jmeno"]),
        lv("E-mail",                   data["email"]),
        lv("Mobilní telefon",          data["mobil"]),
        lv("Povolání / Zaměstnavatel", data["povolani"]),
        lv("Datum schůzky",            data["datum_schuzky"].strftime("%d.%m.%Y")),
        lv("Datum nás. kontaktu",      data["datum_kontaktu"].strftime("%d.%m.%Y")),
    ]
    os_tbl = Table(os_rows, colWidths=[W*0.19, W*0.29])
    os_tbl.setStyle(TableStyle(BASE_STYLE))

    # Pravá část: témata (3 sloupce ano/ne)
    temata = [
        ("Vlastní zajištění",   data["t_vlastni"]),
        ("Zajištění rodiny",    data["t_rodina"]),
        ("Zajištění dětí",      data["t_deti"]),
        ("Bydlení / Rekonstr.", data["t_bydleni"]),
        ("Renta / Rezerva",     data["t_renta"]),
        ("Ochrana majetku",     data["t_majetek"]),
        ("Podnik. rizika",      data["t_podnik"]),
        ("Daňové úspory",       data["t_dane"]),
        ("Optim. úvěrů",        data["t_uvery"]),
    ]
    # 3x3 grid
    tem_rows = []
    for i in range(0, 9, 3):
        row = []
        for t, v in temata[i:i+3]:
            row += [Paragraph(t, s_cell_l), ano_ne(v)]
        tem_rows.append(row)

    cw_t = W * 0.52
    col_w = cw_t / 6
    tem_tbl = Table(
        tem_rows,
        colWidths=[col_w*2.1, col_w*0.7, col_w*2.1, col_w*0.7, col_w*2.1, col_w*0.7]
    )
    tem_tbl.setStyle(TableStyle(BASE_STYLE))

    # Sekce A záhlaví — rozdělené do dvou
    sec_os  = Table([[Paragraph("1 |  OSOBNÍ ÚDAJE", s_sec)]], colWidths=[W*0.48])
    sec_os.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), UNIQA_BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ]))
    sec_tem = Table([[Paragraph("2 |  TÉMATA K ŘEŠENÍ", s_sec)]], colWidths=[W*0.52])
    sec_tem.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), UNIQA_BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ]))

    blok_A_header = Table(
        [[sec_os, sec_tem]],
        colWidths=[W*0.48, W*0.52]
    )
    blok_A_header.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))

    blok_A = Table(
        [[os_tbl, tem_tbl]],
        colWidths=[W*0.48, W*0.52]
    )
    blok_A.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 2),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))

    story.append(blok_A_header)
    story.append(blok_A)
    story.append(SP)

    # ── SEKCE 3: Portfolio ───────────────────────────────────
    story.append(sec_header("3 |  ANALÝZA PORTFOLIA"))

    pf_header = [
        Paragraph("Produkt",    s_cell_hdr),
        Paragraph("Zájem",      s_cell_hdr),
        Paragraph("Pojišťovna", s_cell_hdr),
        Paragraph("Status",     s_cell_hdr),
        Paragraph("Produkt",    s_cell_hdr),
        Paragraph("Zájem",      s_cell_hdr),
        Paragraph("Pojišťovna", s_cell_hdr),
        Paragraph("Status",     s_cell_hdr),
    ]

    # Produkty rozdělíme do 2 sloupců po 5 řádcích
    produkty_l = [
        ("── Ochrana osob ──",      None, None, None),
        ("Životní pojištění",       data["ziv"], data["ziv_p"], data["ziv_s"]),
        ("Úraz / Nemoc",            data["ura"], data["ura_p"], data["ura_s"]),
        ("Invalidita / Péče",       data["inv"], data["inv_p"], data["inv_s"]),
        ("── Majetek a Auto ──",    None, None, None),
        ("Dům / Byt / Odpověd.",    data["maj"], data["maj_p"], data["maj_s"]),
    ]
    produkty_r = [
        ("Auto (POV / HAV)",        data["aut"], data["aut_p"], data["aut_s"]),
        ("── Finance / Podnikání ──",None, None, None),
        ("Investice / DIP",         data["ins"], data["ins_p"], data["ins_s"]),
        ("Penzijko (DPS/PP)",       data["dps"], data["dps_p"], data["dps_s"]),
        ("Podnik. pojištění",       data["pod"], data["pod_p"], data["pod_s"]),
        ("Hypotéka / Úvěr",         data["hyp"], data["hyp_p"], data["hyp_s"]),
    ]

    def make_pf_cell(prod, zajem, poj, stat):
        if zajem is None:
            return [Paragraph(prod, s_group), "", "", ""]
        return [
            Paragraph(prod, s_cell_l),
            ano_ne(zajem),
            Paragraph(poj, s_cell),
            status_par(stat),
        ]

    pf_rows = [pf_header]
    for (pl, zl, jl, sl), (pr, zr, jr, sr) in zip(produkty_l, produkty_r):
        left  = make_pf_cell(pl, zl, jl, sl)
        right = make_pf_cell(pr, zr, jr, sr)
        pf_rows.append(left + right)

    cw = W / 8
    pf_tbl = Table(
        pf_rows,
        colWidths=[cw*2.2, cw*0.7, cw*1.1, cw*1.0, cw*2.2, cw*0.7, cw*1.1, cw*1.0]
    )

    pf_style = [
        ("BACKGROUND",    (0,0),  (-1,0),  UNIQA_BLUE),
        ("ROWBACKGROUNDS",(0,1),  (-1,-1), [WHITE, UNIQA_GRAY]),
        ("TOPPADDING",    (0,0),  (-1,-1), TP),
        ("BOTTOMPADDING", (0,0),  (-1,-1), TP),
        ("LEFTPADDING",   (0,0),  (-1,-1), LP),
        ("VALIGN",        (0,0),  (-1,-1), "MIDDLE"),
        LINE,
        # Středová svislá linka oddělující dvě half-tabulky
        ("LINEAFTER",     (3,0),  (3,-1),  0.8, UNIQA_BLUE),
    ]
    # Zvýraznění skupinových řádků v levé části
    for i, (prod, zajem, _, _) in enumerate(produkty_l):
        if zajem is None:
            pf_style += [
                ("SPAN",       (0, i+1), (3, i+1)),
                ("BACKGROUND", (0, i+1), (3, i+1), UNIQA_LIGHT),
            ]
    # Zvýraznění skupinových řádků v pravé části
    for i, (prod, zajem, _, _) in enumerate(produkty_r):
        if zajem is None:
            pf_style += [
                ("SPAN",       (4, i+1), (7, i+1)),
                ("BACKGROUND", (4, i+1), (7, i+1), UNIQA_LIGHT),
            ]

    pf_tbl.setStyle(TableStyle(pf_style))
    story.append(pf_tbl)

    if data["prispevek"]:
        pr_tbl = Table([[
            Paragraph("Příspěvek zaměstnavatele:", s_label),
            Paragraph(data["prispevek"], s_value),
        ]], colWidths=[W*0.30, W*0.70])
        pr_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), UNIQA_GRAY),
            ("TOPPADDING",    (0,0), (-1,-1), 2),
            ("BOTTOMPADDING", (0,0), (-1,-1), 2),
            ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ]))
        story.append(pr_tbl)

    story.append(SP)

    # ── BLOK B: Kroky + Poznámky (vedle sebe) ────────────────
    sec_kroky = Table([[Paragraph("4 |  ZÁVĚR A DALŠÍ KROKY", s_sec)]], colWidths=[W*0.42])
    sec_kroky.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), UNIQA_BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ]))
    sec_pozn = Table([[Paragraph("5 |  POZNÁMKY", s_sec)]], colWidths=[W*0.58])
    sec_pozn.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), UNIQA_BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ]))
    blok_B_header = Table(
        [[sec_kroky, sec_pozn]],
        colWidths=[W*0.42, W*0.58]
    )
    blok_B_header.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))

    kroky = [
        ("Připravit srovnávací nabídku",         data["k_nabidka"]),
        ("Sjednat / Dopojistit produkty",        data["k_smlouva"]),
        ("Prověřit stávající smlouvy (audit)",   data["k_revize"]),
        ("Servisní schůzka / Aktualizace údajů", data["k_servis"]),
    ]
    k_rows = [[Paragraph(t, s_cell_l), ano_ne(v)] for t, v in kroky]
    k_tbl = Table(k_rows, colWidths=[W*0.32, W*0.10])
    k_tbl.setStyle(TableStyle(BASE_STYLE))

    pozn_text = data["poznamky"] if data["poznamky"] else "— bez poznámek —"
    pozn_tbl = Table(
        [[Paragraph(pozn_text.replace("\n", "<br/>"), s_notes)]],
        colWidths=[W*0.58],
        minRowHeights=[28],
    )
    pozn_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), WHITE),
        ("BOX",           (0,0), (-1,-1), 0.5, UNIQA_BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ]))

    blok_B = Table(
        [[k_tbl, pozn_tbl]],
        colWidths=[W*0.42, W*0.58]
    )
    blok_B.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))

    story.append(blok_B_header)
    story.append(blok_B)
    story.append(Spacer(1, 3))

    # ── PATIČKA ──────────────────────────────────────────────
    story.append(HRFlowable(width=W, thickness=0.5, color=UNIQA_BLUE))
    story.append(Spacer(1, 1))
    story.append(Paragraph(
        f"Dokument vygenerován: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}  |  "
        f"Poradce: {data['poradce']}  |  UNIQA pojišťovna, a.s.  |  Důvěrný dokument",
        s_footer
    ))

    doc.build(story)
    return buffer.getvalue()


# ─────────────────────────────────────────────────────────────
#  LOGIKA ULOŽENÍ
# ─────────────────────────────────────────────────────────────
if odeslat:
    if not jmeno:
        st.error("⚠️ Vyplňte jméno klienta!")
    else:
        data = dict(
            jmeno=jmeno, email=email, mobil=mobil, povolani=povolani,
            datum_schuzky=datum_schuzky, datum_kontaktu=datum_kontaktu,
            poradce=poradce,
            t_vlastni=t_vlastni, t_rodina=t_rodina, t_deti=t_deti,
            t_bydleni=t_bydleni, t_renta=t_renta, t_majetek=t_majetek,
            t_podnik=t_podnik, t_dane=t_dane, t_uvery=t_uvery,
            ziv=ziv, ziv_p=ziv_p, ziv_s=ziv_s,
            ura=ura, ura_p=ura_p, ura_s=ura_s,
            inv=inv, inv_p=inv_p, inv_s=inv_s,
            maj=maj, maj_p=maj_p, maj_s=maj_s,
            aut=aut, aut_p=aut_p, aut_s=aut_s,
            ins=ins, ins_p=ins_p, ins_s=ins_s,
            dps=dps, dps_p=dps_p, dps_s=dps_s,
            pod=pod, pod_p=pod_p, pod_s=pod_s,
            prispevek=prispevek,
            hyp=hyp, hyp_p=hyp_p, hyp_s=hyp_s,
            k_nabidka=k_nabidka, k_smlouva=k_smlouva,
            k_revize=k_revize,   k_servis=k_servis,
            poznamky=poznamky,
        )

        with st.spinner("Generuji PDF..."):
            pdf_bytes = generuj_pdf(data)

        soubor_jmeno = f"Karta_{jmeno.replace(' ', '_')}.pdf"
        st.success(f"✅ PDF připraveno: **{soubor_jmeno}**")
        st.download_button(
            label="📥 Stáhnout PDF k tisku",
            data=pdf_bytes,
            file_name=soubor_jmeno,
            mime="application/pdf",
        )
