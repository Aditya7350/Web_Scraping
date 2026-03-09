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

    # Parse prices for sorting
    df['price_num'] = df['price'].apply(parse_price)
    valid_df = df.dropna(subset=['price_num'])
    
    if valid_df.empty:
        st.write("### 📋 All Collected Data")
        st.dataframe(df[['website', 'name', 'price']], width='stretch')
        st.warning("Could not extract valid prices for comparison.")
        return

    # Sort results
    sorted_df = valid_df.sort_values("price_num")

    # 📊 Price Summary by Platform
    st.write("### 📈 Best Price by Platform")
    platform_best = valid_df.sort_values("price_num").groupby("website").first().reset_index()
    
    # Sort platforms by price (ascending)
    platform_best = platform_best.sort_values("price_num")
    
    cols = st.columns(len(platform_best))
    for i, (_, row) in enumerate(platform_best.iterrows()):
        site_name = row['website'].replace(" (Simulated)", "")
        price_val = row['price_num']
        price_disp = f"₹{price_val/100000:.2f}L" if price_val >= 100000 else f"₹{price_val:,}"
        
        with cols[i]:
            st.metric(site_name, price_disp, help=row['name'])
            if "(Simulated)" in row['website']:
                st.caption("Estimated")
            else:
                st.caption("Live Found")

    st.divider()

    # 🥇 Top Deal Highlight (The Absolute Best)
    best_deal = sorted_df.iloc[0]
    
    st.markdown("### 🏆 Top Pick (Absolute Lowest Price)")
    with st.container(border=True):
        col1, col2 = st.columns([1, 4])
        with col1:
            price_val = best_deal['price_num']
            price_disp = f"₹{price_val/100000:.2f}L" if price_val >= 100000 else f"₹{price_val:,}"
            st.metric("Best Overall", price_disp)
        with col2:
            st.markdown(f"**{best_deal['name']}**")
            st.caption(f"Source: {best_deal['website']}")
            st.success("✨ This is the most affordable options across all 5 sites.")

    st.divider()

    # Ranked Table
    st.write("### 📋 Full Price Ranking")
    display_df = sorted_df[['website', 'name', 'price']].copy()
    display_df.rename(columns={
        "website": "Platform",
        "name": "Listing Title",
        "price": "Market Price"
    }, inplace=True)
    
    st.dataframe(
        display_df, 
        width='stretch',
        hide_index=True
    )