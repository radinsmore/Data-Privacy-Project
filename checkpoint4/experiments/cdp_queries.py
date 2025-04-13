# experiments/cdp_queries.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import laplace_mechanism, compute_error, time_function
import pandas as pd
import numpy as np
import time

# Define the path to the CSV file
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'data.csv')

# Load data
df = pd.read_csv(DATA_PATH, sep=";")

# For demonstration, assume your CSV has the following columns:
# 'Debtor' (1 for debtor, 0 otherwise),
# 'Scholarship holder' (1 for scholarship, 0 otherwise),
# 'Age',
# 'Admission Grade',
# 'Dropout' (1 for dropout, 0 otherwise)
# Adjust query definitions as needed.

def query_dropout_count():
    """Count total dropouts."""
    return int((df['Target'] == "Dropout").sum())

def query_debtors_count():
    """Count students in debt."""
    return int(df['Debtor'].sum())

def query_scholarship_count():
    """Count scholarship holders."""
    return int(df['Scholarship holder'].sum())

def query_age_above_25():
    """Count students older than 25."""
    return int((df['Age at enrollment'] > 25).sum())

def query_high_admission_grade(threshold=14):
    """Count students with admission grade above threshold."""
    return int((df['Admission grade'] > threshold).sum())

# List of queries with labels for 10 different analytics queries.
# You can define additional queries as needed.
queries = {
    # Enrollment
    "dropout_count": query_dropout_count,
    "graduate_count": lambda: int((df['Target'] == "Graduate").sum()),
    
    # Financial factors
    "no_debtor_count": lambda: int((df['Debtor'] == 0).sum()),
    "debtors_count": query_debtors_count,
    "no_scholarship_count": lambda: int((df['Scholarship holder'] == 0).sum()),
    "scholarship_count": query_scholarship_count,

    # Age
    "age_above_25": query_age_above_25,
    "age_under_20": lambda: int((df['Age at enrollment'] < 20).sum()),

    # Grades
    "high_admission": lambda: query_high_admission_grade(14),
    "low_admission": lambda: int((df['Admission grade'] <= 14).sum()),
    
}

def run_cdp_experiments(epsilon_values, num_executions=10, sensitivity=1.0):
    """
    Run each query for each epsilon value num_executions times,
    and record runtime and error compared to ground truth.
    Returns a dictionary with query labels and results.
    """
    results = {}
    
    for query_label, query_func in queries.items():
        true_value = query_func()
        results[query_label] = {"epsilon": [], "noisy_values": [], "errors": [], "runtimes": []}
        
        for epsilon in epsilon_values:
            for _ in range(num_executions):
                # Time the noisy query execution
                def noisy_query():
                    return laplace_mechanism(true_value, sensitivity, epsilon)
                noisy_result, elapsed = time_function(noisy_query)
                error = compute_error(true_value, noisy_result)
                
                results[query_label]["epsilon"].append(epsilon)
                results[query_label]["noisy_values"].append(noisy_result)
                results[query_label]["errors"].append(error)
                results[query_label]["runtimes"].append(elapsed)
                
    return results

if __name__ == '__main__':
    # Define epsilon range (for example: 0.05, 0.1, 0.2, 0.5, 1.0)
    epsilons = [0.05, 0.1, 0.2, 0.5, 1.0]
    cdp_results = run_cdp_experiments(epsilons, num_executions=10, sensitivity=1.0)
    
    # Save results to CSV for each query in results/cdp/
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results', 'cdp')
    os.makedirs(output_dir, exist_ok=True)
    
    for query_label, data in cdp_results.items():
        out_df = pd.DataFrame(data)
        out_df['true_value'] = queries[query_label]()
        out_df.to_csv(os.path.join(output_dir, f"{query_label}_results.csv"), index=False)
    
    print("Central DP experiments complete. Results saved in results/cdp/")
