import sqlite3  # 📌 Lets Python talk to the database

# 📌 Step 1: Connect to the database
conn = sqlite3.connect("data/ecommerce_data.db")  
cursor = conn.cursor()  # 📌 Allows us to send SQL queries

# 📌 Step 2: Write an SQL query
query = "SELECT * FROM products LIMIT 5;"  # 📌 Get the first 5 products

# 📌 Step 3: Run the query and fetch results
cursor.execute(query)  
rows = cursor.fetchall()  # 📌 Store the results

# 📌 Step 4: Print the results
print("\n📊 First 5 Products in the Database:")
for row in rows:
    print(row)  # 📌 Show each row (ID, Name, Price)

# 📌 Step 5: Close the database connection
conn.close()