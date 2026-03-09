import requests
from bs4 import BeautifulSoup

def test_olx():
    model = "Hyundai Creta"
    url = f"https://www.olx.in/items/q-{model.replace(' ', '-')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    print(f"Fetching OLX: {url}")
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    
    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.select('li[data-aut-id="itemBox"]')
    print(f"Found {len(items)} items on OLX")
    
    for item in items[:3]:
        name_el = item.select_one('[data-aut-id="itemTitle"]')
        price_el = item.select_one('[data-aut-id="itemPrice"]')
        print(f"- {name_el.text if name_el else 'NA'} : {price_el.text if price_el else 'NA'}")

if __name__ == "__main__":
    test_olx()
