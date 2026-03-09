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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
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
                
                # Validation: Only add if the model name is in the title
                if model_name.lower() not in name.lower():
                    continue
                
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

    # If we are here, live scrape failed or was blocked. 
    # For demo purposes, we return simulated data but label it correctly.
    mock_data = []
    # Try to guess a reasonable price for the model if possible
    base_price = 10 # Default fallback
    if "creta" in model.lower(): base_price = 12
    elif "baleno" in model.lower(): base_price = 7
    elif "punch" in model.lower(): base_price = 6
    elif "fortuner" in model.lower(): base_price = 30
    
    variants = ["Base", "Mid", "Top", "Sport", "Luxury", "Smart"]
    for var in variants:
        price_val = base_price + random.uniform(-2, 5)
        mock_data.append({
            "website": "Cars24 (Simulated)",
            "name": f"Pre-owned {model} {var}",
            "price": f"₹{price_val:.2f} Lakh"
        })
    return mock_data
