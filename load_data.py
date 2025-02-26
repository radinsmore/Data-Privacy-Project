import sqlite3
import pandas as pd

# Load the dataset
csv_file = "data.csv"  # Update with the actual path in your project
db_file = "students.db"

# Create a database connection
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Load the CSV into a Pandas DataFrame
df = pd.read_csv(csv_file, delimiter=';')

# Save DataFrame to SQL database
df.to_sql("students", conn, if_exists="replace", index=False)

# Close the connection
conn.close()

print("Data successfully loaded into the database.")

