from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import pandas as pd
import time
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CSV_DIR = PROJECT_ROOT / "csv"

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")

driver = webdriver.Chrome(options=options)

df_top5 = pd.read_csv(CSV_DIR / "top5_destinations.csv")
top5_cities = df_top5["city"].tolist()

all_hotels = []

for city in top5_cities:
    url = f"https://www.booking.com/searchresults.fr.html?ss={city.replace(' ', '+')}"
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="property-card"]'))
        )
    except Exception:
        print(f"Aucun résultat détecté pour {city} après 15 secondes.")
        continue

    time.sleep(2)
    sel = Selector(text=driver.page_source)
    hotels = sel.xpath('//div[@data-testid="property-card"]')
    print(f"{city} : {len(hotels)} hôtels trouvés")

    for hotel in hotels:
        all_hotels.append({
            "city": city,
            "name": hotel.xpath('.//div[@data-testid="title"]/text()').get(),
            "url": hotel.xpath('.//a[@data-testid="title-link"]/@href').get(),
            "rating": hotel.xpath('.//div[@data-testid="review-score"]//text()').get(),
            "description": hotel.xpath('.//div[not(*)][string-length(normalize-space(text())) > 40]/text()').get(),
        })

driver.quit()

with open(CSV_DIR / "hotels_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_hotels, f, ensure_ascii=False, indent=2)

print(f"\nTotal hôtels collectés : {len(all_hotels)}")