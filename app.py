import streamlit as st
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import io

# ─────────────────────────────────────────────────────────────
#  FONT
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

font_r = find_font(FONT_SEARCH_PATHS)
font_b = find_font(FONT_BOLD_SEARCH_PATHS)

if font_r and font_b:
    pdfmetrics.registerFont(TTFont("F",  font_r))
    pdfmetrics.registerFont(TTFont("FB", font_b))
    FN  = "F"
    FNB = "FB"
else:
    import urllib.request, tempfile
    FONT_DIR = tempfile.gettempdir()
    NOTO = {
        "F":  "https://fonts.gstatic.com/s/notosans/v36/o-0IIpQlx3QUlC5A4PNb4j5Ba_2c7A.ttf",
        "FB": "https://fonts.gstatic.com/s/notosans/v36/o-0NIpQlx3QUlC5A4PNjXhFVadyB1Wk.ttf",
    }
    for name, url in NOTO.items():
        path = os.path.join(FONT_DIR, f"{name}.ttf")
        if not os.path.exists(path):
            urllib.request.urlretrieve(url, path)
        pdfmetrics.registerFont(TTFont(name, path))
    FN  = "F"
    FNB = "FB"

# ─────────────────────────────────────────────────────────────
#  BARVY
# ─────────────────────────────────────────────────────────────
BLUE  = colors.HexColor("#003399")
LBLUE = colors.HexColor("#dde4f5")
GRAY  = colors.HexColor("#f4f5f7")
WHITE = colors.white
BLACK = colors.black
DGRAY = colors.HexColor("#888888")
GREEN = colors.HexColor("#1a7a3c")
RED   = colors.HexColor("#b00020")

# ─────────────────────────────────────────────────────────────
#  STREAMLIT UI
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Karta klienta UNIQA", layout="wide")

POJISTOVNY = ["-", "UNIQA", "Allianz", "Generali ČP", "Kooperativa",
              "ČPP", "ČSOB", "Pillow", "Direct", "MetLife", "KB"]
STATUSY    = ["-", "Mám / OK", "Chci řešit", "Chci revizi", "Nezájem"]

st.markdown("""
<style>
.main { background-color: #f4f5f7; }
h1 { color: #003399; }
</style>
""", unsafe_allow_html=True)

st.title("📄 Digitální Karta Klienta UNIQA")

with st.form("form"):

    st.subheader("👤 Osobní údaje")
    c1, c2, c3 = st.columns(3)
    with c1:
        jmeno   = st.text_input("Jméno a příjmení")
        email   = st.text_input("E-mail")
    with c2:
        mobil    = st.text_input("Mobilní telefon")
        povolani = st.text_input("Povolání / Zaměstnavatel")
    with c3:
        datum_schuzky  = st.date_input("Datum schůzky",          value=datetime.now())
        datum_kontaktu = st.date_input("Datum nás. kontaktu",     value=datetime.now() + timedelta(days=90))
        poradce        = st.text_input("Poradce / Kód",           value="Jan Miksa")

    st.divider()
    st.subheader("🎯 Témata k řešení")
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
        r1,r2,r3 = st.columns([2,1,1])
        ziv   = r1.checkbox("Životní pojištění")
        ziv_p = r2.selectbox("Poj.", POJISTOVNY, key="p1")
        ziv_s = r3.selectbox("Stat.", STATUSY, key="s1")
        r1,r2,r3 = st.columns([2,1,1])
        ura   = r1.checkbox("Úraz / Nemoc")
        ura_p = r2.selectbox("Poj.", POJISTOVNY, key="p2")
        ura_s = r3.selectbox("Stat.", STATUSY, key="s2")
        r1,r2,r3 = st.columns([2,1,1])
        inv   = r1.checkbox("Invalidita / Péče")
        inv_p = r2.selectbox("Poj.", POJISTOVNY, key="p3")
        inv_s = r3.selectbox("Stat.", STATUSY, key="s3")
        st.write("**Majetek a Auto:**")
        r1,r2,r3 = st.columns([2,1,1])
        maj   = r1.checkbox("Dům / Byt / Odp.")
        maj_p = r2.selectbox("Poj.", POJISTOVNY, key="p4")
        maj_s = r3.selectbox("Stat.", STATUSY, key="s4")
        r1,r2,r3 = st.columns([2,1,1])
        aut   = r1.checkbox("Auto (POV/HAV)")
        aut_p = r2.selectbox("Poj.", POJISTOVNY, key="p5")
        aut_s = r3.selectbox("Stat.", STATUSY, key="s5")
    with col2:
        st.write("**Finance a Podnikání:**")
        r1,r2,r3 = st.columns([2,1,1])
        ins   = r1.checkbox("Investice / DIP")
        ins_p = r2.selectbox("Inst.", POJISTOVNY, key="p6")
        ins_s = r3.selectbox("Stat.", STATUSY, key="s6")
        r1,r2,r3 = st.columns([2,1,1])
        dps   = r1.checkbox("Penzijko (DPS/PP)")
        dps_p = r2.selectbox("Fond", POJISTOVNY, key="p7")
        dps_s = r3.selectbox("Stat.", STATUSY, key="s7")
        r1,r2,r3 = st.columns([2,1,1])
        pod   = r1.checkbox("Podnikatelské poj.")
        pod_p = r2.selectbox("Poj.", POJISTOVNY, key="p8")
        pod_s = r3.selectbox("Stat.", STATUSY, key="s8")
        prispevek = st.text_input("Příspěvek zaměstnavatele:")
        r1,r2,r3 = st.columns([2,1,1])
        hyp   = r1.checkbox("Hypotéka / Úvěr")
        hyp_p = r2.selectbox("Banka", POJISTOVNY, key="p9")
        hyp_s = r3.selectbox("Stat.", STATUSY, key="s9")

    st.divider()
    st.subheader("🏁 Závěr a další kroky")
    cx1, cx2 = st.columns(2)
    with cx1:
        k_nabidka = st.checkbox("Připravit srovnávací nabídku")
        k_smlouva = st.checkbox("Sjednat / Dopojistit produkty")
    with cx2:
        k_revize = st.checkbox("Prověřit stávající smlouvy (audit)")
        k_servis = st.checkbox("Servisní schůzka / Aktualizace údajů")

    poznamky = st.text_area("Detailní poznámky...", height=100)
    odeslat  = st.form_submit_button("💾 ULOŽIT A GENEROVAT PDF")


# ─────────────────────────────────────────────────────────────
#  GENEROVÁNÍ PDF
# ─────────────────────────────────────────────────────────────
def generuj_pdf(d: dict) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=10*mm, rightMargin=10*mm,
        topMargin=8*mm,   bottomMargin=6*mm,
    )

    gs = getSampleStyleSheet()

    def S(name, **kw):
        kw.setdefault("fontName", FN)
        kw.setdefault("fontSize", 8)
        kw.setdefault("leading",  10)
        return ParagraphStyle(name, parent=gs["Normal"], **kw)

    # Styly
    sTitle  = S("ti", fontSize=14, fontName=FNB, textColor=WHITE, leading=18)
    sSub    = S("su", fontSize=7,  textColor=LBLUE, leading=9)
    sSec    = S("sc", fontSize=7.5,fontName=FNB, textColor=WHITE, leading=9)
    sLbl    = S("lb", fontSize=6.5,textColor=DGRAY, leading=8)
    sVal    = S("va", fontSize=8,  fontName=FNB, textColor=BLACK, leading=10)
    sHdr    = S("hd", fontSize=7,  fontName=FNB, textColor=WHITE, leading=9, alignment=TA_CENTER)
    sCell   = S("cc", fontSize=7.5,textColor=BLACK, leading=9, alignment=TA_CENTER)
    sCellL  = S("cl", fontSize=7.5,textColor=BLACK, leading=9, alignment=TA_LEFT)
    sGroup  = S("gr", fontSize=7,  fontName=FNB, textColor=BLUE, leading=9)
    sNote   = S("nt", fontSize=7.5,textColor=BLACK, leading=10)
    sFooter = S("ft", fontSize=6,  textColor=DGRAY, alignment=TA_CENTER)

    W  = A4[0] - 20*mm
    sp = lambda n=3: Spacer(1, n)

    story = []

    # ── pomocné funkce ────────────────────────────────────────
    def sec_bar(text, width=None):
        w = width or W
        t = Table([[Paragraph(text, sSec)]], colWidths=[w])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), BLUE),
            ("TOPPADDING",    (0,0),(-1,-1), 3),
            ("BOTTOMPADDING", (0,0),(-1,-1), 3),
            ("LEFTPADDING",   (0,0),(-1,-1), 6),
            ("RIGHTPADDING",  (0,0),(-1,-1), 6),
        ]))
        return t

    def base_style(extra=None):
        s = [
            ("ROWBACKGROUNDS", (0,0),(-1,-1), [WHITE, GRAY]),
            ("TOPPADDING",     (0,0),(-1,-1), 2),
            ("BOTTOMPADDING",  (0,0),(-1,-1), 2),
            ("LEFTPADDING",    (0,0),(-1,-1), 5),
            ("RIGHTPADDING",   (0,0),(-1,-1), 5),
            ("VALIGN",         (0,0),(-1,-1), "MIDDLE"),
            ("LINEBELOW",      (0,0),(-1,-1), 0.25, colors.HexColor("#cccccc")),
        ]
        if extra:
            s += extra
        return s

    def chip(val):
        if val:
            return Paragraph('<font color="#1a7a3c"><b>✔ ANO</b></font>', sCell)
        return Paragraph('<font color="#b00020"><b>✘ NE</b></font>', sCell)

    STATUS_COLOR = {
        "Mám / OK":    "#1a7a3c",
        "Chci řešit":  "#d45f00",
        "Chci revizi": "#8b0000",
        "Nezájem":     "#888888",
        "-":           "#aaaaaa",
    }
    def stat_p(s):
        c = STATUS_COLOR.get(s, "#555555")
        return Paragraph(f'<font color="{c}"><b>{s}</b></font>', sCell)

    # ─────────────────────────────────────────────────────────
    #  ZÁHLAVÍ
    # ─────────────────────────────────────────────────────────
    ts = datetime.now().strftime("%d.%m.%Y  %H:%M")
    hdr = Table([
        [
            Paragraph("DIGITÁLNÍ KARTA KLIENTA", sTitle),
            Paragraph(f"UNIQA pojišťovna, a.s.<br/>Poradce: <b>{d['poradce']}</b>  |  {ts}", sSub),
        ]
    ], colWidths=[W*0.62, W*0.38])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), BLUE),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",   (0,0),(0,0),   10),
        ("TOPPADDING",    (0,0),(-1,-1),  7),
        ("BOTTOMPADDING", (0,0),(-1,-1),  7),
        ("ALIGN",         (1,0),(1,0),   "RIGHT"),
        ("RIGHTPADDING",  (1,0),(1,0),    10),
    ]))
    story.append(hdr)
    story.append(sp(4))

    # ─────────────────────────────────────────────────────────
    #  SEKCE 1 — OSOBNÍ ÚDAJE
    # ─────────────────────────────────────────────────────────
    story.append(sec_bar("1  |  OSOBNÍ ÚDAJE A SCHŮZKA"))

    # 4 sloupce: label | hodnota | label | hodnota
    cw = [W*0.16, W*0.34, W*0.16, W*0.34]
    os_rows = [
        [Paragraph("Jméno a příjmení", sLbl),
         Paragraph(d["jmeno"] or "—",  sVal),
         Paragraph("Datum schůzky",    sLbl),
         Paragraph(d["datum_schuzky"].strftime("%d.%m.%Y"), sVal)],

        [Paragraph("E-mail",           sLbl),
         Paragraph(d["email"] or "—",  sVal),
         Paragraph("Datum nás. kontaktu", sLbl),
         Paragraph(d["datum_kontaktu"].strftime("%d.%m.%Y"), sVal)],

        [Paragraph("Mobilní telefon",  sLbl),
         Paragraph(d["mobil"] or "—",  sVal),
         Paragraph("Poradce / Kód",    sLbl),
         Paragraph(d["poradce"] or "—",sVal)],

        [Paragraph("Povolání / Zaměstnavatel", sLbl),
         Paragraph(d["povolani"] or "—", sVal),
         Paragraph("", sLbl),
         Paragraph("", sVal)],
    ]
    os_tbl = Table(os_rows, colWidths=cw)
    os_tbl.setStyle(TableStyle(base_style()))
    story.append(os_tbl)
    story.append(sp())

    # ─────────────────────────────────────────────────────────
    #  SEKCE 2 — TÉMATA
    # ─────────────────────────────────────────────────────────
    story.append(sec_bar("2  |  HLAVNÍ TÉMATA K ŘEŠENÍ"))

    temata = [
        ("Vlastní zajištění (příjem)",        d["t_vlastni"]),
        ("Zajištění rodiny",                  d["t_rodina"]),
        ("Zajištění dětí / Start do života",  d["t_deti"]),
        ("Vlastní bydlení / Rekonstrukce",    d["t_bydleni"]),
        ("Renta / Budoucí rezerva",           d["t_renta"]),
        ("Ochrana majetku a auta",            d["t_majetek"]),
        ("Podnikatelská rizika",              d["t_podnik"]),
        ("Daňové úspory a efektivita",        d["t_dane"]),
        ("Optimalizace úvěrů / Dluhů",        d["t_uvery"]),
    ]

    # 3 skupiny po 3 — každá skupina: název | chip | mezera
    # Layout: [nazev][chip][medzera][nazev][chip][medzera][nazev][chip]
    col_n = W * 0.28
    col_c = W * 0.05
    col_g = W * 0.01
    t_rows = []
    for i in range(0, 9, 3):
        row = []
        for j in range(3):
            txt, val = temata[i+j]
            row.append(Paragraph(txt, sCellL))
            row.append(chip(val))
            if j < 2:
                row.append(Paragraph("", sCell))  # mezera
        t_rows.append(row)

    tem_tbl = Table(
        t_rows,
        colWidths=[col_n, col_c, col_g, col_n, col_c, col_g, col_n, col_c]
    )
    tem_tbl.setStyle(TableStyle(base_style()))
    story.append(tem_tbl)
    story.append(sp())

    # ─────────────────────────────────────────────────────────
    #  SEKCE 3 — PORTFOLIO
    # ─────────────────────────────────────────────────────────
    story.append(sec_bar("3  |  ANALÝZA PORTFOLIA"))

    # Šířky sloupců portfolia
    pf_cw = [W*0.30, W*0.09, W*0.16, W*0.20,   # levá polovina
              W*0.005,                            # oddělovač
              W*0.30, W*0.09, W*0.16, W*0.145]  # pravá polovina (zbytek)

    def pf_hdr_row():
        h = Paragraph
        empty = Paragraph("", sHdr)
        return [
            h("Produkt",    sHdr), h("Zájem", sHdr), h("Pojišťovna", sHdr), h("Status", sHdr),
            empty,
            h("Produkt",    sHdr), h("Zájem", sHdr), h("Pojišťovna", sHdr), h("Status", sHdr),
        ]

    def pf_row(prod, zajem, poj, stat, is_group=False):
        if is_group:
            return [Paragraph(prod, sGroup), "", "", "", "", "", "", "", ""]
        return [
            Paragraph(prod, sCellL), chip(zajem),
            Paragraph(poj,  sCell),  stat_p(stat),
            Paragraph("",   sCell),
            Paragraph("",   sCellL), Paragraph("", sCell),
            Paragraph("",   sCell),  Paragraph("", sCell),
        ]

    def pf_row2(prodL, zajem_l, pojL, statL,
                prodR, zajem_r, pojR, statR):
        return [
            Paragraph(prodL, sCellL), chip(zajem_l),
            Paragraph(pojL,  sCell),  stat_p(statL),
            Paragraph("|",   sFooter),
            Paragraph(prodR, sCellL), chip(zajem_r),
            Paragraph(pojR,  sCell),  stat_p(statR),
        ]

    def pf_group_row(text_l, text_r=""):
        tl = Paragraph(text_l, sGroup) if text_l else Paragraph("", sGroup)
        tr = Paragraph(text_r, sGroup) if text_r else Paragraph("", sGroup)
        return [tl, "", "", "", "", tr, "", "", ""]

    pf_rows = [pf_hdr_row()]

    # Skupina 1 záhlaví + Skupina 2 záhlaví vedle sebe
    pf_rows.append(pf_group_row("── Ochrana osob ──", "── Majetek a Auto ──"))
    pf_rows.append(pf_row2("Životní pojištění",   d["ziv"], d["ziv_p"], d["ziv_s"],
                            "Dům / Byt / Odpovědnost", d["maj"], d["maj_p"], d["maj_s"]))
    pf_rows.append(pf_row2("Úraz / Nemoc",        d["ura"], d["ura_p"], d["ura_s"],
                            "Auto (POV / HAV)",    d["aut"], d["aut_p"], d["aut_s"]))
    pf_rows.append(pf_row2("Invalidita / Péče",   d["inv"], d["inv_p"], d["inv_s"],
                            "", False, "-", "-"))

    pf_rows.append(pf_group_row("── Finance a Podnikání ──", ""))
    pf_rows.append(pf_row2("Investice / DIP",      d["ins"], d["ins_p"], d["ins_s"],
                            "Penzijko (DPS/PP)",   d["dps"], d["dps_p"], d["dps_s"]))
    pf_rows.append(pf_row2("Podnik. pojištění",    d["pod"], d["pod_p"], d["pod_s"],
                            "Hypotéka / Úvěr",     d["hyp"], d["hyp_p"], d["hyp_s"]))

    # Styly portfolia
    pf_style = [
        ("BACKGROUND",    (0,0),(-1,0),  BLUE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, GRAY]),
        ("TOPPADDING",    (0,0),(-1,-1), 2),
        ("BOTTOMPADDING", (0,0),(-1,-1), 2),
        ("LEFTPADDING",   (0,0),(-1,-1), 4),
        ("RIGHTPADDING",  (0,0),(-1,-1), 4),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("LINEBELOW",     (0,0),(-1,-1), 0.25, colors.HexColor("#cccccc")),
        # Oddělovač středu
        ("TEXTCOLOR",     (4,0),(4,-1),  colors.HexColor("#aaaaaa")),
        ("ALIGN",         (4,0),(4,-1),  "CENTER"),
        # Zvýraznění skupin
        ("BACKGROUND",    (0,1),(3,1),   LBLUE),
        ("BACKGROUND",    (5,1),(8,1),   LBLUE),
        ("BACKGROUND",    (0,5),(8,5),   LBLUE),
        ("SPAN",          (0,1),(3,1)),
        ("SPAN",          (5,1),(8,1)),
        ("SPAN",          (0,5),(8,5)),
        # Prázdný řádek col 5-8 v group řádku 1
        ("SPAN",          (0,4),(3,4)),  # prázdná bunka invalidita pravá
    ]

    pf_tbl = Table(pf_rows, colWidths=pf_cw)
    pf_tbl.setStyle(TableStyle(pf_style))
    story.append(pf_tbl)

    if d["prispevek"]:
        pr = Table([[
            Paragraph("Příspěvek zaměstnavatele:", sLbl),
            Paragraph(d["prispevek"], sVal),
        ]], colWidths=[W*0.28, W*0.72])
        pr.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), GRAY),
            ("TOPPADDING",    (0,0),(-1,-1), 2),
            ("BOTTOMPADDING", (0,0),(-1,-1), 2),
            ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ]))
        story.append(pr)

    story.append(sp())

    # ─────────────────────────────────────────────────────────
    #  SEKCE 4 — KROKY
    # ─────────────────────────────────────────────────────────
    story.append(sec_bar("4  |  ZÁVĚR A DALŠÍ KROKY"))

    kroky = [
        ("Připravit srovnávací nabídku",         d["k_nabidka"]),
        ("Sjednat / Dopojistit produkty",        d["k_smlouva"]),
        ("Prověřit stávající smlouvy (audit)",   d["k_revize"]),
        ("Servisní schůzka / Aktualizace údajů", d["k_servis"]),
    ]
    # 2 x 2 layout kroků
    k_rows = []
    for i in range(0, 4, 2):
        t1, v1 = kroky[i]
        t2, v2 = kroky[i+1]
        k_rows.append([
            Paragraph(t1, sCellL), chip(v1),
            Paragraph("", sCell),
            Paragraph(t2, sCellL), chip(v2),
        ])

    k_tbl = Table(k_rows, colWidths=[W*0.38, W*0.08, W*0.04, W*0.38, W*0.12])
    k_tbl.setStyle(TableStyle(base_style()))
    story.append(k_tbl)
    story.append(sp())

    # ─────────────────────────────────────────────────────────
    #  SEKCE 5 — POZNÁMKY
    # ─────────────────────────────────────────────────────────
    story.append(sec_bar("5  |  DETAILNÍ POZNÁMKY"))

    pozn_text = d["poznamky"].replace("\n", "<br/>") if d["poznamky"] else "— bez poznámek —"
    pozn = Table(
        [[Paragraph(pozn_text, sNote)]],
        colWidths=[W],
        minRowHeights=[32],
    )
    pozn.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), WHITE),
        ("BOX",           (0,0),(-1,-1), 0.5, BLUE),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 7),
    ]))
    story.append(pozn)
    story.append(sp(4))

    # ─────────────────────────────────────────────────────────
    #  PATIČKA
    # ─────────────────────────────────────────────────────────
    story.append(HRFlowable(width=W, thickness=0.5, color=BLUE))
    story.append(sp(2))
    story.append(Paragraph(
        f"Vygenerováno: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}  |  "
        f"Poradce: {d['poradce']}  |  UNIQA pojišťovna, a.s.  |  Důvěrný dokument",
        sFooter
    ))

    doc.build(story)
    return buf.getvalue()


# ─────────────────────────────────────────────────────────────
#  ODESLÁNÍ
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

        fname = f"Karta_{jmeno.replace(' ', '_')}.pdf"
        st.success(f"✅ PDF připraveno: **{fname}**")
        st.download_button(
            label="📥 Stáhnout PDF k tisku",
            data=pdf_bytes,
            file_name=fname,
            mime="application/pdf",
        )
