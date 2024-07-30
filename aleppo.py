import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd

# Initialisiere die Session-State für die Liste der Geschäfte
if 'shops' not in st.session_state:
    st.session_state.shops = []

# Funktion zum Hinzufügen eines neuen Geschäfts
def add_shop():
    new_shop_name = f"Geschäft {len(st.session_state.shops) + 1}"
    st.session_state.shops.append({"Geschäft": new_shop_name})

# Funktion zum Löschen eines Geschäfts
def delete_shop(shop_to_delete):
    st.session_state.shops = [shop for shop in st.session_state.shops if shop["Geschäft"] != shop_to_delete]

# Sidebar
st.sidebar.title("Geschäfte")

# Konvertiere die Liste der Geschäfte in einen DataFrame für AgGrid
shops_df = pd.DataFrame(st.session_state.shops)

# AgGrid für die interaktive Tabelle
gb = GridOptionsBuilder.from_dataframe(shops_df)
gb.configure_selection(selection_mode="single", use_checkbox=True)
grid_options = gb.build()

grid_response = AgGrid(
    shops_df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    height=200,
    width='100%',
    reload_data=True,
)

# Schaltfläche zum Hinzufügen eines neuen Geschäfts
if st.sidebar.button('+ Geschäft hinzufügen'):
    add_shop()

# Schaltfläche zum Löschen eines Geschäfts
if st.sidebar.button('- Geschäft löschen'):
    if grid_response['selected_rows']:
        shop_to_delete = grid_response['selected_rows'][0]['Geschäft']
        delete_shop(shop_to_delete)

# Hauptseite
st.title("Hauptseite für verschiedene Geschäfte")
st.write("Geschäfte und ihre Namen:")
for shop in st.session_state.shops:
    st.write(f"{shop['Geschäft']}")

# Zusätzliche Inhalte für jedes Geschäft
for shop in st.session_state.shops:
    st.header(shop['Geschäft'])
    st.write(f"Hier könnten Informationen für {shop['Geschäft']} stehen.")
