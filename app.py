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
import io

# --- NASTAVENÍ STRÁNKY ---
st.set_page_config(page_title="Karta klienta UNIQA", layout="wide")

POJISTOVNY = ["-", "UNIQA", "Allianz", "Generali ČP", "Kooperativa", "ČPP", "ČSOB", "Pillow", "Direct", "MetLife", "KB"]
STATUSY    = ["-", "Mám / OK", "Chci řešit", "Chci revizi", "Nezájem"]

UNIQA_BLUE  = colors.HexColor("#003399")
UNIQA_LIGHT = colors.HexColor("#e8edf7")
UNIQA_GRAY  = colors.HexColor("#f5f7f9")
WHITE       = colors.white
BLACK       = colors.black
GREEN       = colors.HexColor("#1a7a3c")
RED         = colors.HexColor("#b00020")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    h1 { color: #003399; }
    h3 { color: #003399; border-bottom: 2px solid #003399; padding-bottom: 5px; margin-top: 20px; }
    .stCheckbox { margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 Digitální Karta Klienta")

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
        r1, r2, r3 = st.columns([2,1,1]); ziv = r1.checkbox("Životní pojištění"); ziv_p = r2.selectbox("Poj.", POJISTOVNY, key="p1"); ziv_s = r3.selectbox("Stat.", STATUSY, key="s1")
        r1, r2, r3 = st.columns([2,1,1]); ura = r1.checkbox("Úraz / Nemoc");      ura_p = r2.selectbox("Poj.", POJISTOVNY, key="p2"); ura_s = r3.selectbox("Stat.", STATUSY, key="s2")
        r1, r2, r3 = st.columns([2,1,1]); inv = r1.checkbox("Invalidita / Péče"); inv_p = r2.selectbox("Poj.", POJISTOVNY, key="p3"); inv_s = r3.selectbox("Stat.", STATUSY, key="s3")
        st.write("**Majetek a Auto:**")
        r1, r2, r3 = st.columns([2,1,1]); maj = r1.checkbox("Dům / Byt / Odp."); maj_p = r2.selectbox("Poj.", POJISTOVNY, key="p4"); maj_s = r3.selectbox("Stat.", STATUSY, key="s4")
        r1, r2, r3 = st.columns([2,1,1]); aut = r1.checkbox("Auto (POV/HAV)");   aut_p = r2.selectbox("Poj.", POJISTOVNY, key="p5"); aut_s = r3.selectbox("Stat.", STATUSY, key="s5")
    with col2:
        st.write("**Finance a Podnikání:**")
        r1, r2, r3 = st.columns([2,1,1]); ins = r1.checkbox("Investice / DIP");     ins_p = r2.selectbox("Inst.", POJISTOVNY, key="p6"); ins_s = r3.selectbox("Stat.", STATUSY, key="s6")
        r1, r2, r3 = st.columns([2,1,1]); dps = r1.checkbox("Penzijko (DPS/PP)");  dps_p = r2.selectbox("Fond", POJISTOVNY, key="p7"); dps_s = r3.selectbox("Stat.", STATUSY, key="s7")
        r1, r2, r3 = st.columns([2,1,1]); pod = r1.checkbox("Podnikatelské poj."); pod_p = r2.selectbox("Poj.", POJISTOVNY, key="p8"); pod_s = r3.selectbox("Stat.", STATUSY, key="s8")
        prispevek = st.text_input("Příspěvek zaměstnavatele:")
        r1, r2, r3 = st.columns([2,1,1]); hyp = r1.checkbox("Hypotéka / Úvěr");    hyp_p = r2.selectbox("Banka", POJISTOVNY, key="p9"); hyp_s = r3.selectbox("Stat.", STATUSY, key="s9")

    st.divider()

    st.subheader("🏁 Závěr a další kroky")
    cx1, cx2 = st.columns(2)
    with cx1:
        k_nabidka = st.checkbox("Připravit srovnávací nabídku")
        k_smlouva = st.checkbox("Sjednat/Dopojistit produkty")
    with cx2:
        k_revize = st.checkbox("Prověřit stávající smlouvy (audit)")
        k_servis = st.checkbox("Servisní schůzka / Aktualizace údajů")

    poznamky = st.text_area("Detailní poznámky k řešení...", height=150)
    odeslat  = st.form_submit_button("💾 ULOŽIT KOMPLETNÍ ZÁZNAM")


# ─────────────────────────────────────────────────────────────
#  POMOCNÁ FUNKCE – generování PDF v paměti
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

    # ── Styly ────────────────────────────────────────────────
    styles = getSampleStyleSheet()

    # ✅ OPRAVA 1: fontName se NEdává napevno, použije se setdefault
    def style(name, parent="Normal", **kw):
        kw.setdefault("fontName", "Helvetica")
        return ParagraphStyle(name, parent=styles[parent], **kw)

    # ✅ OPRAVA 2: Helper pro správný hex formát (#rrggbb) pro ReportLab Paragraph XML
    def to_hex(c):
        return "#%02x%02x%02x" % (int(c.red * 255), int(c.green * 255), int(c.blue * 255))

    s_header_title = style("HT", fontSize=18, textColor=WHITE,
                           alignment=TA_LEFT, leading=22,
                           fontName="Helvetica-Bold")
    s_header_sub   = style("HS", fontSize=10, textColor=UNIQA_LIGHT,
                           alignment=TA_LEFT)
    s_section      = style("SEC", fontSize=11, textColor=WHITE,
                           fontName="Helvetica-Bold", leading=16)
    s_label        = style("LBL", fontSize=8.5, textColor=colors.HexColor("#666666"), leading=11)
    s_value        = style("VAL", fontSize=10, textColor=BLACK,
                           fontName="Helvetica-Bold", leading=13)
    s_cell_hdr     = style("CH",  fontSize=8.5, textColor=WHITE,
                           fontName="Helvetica-Bold", alignment=TA_CENTER)
    s_cell         = style("CC",  fontSize=9,  textColor=BLACK, alignment=TA_CENTER)
    s_cell_l       = style("CCL", fontSize=9,  textColor=BLACK, alignment=TA_LEFT)
    s_notes        = style("NT",  fontSize=9,  textColor=BLACK,
                           leading=13, leftIndent=4)
    s_footer       = style("FT",  fontSize=7.5, textColor=colors.gray,
                           alignment=TA_CENTER)

    W = A4[0] - 30*mm   # použitelná šířka

    story = []

    # ── ZÁHLAVÍ (barevný banner) ──────────────────────────────
    header_data = [[
        Paragraph("DIGITÁLNÍ KARTA KLIENTA", s_header_title),
        Paragraph("Uniqa pojišťovna, a.s.", s_header_sub),
    ]]
    header_tbl = Table(header_data, colWidths=[W*0.65, W*0.35])
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), UNIQA_BLUE),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0), (0,0), 10),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ("ALIGN",        (1,0), (1,0), "RIGHT"),
        ("RIGHTPADDING", (1,0), (1,0), 10),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 6))

    # ── Helper: barevný nadpis sekce ─────────────────────────
    def sec_header(text):
        tbl = Table([[Paragraph(text, s_section)]], colWidths=[W])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), UNIQA_BLUE),
            ("TOPPADDING",   (0,0),(-1,-1), 5),
            ("BOTTOMPADDING",(0,0),(-1,-1), 5),
            ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ]))
        return tbl

    # Helper: dvojice popisek + hodnota
    def lv(label, value):
        return [Paragraph(label, s_label), Paragraph(str(value) if value else "—", s_value)]

    # ✅ OPRAVA 2 aplikována: to_hex() místo color.hexval()
    def ano_ne(val):
        text  = "ANO" if val else "NE"
        hex_c = "#1a7a3c" if val else "#b00020"
        return Paragraph(f'<font color="{hex_c}"><b>{text}</b></font>', s_cell)

    # ── SEKCE 1: Osobní údaje ────────────────────────────────
    story.append(sec_header("  1 |  OSOBNÍ ÚDAJE A SCHŮZKA"))
    story.append(Spacer(1, 4))

    os_data = [
        lv("Jméno a příjmení",         data["jmeno"])    +
        lv("Datum schůzky",            data["datum_schuzky"].strftime("%d.%m.%Y")),
        lv("E-mail",                   data["email"])    +
        lv("Datum nás. kontaktu",      data["datum_kontaktu"].strftime("%d.%m.%Y")),
        lv("Mobilní telefon",          data["mobil"])    +
        lv("Poradce / Kód",            data["poradce"]),
        lv("Povolání / Zaměstnavatel", data["povolani"]) +
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
    story.append(sec_header("  2 |  HLAVNÍ TÉMATA K ŘEŠENÍ"))
    story.append(Spacer(1, 4))

    temata = [
        ("Vlastní zajištění (příjem)",       data["t_vlastni"]),
        ("Zajištění rodiny",                 data["t_rodina"]),
        ("Zajištění dětí / Start do života", data["t_deti"]),
        ("Vlastní bydlení / Rekonstrukce",   data["t_bydleni"]),
        ("Renta / Budoucí rezerva",          data["t_renta"]),
        ("Ochrana majetku a auta",           data["t_majetek"]),
        ("Podnikatelská rizika",             data["t_podnik"]),
        ("Daňové úspory a efektivita",       data["t_dane"]),
        ("Optimalizace úvěrů / Dluhů",       data["t_uvery"]),
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

    # ── SEKCE 3: Analýza portfolia ───────────────────────────
    story.append(sec_header("  3 |  ANALÝZA PORTFOLIA"))
    story.append(Spacer(1, 4))

    def portfolio_header():
        return [
            Paragraph("Produkt",    s_cell_hdr),
            Paragraph("Zájem",      s_cell_hdr),
            Paragraph("Pojišťovna", s_cell_hdr),
            Paragraph("Status",     s_cell_hdr),
        ]

    # ✅ OPRAVA 2 aplikována: přímé hex stringy místo color.hexval()
    STATUS_COLORS = {
        "Mám / OK":    "#1a7a3c",
        "Chci řešit":  "#e65c00",
        "Chci revizi": "#8b0000",
        "Nezájem":     "#888888",
        "-":           "#000000",
    }

    def status_par(s):
        hex_c = STATUS_COLORS.get(s, "#000000")
        return Paragraph(f'<font color="{hex_c}"><b>{s}</b></font>', s_cell)

    produkty = [
        ("── Ochrana osob ──",         None, None, None),
        ("Životní pojištění",          data["ziv"], data["ziv_p"], data["ziv_s"]),
        ("Úraz / Nemoc",               data["ura"], data["ura_p"], data["ura_s"]),
        ("Invalidita / Péče",          data["inv"], data["inv_p"], data["inv_s"]),
        ("── Majetek a Auto ──",        None, None, None),
        ("Dům / Byt / Odpovědnost",    data["maj"], data["maj_p"], data["maj_s"]),
        ("Auto (POV / HAV)",           data["aut"], data["aut_p"], data["aut_s"]),
        ("── Finance a Podnikání ──",   None, None, None),
        ("Investice / DIP",            data["ins"], data["ins_p"], data["ins_s"]),
        ("Penzijko (DPS/PP)",          data["dps"], data["dps_p"], data["dps_s"]),
        ("Podnikatelské pojištění",    data["pod"], data["pod_p"], data["pod_s"]),
        ("Hypotéka / Úvěr",           data["hyp"], data["hyp_p"], data["hyp_s"]),
    ]

    pf_rows    = [portfolio_header()]
    group_rows = []

    for i, (prod, zajem, poj, stat) in enumerate(produkty):
        row_idx = i + 1
        if zajem is None:
            group_rows.append(row_idx)
            pf_rows.append([
                Paragraph(prod, ParagraphStyle(
                    "GH", parent=styles["Normal"],
                    fontName="Helvetica-Bold", fontSize=9,
                    textColor=UNIQA_BLUE)),
                "", "", "",
            ])
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
            Paragraph("Příspěvek zaměstnavatele:", s_label),
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
    story.append(sec_header("  4 |  ZÁVĚR A DALŠÍ KROKY"))
    story.append(Spacer(1, 4))

    kroky = [
        ("Připravit srovnávací nabídku",         data["k_nabidka"]),
        ("Sjednat / Dopojistit produkty",        data["k_smlouva"]),
        ("Prověřit stávající smlouvy (audit)",   data["k_revize"]),
        ("Servisní schůzka / Aktualizace údajů", data["k_servis"]),
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
    story.append(sec_header("  5 |  DETAILNÍ POZNÁMKY"))
    story.append(Spacer(1, 4))

    pozn_text = data["poznamky"] if data["poznamky"] else "— bez poznámek —"
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
        f"Dokument vygenerován: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}  |  "
        f"Poradce: {data['poradce']}  |  UNIQA pojišťovna, a.s."
    )
    story.append(Paragraph(footer_text, s_footer))

    doc.build(story)
    return buffer.getvalue()


# ─────────────────────────────────────────────────────────────
#  LOGIKA ULOŽENÍ
# ─────────────────────────────────────────────────────────────
if odeslat:
    if not jmeno:
        st.error("Chyba: Vyplňte jméno klienta!")
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
