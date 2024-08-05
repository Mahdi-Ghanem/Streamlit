import streamlit as st
import pandas as pd
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO

# Beispiel-Daten für zwei Geschäfte
data_andere = {
    "Produkt": [
        "Brokkoli 2,5kg", "Gouda (15kg)", "Hamburgerbrötchen 55g", "Hamburgerbrötchen 80g", "Hollandaise Sauce", 
        "Joghurt Griechisch", "Mehl", "Mozzarella", "Pommes 10 mm", "Pommes 7 mm", "Pommes salz", "Potato wedges 2.5 kg", 
        "PUTEN 500g", "Salami Geschnitten 500G", "Snack Dressing", "Spinat 2,5KG",
        "Ayran 20x250ml", "CocaCola Dosen","CocaCola Glas", "Cola ZERO Dosen", "Cola ZERO Glas",
        "Fanta EXOTIK Dosen","Fanta EXOTIK Glas", "MEZZO MIX Dosen","MEZZO MIX Glas", "Spreit Dosen", "Spreit Glas",
        "Uludag Dosen","Uludag Glas", "WASSER 0,5 L",
        "Alufolie 150m", "B3 Deckel 100 st", "B3 Salatschale Weiß 100 st", "CC375 BOX PP375 ML 50St",
        "CC50 Sossenbecher", "CC80 Sossenbecher", "Deckel 500 ST", "Döner Beutel 16×16", "Döner Box GROSS", 
        "Döner Box KLEIN", "Gabel Plastik", "Hamburgerbox Klein 100st", "HP3 WARMHALTEVERPACKUNG 125st",
        "Menubox Ungeteilt Beige 100st", "Papp Schalen GROß", "Papp Schalen KLEIN", "Pragsmentpapier 1/4",
        "Pergamentpapier 1/16", "Pizza Box 26", "Pizza Box 30", "Servietten", "Trinkbecher 100 st"
    ]
}

data_meledi = {
    "Produkt": [
        "Geschälte Tomaten", "Artischockenherzen In Wasser 425ml", "Maïskörner", "Kichererbsen Dose", 
        "Rapsöl", "Salat Mayonnaise", "Hartweizengrieß", "Griechischer Joghurt", "Hollandia", 
        "Geraspelter Mozzarella", "Weißkäse", "Thunfisch", "Sambal Oelek", "Geröstete Auberginen Püree", 
        "Frittieröl Halbflüssig 10L", "Meeresfrüchte", "Tafelessig", "Lammkeule Ohne Knochen", "Pfefferkörner"
    ]
}

# Daten für beide Geschäfte in DataFrames umwandeln
df_meledy = pd.DataFrame(data_meledy)
df_andere = pd.DataFrame(data_andere)

# Kategorien definieren
def kategorien_definieren(df, geschaeft):
    if geschaeft == "Meledi":
        lebensmittel = df
        getraenke = pd.DataFrame(columns=["Produkt"])
        verpackung = pd.DataFrame(columns=["Produkt"])
    else:
        lebensmittel = df.iloc[0:16]
        getraenke = df.iloc[16:30]
        verpackung = df.iloc[30:]
    return lebensmittel, getraenke, verpackung

lebensmittel_meledi, getraenke_meledi, verpackung_meledi = kategorien_definieren(df_meledi, "Meledi")
lebensmittel_andere, getraenke_andere, verpackung_andere = kategorien_definieren(df_andere, "Andere")

# CSS-Styling
def apply_styles():
    st.markdown("""
    <style>
    .product-name {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .category-box {
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    .lebensmittel {
        background-color: #ffeeee;  /* Sehr leichtes Rot */
    }
    .getraenke {
        background-color: #e6f7ff;  /* Sehr leichtes Blau */
    }
    .verpackung {
        background-color: #f0fff0;  /* Sehr leichtes Grün */
    }
    .stNumberInput input {
        padding: 5px;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# Start der Streamlit-App
st.title("🍔🍟 Einkaufsliste")

# Geschäftsauswahl
geschaefte = ["Meledy", "Andere"]
geschaeft = st.selectbox("Wähle ein Geschäft aus", geschaefte)

# Daten basierend auf der Geschäftsauswahl setzen
if geschaeft == "Meledy":
    lebensmittel, getraenke, verpackung = lebensmittel_meledy, getraenke_meledy, verpackung_meledy
else:
    lebensmittel, getraenke, verpackung = lebensmittel_andere, getraenke_andere, verpackung_andere

# Platz, um die Anzahl der Produkte einzugeben
st.header("Produkte")
anzahlen = {}

# Lebensmittel-Kategorie
st.markdown('<div class="category-box lebensmittel">', unsafe_allow_html=True)
st.subheader("Lebensmittel")
for index, row in lebensmittel.iterrows():
    product = row['Produkt']
    st.markdown(f"<div class='product-name'>{product}</div>", unsafe_allow_html=True)
    anzahl = st.number_input("", min_value=0, step=1, key=f"{geschaeft}_lebensmittel_{index}")
    anzahlen[product] = anzahl
st.markdown('</div>', unsafe_allow_html=True)

# Getränke-Kategorie
st.markdown('<div class="category-box getraenke">', unsafe_allow_html=True)
st.subheader("Getränke")
for index, row in getraenke.iterrows():
    product = row['Produkt']
    st.markdown(f"<div class='product-name'>{product}</div>", unsafe_allow_html=True)
    anzahl = st.number_input("", min_value=0, step=1, key=f"{geschaeft}_getraenke_{index}")
    anzahlen[product] = anzahl
st.markdown('</div>', unsafe_allow_html=True)

# Verpackung und Sonstiges-Kategorie
st.markdown('<div class="category-box verpackung">', unsafe_allow_html=True)
st.subheader("Verpackung und Sonstiges")
for index, row in verpackung.iterrows():
    product = row['Produkt']
    st.markdown(f"<div class='product-name'>{product}</div>", unsafe_allow_html=True)
    anzahl = st.number_input("", min_value=0, step=1, key=f"{geschaeft}_verpackung_{index}")
    anzahlen[product] = anzahl
st.markdown('</div>', unsafe_allow_html=True)

# OK-Button
if st.button("OK"):
    # Filtern der ausgewählten Produkte
    selected_products = {product: amount for product, amount in anzahlen.items() if amount > 0}
    if selected_products:
        st.session_state['selected_products'] = selected_products
        st.session_state['show_results'] = True

# Neue Seite mit den ausgewählten Produkten und PDF-Export
if 'show_results' in st.session_state and st.session_state['show_results']:
    st.header("Ausgewählte Produkte")
    selected_df = pd.DataFrame(list(st.session_state['selected_products'].items()), columns=['Produkt', 'Anzahl'])
    st.table(selected_df)

    # PDF-Export
    if st.button("Als PDF exportieren"):
        # Erstellen Sie einen BytesIO-Puffer für das PDF
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=(8 * cm, 24 * cm), topMargin=0.5 * cm)
        elements = []

        # Styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.fontSize = 18  # Größere Schriftgröße für die neue Seitengröße

        # Überschrift
        elements.append(Paragraph("Einkaufsliste", title_style))
        elements.append(Spacer(1, 5))  # Kleinerer Abstand zwischen Überschrift und Tabelle

        # Tabelle
        data = [["", "Produkt", "Menge"]] + [[str(i+1), row['Produkt'], row['Anzahl']] for i, row in selected_df.iterrows()]
        table = Table(data, colWidths=[0.5 * cm, 6 * cm, 1.5 * cm])  # Spaltenbreite anpassen
        table.setStyle(TableStyle([
            ('BACKGROUND', (1, 0), (-1, 0), colors.HexColor("#808080")),  # Grau für die Überschrift
            ('TEXTCOLOR', (1, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (1, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 0), (-1, 0), 10),  # Kleinere Schriftgröße für die Produktnamen
            ('FONTSIZE', (0, 1), (0, -1), 8),  # Kleinere Schriftgröße für die Index-Spalte
            ('BOTTOMPADDING', (1, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('LEFTPADDING', (1, 1), (-1, -1), 5),
            ('RIGHTPADDING', (1, 1), (-1, -1), 5),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),  # Vertikale Ausrichtung in der Mitte
            ('ROWHEIGHT', (0, 1), (-1, -1), 20),  # Zeilenhöhe vergrößern
        ]))

        # Hintergrundfarbe für jede zweite Zeile setzen
        for i in range(1, len(data)):
            if i % 2 == 0:
                bg_color = colors.HexColor("#F0F0F0")  # Helle Grau Farbe für jede zweite Zeile
                table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), bg_color)]))

        elements.append(table)

        # PDF-Dokument erstellen
        doc.build(elements)

        # Stellen Sie den BytesIO-Puffer auf den Anfang zurück
        pdf_buffer.seek(0)

        st.download_button(label="Download PDF", data=pdf_buffer, file_name="Einkaufsliste.pdf", mime="application/pdf")
