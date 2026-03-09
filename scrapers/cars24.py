import requests
from bs4 import BeautifulSoup
import random

def get_cars24_prices(model):
    # Cars24 often requires a city. We'll use new-delhi as a default for the demo.
    # Split the model to try and guess make/model for the filter string
    parts = model.lower().split()
    make = parts[0] if len(parts) > 0 else "hyundai"
    model_name = parts[1] if len(parts) > 1 else "creta"
    
    url = f"https://www.cars24.com/buy-used-cars-new-delhi/?f=make%3A{make}%3Bmodel%3A{model_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        
        # Selectors found by subagent
        cars = soup.select("a.styles_carCardWrapper__sXLIp")
        
        if cars:
            for car in cars[:10]:
                # Name usually contains year and model
                name_el = car.select_one("div.styles_contentWrap__9oSrl span:nth-of-type(2)")
                name = name_el.text.strip() if name_el else "NA"
                
                # Price
                price_el = car.select_one("div.styles_priceWrap__VwWBV p:last-of-type")
                price = price_el.text.strip() if price_el else "NA"
                
                results.append({
                    "website": "Cars24",
                    "name": name,
                    "price": price
                })
            if results:
                return results
    except Exception as e:
        pass

    # Mock fallback for Cars24
    variants = ["LXI", "VXI", "ZXI Plus", "Alpha", "Delta", "Sigma"]
    mock_data = []
    base_price = random.randint(6, 20)
    
    for var in variants[:6]:
        price_val = base_price + random.uniform(0.5, 7.0)
        mock_data.append({
            "website": "Cars24 (Mock)",
            "name": f"{model} {var}",
            "price": f"₹{price_val:.2f} Lakh"
        })
    return mock_data
