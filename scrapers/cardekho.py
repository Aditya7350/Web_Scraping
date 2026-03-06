import requests
from bs4 import BeautifulSoup
import random

def get_cardekho_prices(model):
    url = f"https://www.cardekho.com/search?q={model}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }

    try:
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        cars = soup.select(".gsc_col-xs-12")

        if cars and len(cars) > 2: # Check if we actually got items (not just empty templates)
            for car in cars[:10]:
                name = car.select_one("a").text if car.select_one("a") else "NA"
                price = car.select_one(".price").text if car.select_one(".price") else "NA"
                results.append({
                    "website": "CarDekho",
                    "name": name,
                    "price": price
                })
            return results
    except Exception as e:
        pass

    # Expanded Mock Data for variety
    variants = ["Base Model", "Mid Variant", "Top Model", "Luxury Edition", "Sportz Pack", "Adventure Edition", "Smart Hybrid"]
    mock_data = []
    base_price = random.randint(8, 18)
    
    for var in variants[:6]: # Return 6 items
        price_val = base_price + random.uniform(0.5, 8.0)
        mock_data.append({
            "website": "CarDekho (Mock)",
            "name": f"{model} {var}",
            "price": f"Rs. {price_val:.2f} Lakh"
        })
    return mock_data