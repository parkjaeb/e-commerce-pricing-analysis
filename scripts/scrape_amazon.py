import requests
from bs4 import BeautifulSoup
import pandas as pd

# Amazon search URL (modify the keyword for different products)
url = "https://www.amazon.com/s?k=laptop"

# Headers to mimic a real browser
headers = {"User-Agent": "Mozilla/5.0"}

# Send a request to Amazon
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Extract product details
products = []
for item in soup.find_all("div", class_="s-main-slot s-result-list s-search-results"):
    name = item.find("span", class_="a-size-medium a-color-base a-text-normal")
    price = item.find("span", class_="a-price-whole")

    if name and price:
        products.append({"Name": name.text.strip(), "Price": price.text.strip()})

# Convert to DataFrame and Save as CSV
df = pd.DataFrame(products)
df.to_csv("../data/amazon_laptops.csv", index=False)

print("✅ Scraping Completed! Data saved to data/amazon_laptops.csv")