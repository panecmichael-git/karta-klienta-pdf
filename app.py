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
import urllib.request
import os
import io

# ─────────────────────────────────────────────────────────────
#  REGISTRACE UNICODE FONTU (DejaVu Sans)
# ─────────────────────────────────────────────────────────────
FONT_DIR   = "/tmp/fonts"
FONT_URLS  = {
    "DejaVuSans":       "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf",
    "DejaVuSans-Bold":  "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans-Bold.ttf",
}

os.makedirs(FONT_DIR, exist_ok=True)

for font_name, url in FONT_URLS.items():
    path = os.path.join(FONT_DIR, f"{font_name}.ttf")
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)
    try:
        pdfmetrics.registerFont(TTFont(font_name, path))
    except Exception:
        pass  # uz zaregistrovan

FONT_NORMAL = "DejaVuSans"
FONT_BOLD   = "DejaVuSans-Bold"

# --- NASTAVENÍ STRÁNKY ---
st.set_page_config(page_title="Karta klienta UNIQA", layout="wide")

POJISTOVNY = ["-", "UNIQA", "Allianz", "Generali CP", "Kooperativa", "CPP", "CSOB", "Pillow", "Direct", "MetLife", "KB"]
STATUSY    = ["-", "Mam / OK", "Chci resit", "Chci revizi", "Nezajem"]

UNIQA_BLUE  = colors.HexColor("#003399")
UNIQA_LIGHT = colors.HexColor("#e8edf7")
UNIQA_GRAY  = colors.HexColor("#f5f7f9")
WHITE       = colors.white
BLACK       = colors.black

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    h1 { color: #003399; }
    h3 { color: #003399; border-bottom: 2px solid #003399; padding-bottom: 5px; margin-top: 20px; }
    .stCheckbox { margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Digitalni Karta Klienta UNIQA")

with st.form("hlavni_formular"):
    st.subheader("Osobni udaje a Plan")
    c1, c2, c3 = st.columns(3)
    with c1:
        jmeno   = st.text_input("Jmeno a prijmeni")
        email   = st.text_input("E-mail klienta")
    with c2:
        mobil    = st.text_input("Mobilni telefon")
        povolani = st.text_input("Povolani / Zamestnavatel")
    with c3:
        datum_schuzky  = st.date_input("Datum schuzky", value=datetime.now())
        datum_kontaktu = st.date_input("Datum nasledneho kontaktu", value=datetime.now() + timedelta(days=90))
        poradce        = st.text_input("Poradce / Kod", value="Jan Miksa")

    st.divider()

    st.subheader("Hlavni temata k reseni")
    ct1, ct2, ct3 = st.columns(3)
    with ct1:
        t_vlastni = st.checkbox("Vlastni zajisteni (prijem)")
        t_rodina  = st.checkbox("Zajisteni rodiny")
        t_deti    = st.checkbox("Zajisteni deti / Start do zivota")
    with ct2:
        t_bydleni = st.checkbox("Vlastni bydleni / Rekonstrukce")
        t_renta   = st.checkbox("Renta / Budouci rezerva")
        t_majetek = st.checkbox("Ochrana majetku a auta")
    with ct3:
        t_podnik = st.checkbox("Podnikatelska rizika")
        t_dane   = st.checkbox("Danove uspory a efektivita")
        t_uvery  = st.checkbox("Optimalizace uveru / Dluhu")

    st.divider()

    st.subheader("Analyza portfolia")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Ochrana osob:**")
        r1, r2, r3 = st.columns([2,1,1]); ziv = r1.checkbox("Zivotni pojisteni"); ziv_p = r2.selectbox("Poj.", POJISTOVNY, key="p1"); ziv_s = r3.selectbox("Stat.", STATUSY, key="s1")
        r1, r2, r3 = st.columns([2,1,1]); ura = r1.checkbox("Uraz / Nemoc");      ura_p = r2.selectbox("Poj.", POJISTOVNY, key="p2"); ura_s = r3.selectbox("Stat.", STATUSY, key="s2")
        r1, r2, r3 = st.columns([2,1,1]); inv = r1.checkbox("Invalidita / Pece"); inv_p = r2.selectbox("Poj.", POJISTOVNY, key="p3"); inv_s = r3.selectbox("Stat.", STATUSY, key="s3")
        st.write("**Majetek a Auto:**")
        r1, r2, r3 = st.columns([2,1,1]); maj = r1.checkbox("Dum / Byt / Odp."); maj_p = r2.selectbox("Poj.", POJISTOVNY, key="p4"); maj_s = r3.selectbox("Stat.", STATUSY, key="s4")
        r1, r2, r3 = st.columns([2,1,1]); aut = r1.checkbox("Auto (POV/HAV)");   aut_p = r2.selectbox("Poj.", POJISTOVNY, key="p5"); aut_s = r3.selectbox("Stat.", STATUSY, key="s5")
    with col2:
        st.write("**Finance a Podnikani:**")
        r1, r2, r3 = st.columns([2,1,1]); ins = r1.checkbox("Investice / DIP");     ins_p = r2.selectbox("Inst.", POJISTOVNY, key="p6"); ins_s = r3.selectbox("Stat.", STATUSY, key="s6")
        r1, r2, r3 = st.columns([2,1,1]); dps = r1.checkbox("Penzijko (DPS/PP)");  dps_p = r2.selectbox("Fond", POJISTOVNY, key="p7"); dps_s = r3.selectbox("Stat.", STATUSY, key="s7")
        r1, r2, r3 = st.columns([2,1,1]); pod = r1.checkbox("Podnikatelske poj."); pod_p = r2.selectbox("Poj.", POJISTOVNY, key="p8"); pod_s = r3.selectbox("Stat.", STATUSY, key="s8")
        prispevek = st.text_input("Prispevek zamestnavatele:")
        r1, r2, r3 = st.columns([2,1,1]); hyp = r1.checkbox("Hypoteka / Uver");    hyp_p = r2.selectbox("Banka", POJISTOVNY, key="p9"); hyp_s = r3.selectbox("Stat.", STATUSY, key="s9")

    st.divider()

    st.subheader("Zaver a dalsi kroky")
    cx1, cx2 = st.columns(2)
    with cx1:
        k_nabidka = st.checkbox("Pripravit srovnavaci nabidku")
        k_smlouva = st.checkbox("Sjednat/Dopojistit produkty")
    with cx2:
        k_revize = st.checkbox("Proverit stavajici smlouvy (audit)")
        k_servis = st.checkbox("Servisni schuzka / Aktualizace udaju")

    poznamky = st.text_area("Detailni poznamky k reseni...", height=150)
    odeslat  = st.form_submit_button("ULOZIT KOMPLETNI ZAZNAM")


# ─────────────────────────────────────────────────────────────
#  GENEROVÁNÍ PDF
# ─────────────────────────────────────────────────────────────
def generuj_pdf(data: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm,
        topMargin=15*mm,  bottomMargin=15*mm,
        title="Karta klienta UNIQA",
    )

    styles = getSampleStyleSheet()

    # ✅ Všechny styly používají DejaVuSans (Unicode font)
    def style(name, parent="Normal", **kw):
        kw.setdefault("fontName", FONT_NORMAL)
        return ParagraphStyle(name, parent=styles[parent], **kw)

    s_header_title = style("HT", fontSize=18, textColor=WHITE,
                           alignment=TA_LEFT, leading=22,
                           fontName=FONT_BOLD)
    s_header_sub   = style("HS", fontSize=10, textColor=UNIQA_LIGHT,
                           alignment=TA_LEFT)
    s_section      = style("SEC", fontSize=11, textColor=WHITE,
                           fontName=FONT_BOLD, leading=16)
    s_label        = style("LBL", fontSize=8.5,
                           textColor=colors.HexColor("#666666"), leading=11)
    s_value        = style("VAL", fontSize=10, textColor=BLACK,
                           fontName=FONT_BOLD, leading=13)
    s_cell_hdr     = style("CH",  fontSize=8.5, textColor=WHITE,
                           fontName=FONT_BOLD, alignment=TA_CENTER)
    s_cell         = style("CC",  fontSize=9,  textColor=BLACK,
                           alignment=TA_CENTER)
    s_cell_l       = style("CCL", fontSize=9,  textColor=BLACK,
                           alignment=TA_LEFT)
    s_notes        = style("NT",  fontSize=9,  textColor=BLACK,
                           leading=13, leftIndent=4)
    s_footer       = style("FT",  fontSize=7.5, textColor=colors.gray,
                           alignment=TA_CENTER)
    s_group        = style("GH",  fontSize=9,  textColor=UNIQA_BLUE,
                           fontName=FONT_BOLD)

    W = A4[0] - 30*mm

    story = []

    # ── ZÁHLAVÍ ──────────────────────────────────────────────
    header_data = [[
        Paragraph("DIGITALNI KARTA KLIENTA", s_header_title),
        Paragraph("Uniqa pojistovna, a.s.", s_header_sub),
    ]]
    header_tbl = Table(header_data, colWidths=[W*0.65, W*0.35])
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), UNIQA_BLUE),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0), (0,0),  10),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ("ALIGN",        (1,0), (1,0),  "RIGHT"),
        ("RIGHTPADDING", (1,0), (1,0),  10),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 6))

    def sec_header(text):
        tbl = Table([[Paragraph(text, s_section)]], colWidths=[W])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), UNIQA_BLUE),
            ("TOPPADDING",   (0,0),(-1,-1), 5),
            ("BOTTOMPADDING",(0,0),(-1,-1), 5),
            ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ]))
        return tbl

    def lv(label, value):
        return [
            Paragraph(label, s_label),
            Paragraph(str(value) if value else "-", s_value),
        ]

    def ano_ne(val):
        text  = "ANO" if val else "NE"
        hex_c = "#1a7a3c" if val else "#b00020"
        return Paragraph(f'<font color="{hex_c}"><b>{text}</b></font>', s_cell)

    STATUS_COLORS = {
        "Mam / OK":    "#1a7a3c",
        "Chci resit":  "#e65c00",
        "Chci revizi": "#8b0000",
        "Nezajem":     "#888888",
        "-":           "#000000",
    }

    def status_par(s):
        hex_c = STATUS_COLORS.get(s, "#000000")
        return Paragraph(f'<font color="{hex_c}"><b>{s}</b></font>', s_cell)

    # ── SEKCE 1: Osobní údaje ────────────────────────────────
    story.append(sec_header("  1 |  OSOBNI UDAJE A SCHUZKA"))
    story.append(Spacer(1, 4))

    os_data = [
        lv("Jmeno a prijmeni",          data["jmeno"])    +
        lv("Datum schuzky",             data["datum_schuzky"].strftime("%d.%m.%Y")),
        lv("E-mail",                    data["email"])    +
        lv("Datum nas. kontaktu",       data["datum_kontaktu"].strftime("%d.%m.%Y")),
        lv("Mobilni telefon",           data["mobil"])    +
        lv("Poradce / Kod",             data["poradce"]),
        lv("Povolani / Zamestnavatel",  data["povolani"]) +
        ["", ""],
    ]
    os_tbl = Table(os_data, colWidths=[W*0.18, W*0.32, W*0.18, W*0.32])
    os_tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [WHITE, UNIQA_GRAY]),
        ("TOPPADDING",   (0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("LINEBELOW",    (0,0),(-1,-1), 0.3, colors.HexColor("#cccccc")),
    ]))
    story.append(os_tbl)
    story.append(Spacer(1, 8))

    # ── SEKCE 2: Témata ──────────────────────────────────────
    story.append(sec_header("  2 |  HLAVNI TEMATA K RESENI"))
    story.append(Spacer(1, 4))

    temata = [
        ("Vlastni zajisteni (prijem)",       data["t_vlastni"]),
        ("Zajisteni rodiny",                 data["t_rodina"]),
        ("Zajisteni deti / Start do zivota", data["t_deti"]),
        ("Vlastni bydleni / Rekonstrukce",   data["t_bydleni"]),
        ("Renta / Budouci rezerva",          data["t_renta"]),
        ("Ochrana majetku a auta",           data["t_majetek"]),
        ("Podnikatelska rizika",             data["t_podnik"]),
        ("Danove uspory a efektivita",       data["t_dane"]),
        ("Optimalizace uveru / Dluhu",       data["t_uvery"]),
    ]
    rows = []
    for i in range(0, len(temata), 3):
        row = []
        for t, v in temata[i:i+3]:
            row += [Paragraph(t, s_cell_l), ano_ne(v)]
        while len(row) < 6:
            row += ["", ""]
        rows.append(row)

    tem_tbl = Table(rows, colWidths=[W*0.26, W*0.07, W*0.26, W*0.07, W*0.26, W*0.07])
    tem_tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [WHITE, UNIQA_GRAY]),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING",  (0,0),(-1,-1), 6),
        ("LINEBELOW",    (0,0),(-1,-1), 0.3, colors.HexColor("#cccccc")),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(tem_tbl)
    story.append(Spacer(1, 8))

    # ── SEKCE 3: Portfolio ───────────────────────────────────
    story.append(sec_header("  3 |  ANALYZA PORTFOLIA"))
    story.append(Spacer(1, 4))

    def portfolio_header():
        return [
            Paragraph("Produkt",    s_cell_hdr),
            Paragraph("Zajem",      s_cell_hdr),
            Paragraph("Pojistovna", s_cell_hdr),
            Paragraph("Status",     s_cell_hdr),
        ]

    produkty = [
        ("-- Ochrana osob --",         None, None, None),
        ("Zivotni pojisteni",          data["ziv"], data["ziv_p"], data["ziv_s"]),
        ("Uraz / Nemoc",               data["ura"], data["ura_p"], data["ura_s"]),
        ("Invalidita / Pece",          data["inv"], data["inv_p"], data["inv_s"]),
        ("-- Majetek a Auto --",        None, None, None),
        ("Dum / Byt / Odpovednost",    data["maj"], data["maj_p"], data["maj_s"]),
        ("Auto (POV / HAV)",           data["aut"], data["aut_p"], data["aut_s"]),
        ("-- Finance a Podnikani --",   None, None, None),
        ("Investice / DIP",            data["ins"], data["ins_p"], data["ins_s"]),
        ("Penzijko (DPS/PP)",          data["dps"], data["dps_p"], data["dps_s"]),
        ("Podnikatelske pojisteni",    data["pod"], data["pod_p"], data["pod_s"]),
        ("Hypoteka / Uver",            data["hyp"], data["hyp_p"], data["hyp_s"]),
    ]

    pf_rows    = [portfolio_header()]
    group_rows = []

    for i, (prod, zajem, poj, stat) in enumerate(produkty):
        row_idx = i + 1
        if zajem is None:
            group_rows.append(row_idx)
            pf_rows.append([Paragraph(prod, s_group), "", "", ""])
        else:
            pf_rows.append([
                Paragraph(prod, s_cell_l),
                ano_ne(zajem),
                Paragraph(poj, s_cell),
                status_par(stat),
            ])

    pf_tbl = Table(pf_rows, colWidths=[W*0.42, W*0.13, W*0.22, W*0.23])
    style_cmds = [
        ("BACKGROUND",    (0,0), (-1,0), UNIQA_BLUE),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, UNIQA_GRAY]),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("LINEBELOW",     (0,0), (-1,-1), 0.3, colors.HexColor("#cccccc")),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("SPAN",          (0, group_rows[0]), (-1, group_rows[0])),
        ("SPAN",          (0, group_rows[1]), (-1, group_rows[1])),
        ("SPAN",          (0, group_rows[2]), (-1, group_rows[2])),
        ("BACKGROUND",    (0, group_rows[0]), (-1, group_rows[0]), UNIQA_LIGHT),
        ("BACKGROUND",    (0, group_rows[1]), (-1, group_rows[1]), UNIQA_LIGHT),
        ("BACKGROUND",    (0, group_rows[2]), (-1, group_rows[2]), UNIQA_LIGHT),
    ]
    pf_tbl.setStyle(TableStyle(style_cmds))
    story.append(pf_tbl)

    if data["prispevek"]:
        story.append(Spacer(1, 3))
        tbl = Table([[
            Paragraph("Prispevek zamestnavatele:", s_label),
            Paragraph(data["prispevek"], s_value),
        ]], colWidths=[W*0.35, W*0.65])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), UNIQA_GRAY),
            ("TOPPADDING",    (0,0),(-1,-1), 4),
            ("BOTTOMPADDING", (0,0),(-1,-1), 4),
            ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ]))
        story.append(tbl)

    story.append(Spacer(1, 8))

    # ── SEKCE 4: Další kroky ─────────────────────────────────
    story.append(sec_header("  4 |  ZAVER A DALSI KROKY"))
    story.append(Spacer(1, 4))

    kroky = [
        ("Pripravit srovnavaci nabidku",         data["k_nabidka"]),
        ("Sjednat / Dopojistit produkty",        data["k_smlouva"]),
        ("Proverit stavajici smlouvy (audit)",   data["k_revize"]),
        ("Servisni schuzka / Aktualizace udaju", data["k_servis"]),
    ]
    k_rows = [[Paragraph(t, s_cell_l), ano_ne(v)] for t, v in kroky]
    k_tbl = Table(k_rows, colWidths=[W*0.82, W*0.18])
    k_tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [WHITE, UNIQA_GRAY]),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("LINEBELOW",    (0,0),(-1,-1), 0.3, colors.HexColor("#cccccc")),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(k_tbl)
    story.append(Spacer(1, 8))

    # ── SEKCE 5: Poznámky ────────────────────────────────────
    story.append(sec_header("  5 |  DETAILNI POZNAMKY"))
    story.append(Spacer(1, 4))

    pozn_text = data["poznamky"] if data["poznamky"] else "- bez poznamek -"
    pozn_tbl = Table(
        [[Paragraph(pozn_text.replace("\n", "<br/>"), s_notes)]],
        colWidths=[W],
        minRowHeights=[40],
    )
    pozn_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), WHITE),
        ("BOX",           (0,0),(-1,-1), 0.5, UNIQA_BLUE),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
    ]))
    story.append(pozn_tbl)
    story.append(Spacer(1, 10))

    # ── PATIČKA ──────────────────────────────────────────────
    story.append(HRFlowable(width=W, thickness=1, color=UNIQA_BLUE))
    story.append(Spacer(1, 3))
    footer_text = (
        f"Dokument vygenerovan: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}  |  "
        f"Poradce: {data['poradce']}  |  UNIQA pojistovna, a.s."
    )
    story.append(Paragraph(footer_text, s_footer))

    doc.build(story)
    return buffer.getvalue()


# ─────────────────────────────────────────────────────────────
#  LOGIKA ULOŽENÍ
# ─────────────────────────────────────────────────────────────
if odeslat:
    if not jmeno:
        st.error("Chyba: Vyplnte jmeno klienta!")
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
        st.success(f"PDF pripraveno: **{soubor_jmeno}**")
        st.download_button(
            label="Stahnout PDF k tisku",
            data=pdf_bytes,
            file_name=soubor_jmeno,
            mime="application/pdf",
        )
