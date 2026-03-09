import requests
from bs4 import BeautifulSoup
import random

def get_spinny_prices(model):
    # Spinny URL pattern usually involves the city
    url = f"https://www.spinny.com/used-cars-in-delhi-ncr/s/?q={model.replace(' ', '%20')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }

    try:
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        
        # Spinny selectors (common patterns)
        cars = soup.select('div[class*="styles_carCard"]')
        
        if cars:
            for car in cars[:10]:
                name_el = car.select_one('div[class*="styles_carName"]')
                name = name_el.text.strip() if name_el else "NA"
                
                # Validation
                if model.lower().split()[0] not in name.lower():
                    continue
                    
                price_el = car.select_one('div[class*="styles_price"]')
                price = price_el.text.strip() if price_el else "NA"
                
                results.append({
                    "website": "Spinny",
                    "name": name,
                    "price": price
                })
            if results: return results
    except:
        pass

    # Simulated data for Demo
    mock_data = []
    base_price = 4.5
    if "creta" in model.lower(): base_price = 12.5
    elif "punch" in model.lower(): base_price = 6.2
    
    variants = ["Lxi", "Vxi", "Zxi", "Alpha", "Delta"]
    for var in variants:
        # Realistic variability
        price_val = base_price + random.uniform(-0.5, 5.0)
        mock_data.append({
            "website": "Spinny (Simulated)",
            "name": f"Certified {model} {var} - High Quality",
            "price": f"₹ {price_val:.2f} Lakh"
        })
    return mock_data
