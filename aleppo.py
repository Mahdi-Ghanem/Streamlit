import streamlit as st

# Initialisieren der Session-State für die Liste der Geschäfte
if 'shops' not in st.session_state:
    st.session_state.shops = []

# Funktion zum Hinzufügen eines neuen Geschäfts
def add_shop():
    st.session_state.shops.append(f"Geschäft {len(st.session_state.shops) + 1}")

# Funktion zum Löschen eines Geschäfts
def delete_shop(shop_to_delete):
    st.session_state.shops = [shop for shop in st.session_state.shops if shop != shop_to_delete]

# Sidebar
st.sidebar.title("Geschäfte")

# Anzeige der vorhandenen Geschäfte und Eingabefelder zur Umbenennung
for i, shop in enumerate(st.session_state.shops):
    new_name = st.sidebar.text_input(f"Name des Geschäfts {i+1}", value=shop)
    st.session_state.shops[i] = new_name

# Schaltfläche zum Hinzufügen eines neuen Geschäfts
if st.sidebar.button('+ Geschäft hinzufügen'):
    add_shop()

# Schaltfläche zum Löschen eines Geschäfts
if st.sidebar.button('- Geschäft löschen'):
    shop_to_delete = st.sidebar.selectbox("Wählen Sie ein Geschäft zum Löschen", st.session_state.shops)
    if st.sidebar.button('Löschen bestätigen'):
        delete_shop(shop_to_delete)

# Hauptseite
st.title("Hauptseite für verschiedene Geschäfte")
st.write("Geschäfte und ihre Namen:")
for shop in st.session_state.shops:
    st.write(f"{shop}")

# Zusätzliche Inhalte für jedes Geschäft
for shop in st.session_state.shops:
    st.header(shop)
    st.write(f"Hier könnten Informationen für {shop} stehen.")
