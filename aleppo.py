import streamlit as st

# Title of the main page
st.title("Hauptseite für verschiedene Geschäfte")

# Sidebar title
st.sidebar.title("Geschäfte")

# Number of shops
number_of_shops = st.sidebar.number_input("Anzahl der Geschäfte", min_value=1, max_value=10, value=2, step=1)

# Dictionary to store shop names
shop_names = {}

# Loop to create input fields for each shop
for i in range(number_of_shops):
    shop_name = st.sidebar.text_input(f"Name des Geschäfts {i+1}", value=f"Geschäft {i+1}")
    shop_names[f"Geschäft {i+1}"] = shop_name

# Display the entered shop names on the main page
st.write("Geschäfte und ihre Namen:")
for key, value in shop_names.items():
    st.write(f"{key}: {value}")

# Additional content for each shop
for key, value in shop_names.items():
    st.header(value)
    st.write(f"Hier könnten Informationen für {value} stehen.")
