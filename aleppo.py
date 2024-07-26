import streamlit as st
import pandas as pd
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO

# Beispiel-Daten
data = {
    "Produkt": [
        "Brokkoli 2,5kg", "Gouda (15kg)", "Hamburgerbrötchen 80g", "Hamburgerbrötchen 55g", 
        "Hollandaise Sauce", "Joghurt Griechisch", "Mozzarella", "Pommes 7 mm", 
        "Pommes 10 mm", "PUTEN 500g", "Salami Geschnitten 500G", "Spinat 2,5KG", 
        "Hollandaise", "Mehl", "Snack Dressing", "Potato wedges 2.5 kg", "Pommes salz",
        "Ayran 20x250ml", "CocaCola Dosen","CocaCola Glas", "Cola ZERO Dosen", "Cola ZERO Glas",
        "Fanta EXOTIK Dosen","Fanta EXOTIK Glas", "MEZZO MIX Dosen","MEZZO MIX Glas", "Spreit Dosen", "Spreit Glas",
        "Uludag Dosen","Uludag Glas", "WASSER 0,5 L", "Servietten", "B3 Deckel 100 st", 
        "B3 Salatschale Weiß 100 st", "CC375 BOX PP375 ML 50St", "CC50 Sossenbecher+D 500st", 
        "CC80 Sossenbeche BESCHER+", "Deckel 500 ST", "Döner Box GROSS", "Döner Box KLEIN", 
        "Hamburgerbox Klein 100st", "Papp schalen 250st", "Menubox Ungeteilt Beige 100st", 
        "Pergamentpapier 12,5kg", "Trinkbecher 100 st", "ALUFolie 1200g", 
        "HP3 WARMHALTEVERP LANCH 125st","Döner Beutel 16×16", "Gabel Plastik", "Pizza Box 30", "Pizza Box 26", "Pragsmentpapier 1/4"
    ]
}
df = pd.DataFrame(data)

# Kategorien definieren
lebensmittel = df.iloc[0:17]
getraenke = df.iloc[17:31]
verpackung = df.iloc[31:]

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
st.title("🍔🍟 Aleppo Einkaufsliste")

# Platz, um die Anzahl der Produkte einzugeben
st.header("Produkte")
anzahlen = {}

# Lebensmittel-Kategorie
st.markdown('<div class="category-box lebensmittel">', unsafe_allow_html=True)
st.subheader("Lebensmittel")
for index, row in lebensmittel.iterrows():
    product = row['Produkt']
    st.markdown(f"<div class='product-name'>{product}</div>", unsafe_allow_html=True)
    anzahl = st.number_input("", min_value=0, step=1, key=index)
    anzahlen[product] = anzahl
st.markdown('</div>', unsafe_allow_html=True)

# Getränke-Kategorie
st.markdown('<div class="category-box getraenke">', unsafe_allow_html=True)
st.subheader("Getränke")
for index, row in getraenke.iterrows():
    product = row['Produkt']
    st.markdown(f"<div class='product-name'>{product}</div>", unsafe_allow_html=True)
    anzahl = st.number_input("", min_value=0, step=1, key=index + len(lebensmittel))
    anzahlen[product] = anzahl
st.markdown('</div>', unsafe_allow_html=True)

# Verpackung und Sonstiges-Kategorie
st.markdown('<div class="category-box verpackung">', unsafe_allow_html=True)
st.subheader("Verpackung und Sonstiges")
for index, row in verpackung.iterrows():
    product = row['Produkt']
    st.markdown(f"<div class='product-name'>{product}</div>", unsafe_allow_html=True)
    anzahl = st.number_input("", min_value=0, step=1, key=index + len(lebensmittel) + len(getraenke))
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
        elements.append(Paragraph("Aleppo Einkauf", title_style))
        elements.append(Spacer(1, 5))  # Kleinerer Abstand zwischen Überschrift und Tabelle

        # Tabelle
        data = [["", "Produkt", "Menge"]] + [[str(i+1), row['Produkt'], row['Anzahl']] for i, row in selected_df.iterrows()]
        table = Table(data, colWidths=[0.5 * cm, 6 * cm, 1.5 * cm])  # Spaltenbreite anpassen
        table.setStyle(TableStyle([
            ('BACKGROUND', (1, 0), (-1, 0), colors.HexColor("#808080")),  # Grau für die Überschrift
            ('TEXTCOLOR', (1, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Zahlen in der Menge-Spalte nach rechts ausrichten
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
