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

# ─────────────────────────────────────────────────────────────
#  STREAMLIT UI
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Karta klienta", layout="wide")

POJISTOVNY = ["-", "UNIQA", "Allianz", "Generali ČP", "Kooperativa",
              "ČPP", "ČSOB", "Pillow", "Direct", "MetLife", "KB"]
STATUSY    = ["-", "Mám / OK", "Chci řešit", "Chci revizi", "Nezájem"]

st.markdown("""
<style>
.main { background-color: #f4f5f7; }
h1 { color: #003399; }
</style>
""", unsafe_allow_html=True)

st.title("📄 Digitální Karta Klienta")

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
        datum_schuzky  = st.date_input("Datum schůzky",      value=datetime.now())
        datum_kontaktu = st.date_input("Datum nás. kontaktu", value=datetime.now() + timedelta(days=90))
        poradce        = st.text_input("Poradce / Kód",       value="Jan Miksa")

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
        ziv_s = r3.selectbox("Stat.", STATUSY,   key="s1")
        r1,r2,r3 = st.columns([2,1,1])
        ura   = r1.checkbox("Úraz / Nemoc")
        ura_p = r2.selectbox("Poj.", POJISTOVNY, key="p2")
        ura_s = r3.selectbox("Stat.", STATUSY,   key="s2")
        r1,r2,r3 = st.columns([2,1,1])
        inv   = r1.checkbox("Invalidita / Péče")
        inv_p = r2.selectbox("Poj.", POJISTOVNY, key="p3")
        inv_s = r3.selectbox("Stat.", STATUSY,   key="s3")
        st.write("**Majetek a Auto:**")
        r1,r2,r3 = st.columns([2,1,1])
        maj   = r1.checkbox("Dům / Byt / Odp.")
        maj_p = r2.selectbox("Poj.", POJISTOVNY, key="p4")
        maj_s = r3.selectbox("Stat.", STATUSY,   key="s4")
        r1,r2,r3 = st.columns([2,1,1])
        aut   = r1.checkbox("Auto (POV/HAV)")
        aut_p = r2.selectbox("Poj.", POJISTOVNY, key="p5")
        aut_s = r3.selectbox("Stat.", STATUSY,   key="s5")
    with col2:
        st.write("**Finance a Podnikání:**")
        r1,r2,r3 = st.columns([2,1,1])
        ins   = r1.checkbox("Investice / DIP")
        ins_p = r2.selectbox("Inst.", POJISTOVNY, key="p6")
        ins_s = r3.selectbox("Stat.", STATUSY,    key="s6")
        r1,r2,r3 = st.columns([2,1,1])
        dps   = r1.checkbox("Penzijko (DPS/PP)")
        dps_p = r2.selectbox("Fond",  POJISTOVNY, key="p7")
        dps_s = r3.selectbox("Stat.", STATUSY,    key="s7")
        r1,r2,r3 = st.columns([2,1,1])
        pod   = r1.checkbox("Podnikatelské poj.")
        pod_p = r2.selectbox("Poj.", POJISTOVNY, key="p8")
        pod_s = r3.selectbox("Stat.", STATUSY,   key="s8")
        prispevek = st.text_input("Příspěvek zaměstnavatele:")
        r1,r2,r3 = st.columns([2,1,1])
        hyp   = r1.checkbox("Hypotéka / Úvěr")
        hyp_p = r2.selectbox("Banka", POJISTOVNY, key="p9")
        hyp_s = r3.selectbox("Stat.", STATUSY,    key="s9")

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
#  PDF
# ─────────────────────────────────────────────────────────────
def generuj_pdf(d: dict) -> bytes:
    buf = io.BytesIO()

    # A4 = 595.27 x 841.89 pt
    # Okraje 10mm každá strana → W = 595.27 - 20mm = 595.27 - 56.69 ≈ 538.58 pt
    LEFT = RIGHT = 10 * mm
    TOP  = 8  * mm
    BOT  = 6  * mm

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=LEFT, rightMargin=RIGHT,
        topMargin=TOP,   bottomMargin=BOT,
    )

    gs  = getSampleStyleSheet()
    W   = A4[0] - LEFT - RIGHT   # přesná šířka obsahu v bodech

    # ── styly ────────────────────────────────────────────────
    def S(name, **kw):
        kw.setdefault("fontName", FN)
        kw.setdefault("fontSize", 8)
        kw.setdefault("leading",  10)
        kw.setdefault("wordWrap", "CJK")
        return ParagraphStyle(name, parent=gs["Normal"], **kw)

    sTitle  = S("ti", fontSize=13, fontName=FNB, textColor=WHITE,
                leading=16, alignment=TA_LEFT)
    sSub    = S("su", fontSize=7,  textColor=LBLUE, leading=9,
                alignment=TA_RIGHT)
    sSec    = S("sc", fontSize=7.5, fontName=FNB, textColor=WHITE, leading=9)
    sLbl    = S("lb", fontSize=6.5, textColor=DGRAY, leading=8)
    sVal    = S("va", fontSize=8,   fontName=FNB, textColor=BLACK, leading=10)
    sHdr    = S("hd", fontSize=7,   fontName=FNB, textColor=WHITE, leading=9,
                alignment=TA_CENTER)
    sCell   = S("cc", fontSize=7.5, textColor=BLACK, leading=9,
                alignment=TA_CENTER)
    sCellL  = S("cl", fontSize=7.5, textColor=BLACK, leading=9,
                alignment=TA_LEFT)
    # MENŠÍ font pro témata, aby se text vešel na jeden řádek
    sCellTema = S("ct", fontSize=6.8, textColor=BLACK, leading=8,
                  alignment=TA_LEFT)
    sGroup  = S("gr", fontSize=7,   fontName=FNB, textColor=BLUE, leading=9)
    sNote   = S("nt", fontSize=7.5, textColor=BLACK, leading=10)
    sFooter = S("ft", fontSize=6,   textColor=DGRAY, alignment=TA_CENTER)

    # ── pomocné ───────────────────────────────────────────────
    sp = lambda n=3: Spacer(1, n)

    # Padding pro buňky — MUSÍ být malý, aby colWidths nevyšly záporně
    PAD = 3   # pt

    def base_ts(extra=None):
        """Základní TableStyle — bez negat. šířky."""
        s = [
            ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, GRAY]),
            ("TOPPADDING",     (0,0), (-1,-1), PAD),
            ("BOTTOMPADDING",  (0,0), (-1,-1), PAD),
            ("LEFTPADDING",    (0,0), (-1,-1), PAD),
            ("RIGHTPADDING",   (0,0), (-1,-1), PAD),
            ("VALIGN",         (0,0), (-1,-1), "MIDDLE"),
            ("LINEBELOW",      (0,0), (-1,-1), 0.25,
             colors.HexColor("#cccccc")),
        ]
        if extra:
            s += extra
        return s

    def sec_bar(txt):
        t = Table([[Paragraph(txt, sSec)]], colWidths=[W])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), BLUE),
            ("TOPPADDING",    (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ("LEFTPADDING",   (0,0), (-1,-1), 6),
            ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ]))
        return t

    def chip(val):
        if val:
            return Paragraph(
                '<font color="#1a7a3c"><b>ANO</b></font>', sCell)
        return Paragraph(
            '<font color="#b00020"><b>NE</b></font>', sCell)

    STATUS_COL = {
        "Mám / OK":    "#1a7a3c",
        "Chci řešit":  "#d45f00",
        "Chci revizi": "#8b0000",
        "Nezájem":     "#888888",
        "-":           "#aaaaaa",
    }
    def stat_p(s):
        c = STATUS_COL.get(s, "#555555")
        return Paragraph(
            f'<font color="{c}"><b>{s}</b></font>', sCell)

    story = []

    # ════════════════════════════════════════════════════════
    #  ZÁHLAVÍ
    # ════════════════════════════════════════════════════════
    ts = datetime.now().strftime("%d.%m.%Y  %H:%M")

    # Přesné colWidths = W
    hdr = Table([[
        Paragraph("DIGITÁLNÍ KARTA KLIENTA", sTitle),
        Paragraph(
            f"Poradce: <b>{d['poradce']}</b>  |  {ts}",
            sSub),
    ]], colWidths=[W * 0.60, W * 0.40])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), BLUE),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (0, 0),  10),
        ("LEFTPADDING",   (1,0), (1, 0),  PAD),
        ("RIGHTPADDING",  (0,0), (-1,-1), PAD),
    ]))
    story.append(hdr)
    story.append(sp(4))

    # ════════════════════════════════════════════════════════
    #  SEC 1 — OSOBNÍ ÚDAJE
    # ════════════════════════════════════════════════════════
    story.append(sec_bar("1  |  OSOBNÍ ÚDAJE A SCHŮZKA"))

    C_LBL = W * 0.18   # label
    C_VAL = W * 0.32   # hodnota
    cw_os = [C_LBL, C_VAL, C_LBL, C_VAL]

    os_rows = [
        [Paragraph("Jméno a příjmení",    sLbl),
         Paragraph(d["jmeno"] or "—",     sVal),
         Paragraph("Datum schůzky",       sLbl),
         Paragraph(d["datum_schuzky"].strftime("%d.%m.%Y"), sVal)],

        [Paragraph("E-mail",              sLbl),
         Paragraph(d["email"] or "—",     sVal),
         Paragraph("Datum nás. kontaktu", sLbl),
         Paragraph(d["datum_kontaktu"].strftime("%d.%m.%Y"), sVal)],

        [Paragraph("Mobilní telefon",     sLbl),
         Paragraph(d["mobil"] or "—",     sVal),
         Paragraph("Poradce / Kód",       sLbl),
         Paragraph(d["poradce"] or "—",   sVal)],

        [Paragraph("Povolání",            sLbl),
         Paragraph(d["povolani"] or "—",  sVal),
         Paragraph("", sLbl),
         Paragraph("", sVal)],
    ]
    os_tbl = Table(os_rows, colWidths=cw_os)
    os_tbl.setStyle(TableStyle(base_ts()))
    story.append(os_tbl)
    story.append(sp(3))

    # ════════════════════════════════════════════════════════
    #  SEC 2 — TÉMATA
    #  Rozšířené sloupce pro názvy + menší font, aby se vešel
    #  celý text ("Vlastní bydlení / Rekonstrukce", "Start do
    #  života", "Daňové úspory a efektivita", "Optimalizace
    #  úvěrů / Dluhů").
    # ════════════════════════════════════════════════════════
    story.append(sec_bar("2  |  HLAVNÍ TÉMATA K ŘEŠENÍ"))

    # Širší sloupec pro text, užší pro chip
    C_TEM  = W * 0.295
    C_CHIP = W * 0.038
    C_CHIP_LAST = W - 3 * C_TEM - 2 * C_CHIP
    cw_tem = [C_TEM, C_CHIP, C_TEM, C_CHIP, C_TEM, C_CHIP_LAST]

    temata = [
        ("Vlastní zajištění (příjem)",          d["t_vlastni"]),
        ("Zajištění rodiny",                    d["t_rodina"]),
        ("Zajištění dětí / Start do života",    d["t_deti"]),
        ("Vlastní bydlení / Rekonstrukce",      d["t_bydleni"]),
        ("Renta / Budoucí rezerva",             d["t_renta"]),
        ("Ochrana majetku a auta",              d["t_majetek"]),
        ("Podnikatelská rizika",                d["t_podnik"]),
        ("Daňové úspory a efektivita",          d["t_dane"]),
        ("Optimalizace úvěrů / Dluhů",          d["t_uvery"]),
    ]
    t_rows = []
    for i in range(0, 9, 3):
        row = []
        for txt, val in temata[i:i+3]:
            row.append(Paragraph(txt, sCellTema))
            row.append(chip(val))
        t_rows.append(row)

    tem_tbl = Table(t_rows, colWidths=cw_tem)
    tem_tbl.setStyle(TableStyle(base_ts()))
    story.append(tem_tbl)
    story.append(sp(3))

    # ════════════════════════════════════════════════════════
    #  SEC 3 — PORTFOLIO
    # ════════════════════════════════════════════════════════
    story.append(sec_bar("3  |  ANALÝZA PORTFOLIA"))

    A = W * 0.220   # produkt
    B = W * 0.068   # zájem
    C = W * 0.116   # pojišťovna
    D = W * 0.096   # status
    cw_pf = [A, B, C, D, A, B, C, D]

    def pf_hdr():
        h = lambda t: Paragraph(t, sHdr)
        return [h("Produkt"), h("Zájem"), h("Pojišťovna"), h("Status"),
                h("Produkt"), h("Zájem"), h("Pojišťovna"), h("Status")]

    def pf_group(left_txt, right_txt):
        l = Paragraph(left_txt,  sGroup) if left_txt  else Paragraph("", sGroup)
        r = Paragraph(right_txt, sGroup) if right_txt else Paragraph("", sGroup)
        return [l, "", "", "", r, "", "", ""]

    def pf_data(pL, zL, jL, sL, pR, zR, jR, sR):
        def side(prod, zajem, poj, stat):
            if prod == "":
                return [Paragraph("", sCellL), Paragraph("", sCell),
                        Paragraph("", sCell),  Paragraph("", sCell)]
            return [Paragraph(prod, sCellL), chip(zajem),
                    Paragraph(poj,  sCell),  stat_p(stat)]
        return side(pL, zL, jL, sL) + side(pR, zR, jR, sR)

    pf_rows = [
        pf_hdr(),
        pf_group("── Ochrana osob ──",     "── Majetek a Auto ──"),
        pf_data("Životní pojištění",  d["ziv"], d["ziv_p"], d["ziv_s"],
                "Dům / Byt / Odp.",  d["maj"], d["maj_p"], d["maj_s"]),
        pf_data("Úraz / Nemoc",       d["ura"], d["ura_p"], d["ura_s"],
                "Auto (POV / HAV)",  d["aut"], d["aut_p"], d["aut_s"]),
        pf_data("Invalidita / Péče",  d["inv"], d["inv_p"], d["inv_s"],
                "",                  False,    "-",         "-"),
        pf_group("── Finance a Podnikání ──", ""),
        pf_data("Investice / DIP",    d["ins"], d["ins_p"], d["ins_s"],
                "Penzijko (DPS/PP)", d["dps"], d["dps_p"], d["dps_s"]),
        pf_data("Podnik. pojištění",  d["pod"], d["pod_p"], d["pod_s"],
                "Hypotéka / Úvěr",  d["hyp"], d["hyp_p"], d["hyp_s"]),
    ]

    pf_style = [
        ("BACKGROUND",    (0,0), (-1,0),  BLUE),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, GRAY]),
        ("TOPPADDING",    (0,0), (-1,-1), PAD),
        ("BOTTOMPADDING", (0,0), (-1,-1), PAD),
        ("LEFTPADDING",   (0,0), (-1,-1), PAD),
        ("RIGHTPADDING",  (0,0), (-1,-1), PAD),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("LINEBELOW",     (0,0), (-1,-1), 0.25, colors.HexColor("#cccccc")),
        ("LINEAFTER",     (3,0), (3,-1),  0.8,  BLUE),
        ("SPAN",       (0,1), (3,1)),
        ("SPAN",       (4,1), (7,1)),
        ("BACKGROUND", (0,1), (3,1), LBLUE),
        ("BACKGROUND", (4,1), (7,1), LBLUE),
        ("SPAN",       (0,5), (7,5)),
        ("BACKGROUND", (0,5), (7,5), LBLUE),
    ]
    pf_tbl = Table(pf_rows, colWidths=cw_pf)
    pf_tbl.setStyle(TableStyle(pf_style))
    story.append(pf_tbl)

    if d["prispevek"]:
        pr_cw = [W * 0.30, W * 0.70]
        pr = Table([[
            Paragraph("Příspěvek zaměstnavatele:", sLbl),
            Paragraph(d["prispevek"], sVal),
        ]], colWidths=pr_cw)
        pr.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), GRAY),
            ("TOPPADDING",    (0,0), (-1,-1), PAD),
            ("BOTTOMPADDING", (0,0), (-1,-1), PAD),
            ("LEFTPADDING",   (0,0), (-1,-1), PAD),
            ("RIGHTPADDING",  (0,0), (-1,-1), PAD),
        ]))
        story.append(pr)

    story.append(sp(3))

    # ════════════════════════════════════════════════════════
    #  SEC 4 — ZÁVĚR A KROKY
    # ════════════════════════════════════════════════════════
    story.append(sec_bar("4  |  ZÁVĚR A DALŠÍ KROKY"))

    cw_k = [W*0.39, W*0.07, W*0.04, W*0.39, W*0.11]
    kroky = [
        ("Připravit srovnávací nabídku",         d["k_nabidka"]),
        ("Sjednat / Dopojistit produkty",        d["k_smlouva"]),
        ("Prověřit stávající smlouvy (audit)",   d["k_revize"]),
        ("Servisní schůzka / Aktualizace údajů", d["k_servis"]),
    ]
    k_rows = []
    for i in range(0, 4, 2):
        t1, v1 = kroky[i]
        t2, v2 = kroky[i+1]
        k_rows.append([
            Paragraph(t1, sCellL), chip(v1),
            Paragraph("",  sCell),
            Paragraph(t2, sCellL), chip(v2),
        ])
    k_tbl = Table(k_rows, colWidths=cw_k)
    k_tbl.setStyle(TableStyle(base_ts()))
    story.append(k_tbl)
    story.append(sp(3))

    # ════════════════════════════════════════════════════════
    #  SEC 5 — POZNÁMKY
    # ════════════════════════════════════════════════════════
    story.append(sec_bar("5  |  DETAILNÍ POZNÁMKY"))

    pozn_text = (d["poznamky"].replace("\n", "<br/>")
                 if d["poznamky"] else "— bez poznámek —")
    pozn = Table(
        [[Paragraph(pozn_text, sNote)]],
        colWidths=[W],
        minRowHeights=[30],
    )
    pozn.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), WHITE),
        ("BOX",           (0,0), (-1,-1), 0.5, BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
    ]))
    story.append(pozn)
    story.append(sp(5))

    # ════════════════════════════════════════════════════════
    #  PATIČKA
    # ════════════════════════════════════════════════════════
    story.append(HRFlowable(width=W, thickness=0.5, color=BLUE))
    story.append(sp(2))
    story.append(Paragraph(
        f"Vygenerováno: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}  |  "
        f"Poradce: {d['poradce']}  |  Důvěrný dokument",
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
            t_vlastni=t_vlastni, t_rodina=t_rodina,  t_deti=t_deti,
            t_bydleni=t_bydleni, t_renta=t_renta,    t_majetek=t_majetek,
            t_podnik=t_podnik,   t_dane=t_dane,       t_uvery=t_uvery,
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
