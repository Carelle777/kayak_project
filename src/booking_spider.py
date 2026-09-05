import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CSV_DIR = PROJECT_ROOT / "csv"

class BookingSpider(scrapy.Spider):
    name = "booking_spider"

    custom_settings = {
        "FEEDS": {str(CSV_DIR / "hotels_raw.json"): {"format": "json"}},
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 2,
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "LOG_LEVEL": "INFO"
    }

    def __init__(self, cities=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            f"https://www.booking.com/searchresults.fr.html?ss={city.replace(' ', '+')}"
            for city in cities
        ]

    def parse(self, response):
        # --- DEBUG : sauvegarde la page brute reçue pour inspection ---
        city = response.url.split("ss=")[1].split("&")[0].replace("+", " ")
        debug_file = CSV_DIR / f"debug_{city.replace(' ', '_')}.html"
        debug_file.write_text(response.text, encoding="utf-8")

        hotels = response.xpath('//div[@data-testid="property-card"]')
        self.log(f"Ville: {city} | Statut: {response.status} | Hôtels trouvés: {len(hotels)}")

        for hotel in hotels:
            yield {
                "city": city,
                "name": hotel.xpath('.//div[@data-testid="title"]/text()').get(),
                "url": hotel.xpath('.//a[@data-testid="title-link"]/@href').get(),
                "rating": hotel.xpath('.//div[@data-testid="review-score"]//text()').get(),
                "description": hotel.xpath('.//div[@data-testid="recommended-units"]//text()').get(),
            }

if __name__ == "__main__":
    df_top5 = pd.read_csv(CSV_DIR / "top5_destinations.csv")
    top5_cities = df_top5["city"].tolist()

    process = CrawlerProcess()
    process.crawl(BookingSpider, cities=top5_cities)
    process.start()