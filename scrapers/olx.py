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
                price = item.select_one('[data-aut-id="itemPrice"]').text if item.select_one('[data-aut-id="itemPrice"]') else "NA"
                results.append({
                    "website": "OLX",
                    "name": name,
                    "price": price
                })
            return results
    except:
        pass

    # Mock fallback for OLX
    mock_data = []
    for i in range(1, 7):
        price_val = random.randint(5, 25)
        km = random.randint(10, 80)
        mock_data.append({
            "website": "OLX (Mock)",
            "name": f"Used {model} - {km}k km driven",
            "price": f"₹ {price_val},{random.randint(10, 99)}000"
        })
    return mock_data
