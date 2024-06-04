import streamlit as st
import pandas as pd

# Beispiel-Daten
data = {
    "Produkt": [
        "Brokkoli 2,5kg", "Gouda (15kg)", "Hamburgerbrötchen 80g", "Hamburgerbrötchen 55g", 
        "Hollandaise Sauce", "Joghurt Griechisch", "Mozzarella", "Pommes 7 mm", 
        "Pommes 10 mm", "PUTEN 500g", "Salami Geschnitten 500G", "Spinat 2,5KG", 
        "Ayran 20x250ml", "CocaCola 24x0,33 L", "Cola ZERO (24x0,33 L)", 
        "Fanta EXOTIK (24x0,33 L)", "MEZZO MIX (24x0,33)", "Spreit (24x0,33 L)", 
        "Uludag (24x0,33)", "WASSER 0,5 L x 24", "Servietten", "B3 Deckel 100 st", 
        "B3 Salatschale Weiß 100 st", "CC375 BOX PP375 ML 50St", "CC50 Sossenbecher+D 500st", 
        "CC80 Sossenbeche BESCHER+", "Deckel 500 ST", "Döner Box GROSS", "Döner Box KLEIN", 
        "Hamburgerbox Klein 100st", "Papp schalen 250st", "Menubox Ungeteilt Beige 100st", 
        "Pergamentpapier 12,5kg", "Trinkbecher 100 st", "ALUFolie 1200g", 
        "HP3 WARMHALTEVERP LANCH 125st", "Pfand Kisten Flaschen (24X0,330 cl)"
    ]
}
df = pd.DataFrame(data)

# Kategorien definieren
lebensmittel = df.iloc[0:12]
getraenke = df.iloc[12:20]
verpackung = df.iloc[20:]

# CSS-Styling
def apply_styles():
    st.markdown("""
    <style>
    .product-name {
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 2px;
    }
    .category-box {
        background-color: rgba(0, 0, 0, 0.05);  /* Leichter Hintergrund */
        padding: 5px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    .lebensmittel {
        background-color: #ffcccc;  /* Leichtes Rot */
    }
    .getraenke {
        background-color: #cceeff;  /* Leichtes Blau */
    }
    .verpackung {
        background-color: #ccffcc;  /* Leichtes Grün */
    }
    .stNumberInput {
        padding: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# Start der Streamlit-App
st.title("Einkaufsliste für mein Geschäft")

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

# Neue Seite mit den ausgewählten Produkten
if 'show_results' in st.session_state and st.session_state['show_results']:
    st.header("Ausgewählte Produkte")
    selected_df = pd.DataFrame(list(st.session_state['selected_products'].items()), columns=['Produkt', 'Anzahl'])
    st.table(selected_df)
