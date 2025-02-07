import sqlite3  # 📌 Lets Python talk to the SQLite database
import pandas as pd  # 📌 Helps read the CSV file

# 📌 Step 1: Connect to (or create) the database
conn = sqlite3.connect("data/ecommerce_data.db")  
cursor = conn.cursor()  # 📌 Allows us to send SQL commands to the database

# 📌 Step 2: Create a table if it doesn’t exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 📌 Unique ID for each product
    name TEXT,  -- 📌 Stores product names
    price REAL  -- 📌 Stores product prices
)
""")

# 📌 Step 3: Read the CSV file (the scraped data)
df = pd.read_csv("../data/amazon_laptops.csv")  # 📌 Load the scraped data

# 📌 Step 4: Clean the data (remove missing values)
df.dropna(inplace=True)  

# 📌 Step 5: Insert data into the database
for _, row in df.iterrows():  # 📌 Loops through every row in the CSV file
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", 
                   (row["Name"], row["Price"]))  # 📌 Inserts data into the database

# 📌 Step 6: Save and close the database
conn.commit()  # 📌 Saves the changes
conn.close()  # 📌 Closes the database

print("✅ Data stored in SQLite successfully!")  # 📌 Shows that everything worked!