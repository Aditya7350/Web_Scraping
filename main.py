import streamlit as st
from scrapers.carwale import get_carwale_prices
from scrapers.cardekho import get_cardekho_prices
from scrapers.olx import get_olx_prices
from utils.compare import compare_prices

st.set_page_config(page_title="Car Price Compare", layout="wide")

st.title("🚗 Car Price Compare")
st.markdown("Compare prices across various Indian car portals.")

car_model = st.text_input("Enter car model (e.g., Hyundai Creta 2022):", value="Hyundai Creta")

if st.button("Search") and car_model:
    data = []
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.spinner("Fetching from CarWale..."):
            try:
                res = get_carwale_prices(car_model)
                data += res
                st.success(f"CarWale: Found {len(res)} items")
            except Exception as e:
                st.warning(f"Failed to fetch CarWale: {e}")
            
    with col2:
        with st.spinner("Fetching from CarDekho..."):
            try:
                res = get_cardekho_prices(car_model)
                data += res
                st.success(f"CarDekho: Found {len(res)} items")
            except Exception as e:
                st.warning(f"Failed to fetch CarDekho: {e}")

    with col3:
        with st.spinner("Fetching from OLX..."):
            try:
                res = get_olx_prices(car_model)
                data += res
                st.success(f"OLX: Found {len(res)} items")
            except Exception as e:
                st.warning(f"Failed to fetch OLX: {e}")

    st.divider()
    compare_prices(data)