import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 📌 Set up Chrome options
options = Options()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-infobars")

# ✅ Rotate between real User-Agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]
options.add_argument(f"user-agent={random.choice(user_agents)}")

# 📌 Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 📌 Open Amazon
amazon_url = "https://www.amazon.com/s?k=laptop"
driver.get(amazon_url)

# ✅ Save HTML for debugging
with open("amazon_page.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

# 📌 Scroll down multiple times to load all products
for i in range(3):
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(random.uniform(2, 5))

# 📌 Debugging: Print HTML preview
print("🔍 PAGE HTML PREVIEW:\n", driver.page_source[:3000])

# 📌 Wait for product listings to appear dynamically
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 's-result-item') and @data-component-type='s-search-result']"))
    )
except:
    print("⚠️ Products did not load in time! Amazon might be blocking your scraper.")

# 📌 Extract product details
products = []
items = driver.find_elements(By.XPATH, "//div[contains(@class, 's-result-item') and @data-component-type='s-search-result']")

for item in items:
    try:
        name = item.find_element(By.XPATH, ".//h2[@class='a-size-medium a-spacing-none a-color-base a-text-normal']").text
    except:
        name = "N/A"

    try:
        price_whole = item.find_element(By.XPATH, ".//span[@class='a-price-whole']").text  # ✅ Price Whole
        price_fraction = item.find_element(By.XPATH, ".//span[@class='a-price-fraction']").text  # ✅ Price Fraction
        price = f"{price_whole}.{price_fraction}"  # ✅ Combine whole and fraction
    except:
        price = "N/A"

    products.append({"Name": name, "Price": price})

# 📌 Save data to CSV
df = pd.DataFrame(products)
df.to_csv("data/amazon_laptops.csv", index=False)

print("✅ Scraping Completed! Total products scraped:", len(products))
print("✅ Data saved to data/amazon_laptops.csv")

# 📌 Close browser
driver.quit()