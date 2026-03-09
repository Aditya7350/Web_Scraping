import requests
from bs4 import BeautifulSoup

def test_cars24():
    model = "Hyundai Creta"
    parts = model.lower().split()
    make = parts[0]
    model_name = parts[1]
    
    url = f"https://www.cars24.com/buy-used-cars-new-delhi/?f=make%3A{make}%3Bmodel%3A{model_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    print(f"Fetching: {url}")
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {r.status_code}")
        
        if r.status_code != 200:
            print("Blocked or page not found.")
            return

        soup = BeautifulSoup(r.text, "html.parser")
        
        # Check for existence of the selectors
        cars = soup.select("a.styles_carCardWrapper__sXLIp")
        print(f"Found {len(cars)} cars with selector 'a.styles_carCardWrapper__sXLIp'")
        
        if not cars:
            # Maybe the layout changed or it's JS rendered
            print("No cars found. Printing first 1000 chars of HTML...")
            print(r.text[:1000])
            
            # Check for common title/price keywords to find new selectors
            title_search = soup.find_all(string=lambda t: "Creta" in t)
            print(f"Occurrences of 'Creta': {len(title_search)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_cars24()
