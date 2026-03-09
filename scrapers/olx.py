import requests
from bs4 import BeautifulSoup
import random

def get_olx_prices(model):
    # OLX search URL
    url = f"https://www.olx.in/items/q-{model.replace(' ', '-')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        
        # Selectors for OLX (these change often, so we use common classes if possible)
        items = soup.select('li[data-aut-id="itemBox"]')
        
        if items:
            for item in items[:10]:
                name = item.select_one('[data-aut-id="itemTitle"]').text if item.select_one('[data-aut-id="itemTitle"]') else "NA"
                
                # Strict Filtering: Skip mismatched results (like sponsored items)
                if model.lower().split()[0] not in name.lower():
                    continue
                    
                price = item.select_one('[data-aut-id="itemPrice"]').text if item.select_one('[data-aut-id="itemPrice"]') else "NA"
                results.append({
                    "website": "OLX",
                    "name": name,
                    "price": price
                })
            if results: return results
    except:
        pass

    # For Demo purposes - Simulated data when blocked or 0 results
    mock_data = []
    base_price = 5 # Default Lxi price
    if "creta" in model.lower(): base_price = 11
    elif "punch" in model.lower(): base_price = 5.2
    
    for i in range(1, 7):
        price_val = base_price + random.uniform(0.5, 4.0)
        mock_data.append({
            "website": "OLX (Simulated)",
            "name": f"Used {model} - {random.randint(5, 50)}k km driven",
            "price": f"₹ {int(price_val)},{random.randint(10, 99)}000"
        })
    return mock_data
