import requests
from bs4 import BeautifulSoup
import random

def get_carwale_prices(model):
    url = f"https://www.carwale.com/search/?q={model}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }

    try:
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        cars = soup.select(".o-jLqgOG")

        if cars and len(cars) > 2:
            for car in cars[:10]:
                name = car.select_one(".o-jLqgOG").text if car.select_one(".o-jLqgOG") else "NA"
                price = car.select_one(".o-cJrNdO").text if car.select_one(".o-cJrNdO") else "NA"
                results.append({
                    "website": "CarWale",
                    "name": name,
                    "price": price
                })
            return results
    except Exception as e:
        pass
        
    # Expanded Mock Data
    variants = ["S Option", "SX Opt Turbo", "EX Trim", "Manual Trend", "Automatic Luxury", "X-Line Premium", "Anniversary Ed."]
    mock_data = []
    base_price = random.randint(7, 16)
    
    for var in variants[:6]: # Return 6 items
        price_val = base_price + random.uniform(1.0, 9.0)
        mock_data.append({
            "website": "CarWale (Mock)",
            "name": f"{model} {var}",
            "price": f"Rs. {price_val:.2f} Lakh"
        })
    return mock_data