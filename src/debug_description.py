from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import time

options = Options()
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
driver.get("https://www.booking.com/searchresults.fr.html?ss=Collioure")

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//div[@data-testid="property-card"]'))
)
time.sleep(2)

sel = Selector(text=driver.page_source)
first_hotel = sel.xpath('//div[@data-testid="property-card"]')[0]

# Affiche le HTML complet du premier hôtel, tel que Selenium l'a vraiment reçu
print(first_hotel.get())

driver.quit()