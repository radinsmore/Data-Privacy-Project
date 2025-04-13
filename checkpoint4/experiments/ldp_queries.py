# experiments/ldp_queries.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import randomized_response, compute_error, time_function
import pandas as pd
import numpy as np
import time

# Define the path to the CSV file (same as in cdp_queries.py)
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'data.csv')

# Load data
df = pd.read_csv(DATA_PATH, sep=";")

# For simplicity, we will simulate LDP on binary queries.
def ldp_noisy_count(column_name, epsilon, positive_value):
    """
    Apply LDP mechanism on a column with a specific string value.
    Only records matching `positive_value` are considered as '1'.
    """
    binary_values = df[column_name].apply(lambda v: 1 if v == positive_value else 0)
    noisy_values = binary_values.apply(lambda v: randomized_response(v, epsilon))
    return noisy_values.sum()

# Define LDP queries in a similar dictionary
ldp_queries = {
    "dropout_count": lambda eps: ldp_noisy_count('Target', eps, 'Dropout'),
    "debtors_count": lambda eps: ldp_noisy_count('Debtor', eps, 1),
    "scholarship_count": lambda eps: ldp_noisy_count('Scholarship holder', eps, 1),
    # For non-binary columns, you can use the same structure or compute truthfully (if not the focus of privacy test)
    "age_above_25": lambda eps: int((df['Age at enrollment'] > 25).sum()),
    "high_admission": lambda eps: int((df['Admission grade'] > 14).sum()),
    "graduate_count": lambda eps: ldp_noisy_count('Target', eps, 'Graduate'),
    "age_under_20": lambda eps: int((df['Age at enrollment'] < 20).sum()),
    "low_admission": lambda eps: int((df['Admission grade'] <= 14).sum()),
    "no_debtor_count": lambda eps: ldp_noisy_count('Debtor', eps, 0),
    "no_scholarship_count": lambda eps: ldp_noisy_count('Scholarship holder', eps, 0),
}

# True values (from central non-private aggregation)
true_values = {
    # Enrollment
    "dropout_count": int((df['Target'] == "Dropout").sum()),
    "graduate_count": int((df['Target'] == "Graduate").sum()),

    # Financial factors
    "debtors_count": int(df['Debtor'].sum()),
    "no_debtor_count": int((df['Debtor'] == 0).sum()),
    "scholarship_count": int(df['Scholarship holder'].sum()),
    "no_scholarship_count": int((df['Scholarship holder'] == 0).sum()),

    # Age
    "age_above_25": int((df['Age at enrollment'] > 25).sum()),
    "age_under_20": int((df['Age at enrollment'] < 20).sum()),

    # Grades
    "high_admission": int((df['Admission grade'] > 14).sum()),
    "low_admission": int((df['Admission grade'] <= 14).sum()),
}

def run_ldp_experiments(epsilon_values, num_executions=10):
    """
    Run each LDP query for each epsilon value num_executions times.
    Record runtime and error compared to the true (non-private) value.
    """
    results = {}
    
    for query_label, query_func in ldp_queries.items():
        results[query_label] = {"epsilon": [], "noisy_values": [], "errors": [], "runtimes": []}
        
        for epsilon in epsilon_values:
            for _ in range(num_executions):
                def noisy_query():
                    return query_func(epsilon)
                noisy_result, elapsed = time_function(noisy_query)
                error = compute_error(true_values[query_label], noisy_result)
                
                results[query_label]["epsilon"].append(epsilon)
                results[query_label]["noisy_values"].append(noisy_result)
                results[query_label]["errors"].append(error)
                results[query_label]["runtimes"].append(elapsed)
                
    return results

if __name__ == '__main__':
    epsilons = [0.05, 0.1, 0.2, 0.5, 1.0]
    ldp_results = run_ldp_experiments(epsilons, num_executions=10)
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results', 'ldp')
    os.makedirs(output_dir, exist_ok=True)
    
    for query_label, data in ldp_results.items():
        out_df = pd.DataFrame(data)
        # Add the true value for comparison
        true_val = true_values[query_label]
        out_df['true_value'] = true_val
        out_df.to_csv(os.path.join(output_dir, f"{query_label}_results.csv"), index=False)
    
    print("Local DP experiments complete. Results saved in results/ldp/")
