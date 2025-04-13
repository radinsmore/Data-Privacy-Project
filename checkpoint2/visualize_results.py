import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create a folder to store visualizations
output_dir = "visualizations"
os.makedirs(output_dir, exist_ok=True)

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

# Execute queries and store results in DataFrames
query_results = {key: pd.read_sql_query(q, conn) for key, q in queries.items()}

# Close database connection
conn.close()

# Define mapping for course codes to course names
course_mapping = {
    "33": "Biofuel Production Technologies",
    "171": "Animation and Multimedia Design",
    "8014": "Social Service (evening attendance)",
    "9003": "Agronomy",
    "9070": "Communication Design",
    "9085": "Veterinary Nursing",
    "9119": "Informatics Engineering",
    "9130": "Equinculture",
    "9147": "Management",
    "9238": "Social Service",
    "9254": "Tourism",
    "9500": "Nursing",
    "9556": "Oral Hygiene",
    "9670": "Advertising and Marketing Management",
    "9773": "Journalism and Communication",
    "9853": "Basic Education",
    "9991": "Management (evening attendance)"
}

# Generate and save visualizations without displaying them
for title, df in query_results.items():
    plt.figure(figsize=(12, 5))
    filename = f"{output_dir}/{title.replace(' ', '_').lower()}.png"
    
    # For dropout rates by course, replace course code with course name
    if title == "dropout_rates_by_course":
        df["Course"] = df["Course"].astype(str).map(course_mapping).fillna(df["Course"])
    
    if "percentage" in df.columns:
        plt.bar(df["Target"], df["percentage"], color=['red', 'blue', 'green'])
        plt.xlabel("Student Outcome")
        plt.ylabel("Percentage (%)")
        plt.title(title)
    
    elif "dropout_rate" in df.columns and "Course" in df.columns:
        plt.barh(df["Course"].astype(str), df["dropout_rate"], color='red')
        plt.xlabel("Dropout Rate (%)")
        plt.ylabel("Course")
        plt.title(title)
        plt.gca().invert_yaxis()
    
    elif "avg_admission_grade" in df.columns:
        plt.bar(df["Target"], df["avg_admission_grade"], color=['red', 'blue', 'green'])
        plt.xlabel("Student Outcome")
        plt.ylabel("Average Admission Grade")
        plt.title(title)
    
    elif "avg_unemployment_rate" in df.columns:
        df.set_index("Target").plot(kind="bar", figsize=(10, 6))
        plt.title(title)
        plt.ylabel("Average Value")
        plt.legend(["Unemployment Rate", "Inflation Rate", "GDP"])
        plt.xticks(rotation=0)
    
    elif "scholarship_students" in df.columns:
        df.set_index("Target").plot(kind="bar", figsize=(8, 5))
        plt.title(title)
        plt.ylabel("Count")
        plt.legend(["Scholarship Holders", "Students in Debt"])
        plt.xticks(rotation=0)
    
    elif "avg_first_sem_grade" in df.columns:
        plt.bar(df["Target"], df["avg_first_sem_grade"], color=['red', 'blue', 'green'])
        plt.xlabel("Student Outcome")
        plt.ylabel("Average First Semester Grade")
        plt.title(title)
    
    elif "dropout_rate" in df.columns and "Age at enrollment" in df.columns:
        plt.plot(df["Age at enrollment"], df["dropout_rate"], marker='o', linestyle='-')
        plt.xlabel("Age at Enrollment")
        plt.ylabel("Dropout Rate (%)")
        plt.title(title)
    
    elif "dropout_rate" in df.columns and "Gender" in df.columns:
        plt.bar(df["Gender"].astype(str), df["dropout_rate"], color=['purple', 'orange'])
        plt.xlabel("Gender")
        plt.ylabel("Dropout Rate (%)")
        plt.title(title)
    
    plt.savefig(filename)
    plt.close()

print(f"Visualizations saved in the '{output_dir}' folder!")
