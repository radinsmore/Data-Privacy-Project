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
def ldp_noisy_count(column_name, epsilon, threshold=None, positive_value=None, mode="eq"):
    """
    Apply LDP to a binary representation of the data.

    - If positive_value is specified, compare by equality.
    - If threshold and mode are specified, compare numerically:
        - mode="gt": value > threshold
        - mode="lt": value < threshold
    """
    if positive_value is not None:
        binary = (df[column_name] == positive_value).astype(int)
    elif threshold is not None:
        if mode == "gt":
            binary = (df[column_name] > threshold).astype(int)
        elif mode == "lt":
            binary = (df[column_name] < threshold).astype(int)
        elif mode == "ge":
            binary = (df[column_name] >= threshold).astype(int)
        elif mode == "le":
            binary = (df[column_name] <= threshold).astype(int)
        else:
            raise ValueError("Unsupported mode for threshold comparison")
    else:
        raise ValueError("Must provide either positive_value or threshold")

    noisy_values = randomized_response(binary, epsilon)
    return int(noisy_values.sum())

# Define LDP queries in a similar dictionary
ldp_queries = {
    "dropout_count": lambda eps: ldp_noisy_count('Target', eps, positive_value='Dropout'),
    "debtors_count": lambda eps: ldp_noisy_count('Debtor', eps, positive_value=1),
    "scholarship_count": lambda eps: ldp_noisy_count('Scholarship holder', eps, positive_value=1),
    # For non-binary columns, you can use the same structure or compute truthfully (if not the focus of privacy test)
    "graduate_count": lambda eps: ldp_noisy_count('Target', eps, positive_value='Graduate'),
    # "age_above_25": lambda eps: int((df['Age at enrollment'] > 25).sum()), #fix
    # "high_admission": lambda eps: int((df['Admission grade'] > 14).sum()), #fix
    # "age_under_20": lambda eps: ldp_noisy_count(int((df['Age at enrollment'] < 20).sum())), #fix
    # "low_admission": lambda eps: int((df['Admission grade'] <= 14).sum()), #fix
    "age_above_25": lambda eps: ldp_noisy_count("Age at enrollment", eps, threshold=25, mode="gt"),
    "high_admission": lambda eps: ldp_noisy_count("Admission grade", eps, threshold=14, mode="gt"),
    "age_under_20": lambda eps: ldp_noisy_count("Age at enrollment", eps, threshold=20, mode="lt"),
    "low_admission": lambda eps: ldp_noisy_count("Admission grade", eps, threshold=14, mode="le"),  # update function to support 'le'

    "no_debtor_count": lambda eps: ldp_noisy_count('Debtor', eps, positive_value=0),
    "no_scholarship_count": lambda eps: ldp_noisy_count('Scholarship holder', eps, positive_value=0),
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
