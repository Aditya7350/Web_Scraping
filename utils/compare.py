import pandas as pd
import streamlit as st
import re

def parse_price(price_str):
    if not isinstance(price_str, str) or price_str == "NA": 
        return None
    
    price_str = price_str.lower().strip()
    
    # Check if it mentions 'Lakh' or 'Lac'
    is_lakh = "lakh" in price_str or "lac" in price_str
    
    # Extract numeric part (including decimals)
    cleaned = re.sub(r'[^0-9.]', '', price_str)
    
    try:
        val = float(cleaned)
        if is_lakh:
            val *= 100000
        return int(val)
    except:
        return None

def compare_prices(data):
    df = pd.DataFrame(data)

    if df.empty:
        st.write("### Collected Data")
        st.info("No data found from any source.")
        return

    st.write("### 📋 All Collected Data")
    st.dataframe(df, use_container_width=True)

    st.write("### 🏆 Best Price Options")

    # Parse prices to numeric for comparison
    df['price_num'] = df['price'].apply(parse_price)
    
    # Drop rows where price couldn't be parsed
    valid_df = df.dropna(subset=['price_num'])
    
    if valid_df.empty:
        st.warning("Could not extract valid prices for comparison.")
        return

    # Sort by price ascending
    best = valid_df.sort_values("price_num")
    
    # Format for display (remove the internal column)
    display_df = best[['website', 'name', 'price']].head(10)
    
    st.table(display_df) # Using table for better readability of winners