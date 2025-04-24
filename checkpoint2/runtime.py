import sqlite3
import time

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Count how many rows are in the table
cursor.execute("SELECT COUNT(*) FROM students")
total_students = cursor.fetchone()[0]

# Number of rows to simulate
num_rows = 5

start_no_delay = time.perf_counter()

for i in range(num_rows):
    cursor.execute("SELECT \"Admission grade\" FROM students LIMIT 1 OFFSET ?", (i,))
    cursor.fetchone()

end_no_delay = time.perf_counter()
print(f"Time without delay: {end_no_delay - start_no_delay:.6f} seconds")

print("\nRunning queries WITH artificial delay to simulate uniform query time (min 0.1s each)...")
start_with_delay = time.time()

for i in range(num_rows):
    query_start = time.time()
    cursor.execute("SELECT \"Admission grade\" FROM students LIMIT 1 OFFSET ?", (i,))
    cursor.fetchone()
    elapsed = time.time() - query_start
    if elapsed < 0.1:
        time.sleep(0.1 - elapsed)

end_with_delay = time.time()
print(f"Time with delay:    {end_with_delay - start_with_delay:.4f} seconds")

conn.close()
