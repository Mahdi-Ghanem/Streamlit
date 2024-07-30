import streamlit as st

# Initialisiere die Session-State für die Liste der Geschäfte
if 'shops' not in st.session_state:
    st.session_state.shops = []

# Funktion zum Hinzufügen eines neuen Geschäfts
def add_shop():
    new_shop_name = f"Geschäft {len(st.session_state.shops) + 1}"
    st.session_state.shops.append(new_shop_name)

# Funktion zum Löschen eines Geschäfts
def delete_shop(shop_to_delete):
    st.session_state.shops = [shop for shop in st.session_state.shops if shop != shop_to_delete]

# Sidebar
st.sidebar.title("Geschäfte")

# Anzeige der vorhandenen Geschäfte und Eingabefelder zur Umbenennung
for i, shop in enumerate(st.session_state.shops):
    cols = st.sidebar.columns([4, 1])
    new_name = cols[0].text_input(f"Name des Geschäfts {i+1}", value=shop, key=f"shop_{i}")
    st.session_state.shops[i] = new_name
    if cols[1].button("...", key=f"delete_{i}"):
        if st.sidebar.button(f"Löschen bestätigen {i}", key=f"confirm_delete_{i}"):
            delete_shop(shop)

# Schaltfläche zum Hinzufügen eines neuen Geschäfts
if st.sidebar.button('+ Geschäft hinzufügen'):
    add_shop()

# Hauptseite
st.title("Hauptseite für verschiedene Geschäfte")
st.write("Geschäfte und ihre Namen werden nur in der Sidebar angezeigt.")
