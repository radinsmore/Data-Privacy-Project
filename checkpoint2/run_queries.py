import sqlite3
import pandas as pd
# Connect to SQLite database
db_file = "students.db"
conn = sqlite3.connect(db_file)

# Define SQL queries
queries = {
    "dropout_success_rate": """
        SELECT Target, COUNT(*) AS student_count, 
               ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM students)), 2) AS percentage
        FROM students
        GROUP BY Target
        ORDER BY student_count DESC;
    """,
    
    "dropout_rates_by_course": """
        SELECT Course, 
               COUNT(*) AS total_students,
               SUM(CASE WHEN Target = 'Dropout' THEN 1 ELSE 0 END) AS dropout_count,
               ROUND((SUM(CASE WHEN Target = 'Dropout' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS dropout_rate
        FROM students
        GROUP BY Course
        ORDER BY dropout_rate DESC;
    """,
    
    "admission_grade_vs_dropout": """
        SELECT Target, 
               ROUND(AVG("Admission grade"), 2) AS avg_admission_grade
        FROM students
        GROUP BY Target
        ORDER BY avg_admission_grade DESC;
    """,
    
    "socioeconomic_factors": """
        SELECT Target, 
               ROUND(AVG("Unemployment rate"), 2) AS avg_unemployment_rate,
               ROUND(AVG("Inflation rate"), 2) AS avg_inflation_rate,
               ROUND(AVG(GDP), 2) AS avg_GDP
        FROM students
        GROUP BY Target;
    """,
    
    "financial_factors": """
        SELECT Target, 
               SUM(CASE WHEN "Scholarship holder" = 1 THEN 1 ELSE 0 END) AS scholarship_students,
               SUM(CASE WHEN Debtor = 1 THEN 1 ELSE 0 END) AS students_in_debt
        FROM students
        GROUP BY Target;
    """,
    
    "first_semester_performance": """
        SELECT Target, 
               ROUND(AVG("Curricular units 1st sem (grade)"), 2) AS avg_first_sem_grade
        FROM students
        GROUP BY Target
        ORDER BY avg_first_sem_grade DESC;
    """,
    
    "dropout_by_age_group": """
        SELECT "Age at enrollment", 
               COUNT(*) AS total_students,
               SUM(CASE WHEN Target = 'Dropout' THEN 1 ELSE 0 END) AS dropout_count,
               ROUND((SUM(CASE WHEN Target = 'Dropout' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS dropout_rate
        FROM students
        GROUP BY "Age at enrollment"
        ORDER BY "Age at enrollment";
    """,
    
    "gender_dropout_rates": """
        SELECT Gender, 
               COUNT(*) AS total_students,
               SUM(CASE WHEN Target = 'Dropout' THEN 1 ELSE 0 END) AS dropout_count,
               ROUND((SUM(CASE WHEN Target = 'Dropout' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS dropout_rate
        FROM students
        GROUP BY Gender;
    """
}

# Execute queries and save results
for name, query in queries.items():
    df = pd.read_sql_query(query, conn)

    # Print result to console
    print(f"\n--- {name.replace('_', ' ').title()} ---")
    print(df)

    # Save to CSV
    df.to_csv(f"{name}.csv", index=False)

# Close database connection
conn.close()

print("\nAll queries executed successfully. Results saved as CSV files.")
