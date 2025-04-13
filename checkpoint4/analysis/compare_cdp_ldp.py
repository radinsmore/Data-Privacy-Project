# analysis/compare_cdp_ldp.py

def main():
    comparison_text = """
    Comparison of Central Differential Privacy (CDP) and Local Differential Privacy (LDP):
    
    1. **Privacy Budget Allocation:**
       - In CDP, the trusted curator adds noise to the entire dataset. Hence, each query consumes an epsilon from the privacy budget.
       - In LDP, noise is applied at each user's record, and the overall aggregate is computed on privatized responses. 
         This typically requires a larger overall noise level (or a different per-user budget) to achieve similar accuracy.
    
    2. **Accuracy and Error:**
       - CDP typically offers better accuracy because noise is added after aggregation.
       - LDP introduces more noise due to the need to protect each user's data individually, which increases error in aggregate queries.
    
    3. **Runtime:**
       - The runtime differences are mostly due to the additional overhead of per-record randomization in LDP.
       - With both systems, runtime increases slightly with smaller epsilon (more noise) due to additional computation.
    
    4. **Pros and Cons:**
       - **Central DP (CDP):**
         - Pros: Better accuracy, simpler noise addition.
         - Cons: Requires a trusted curator.
       - **Local DP (LDP):**
         - Pros: No need for a trusted curator; stronger privacy guarantee per user.
         - Cons: Higher error, more complex if aggregating over many queries.
    
    In our experiments, as epsilon increases (i.e., less noise), both systems produce aggregate results closer to the true value, but LDP always shows a larger spread due to per-user noise. The trade-off between accuracy and privacy is more noticeable in LDP.
    """
    print(comparison_text)
    
if __name__ == '__main__':
    main()
