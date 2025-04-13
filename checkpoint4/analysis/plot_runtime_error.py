# analysis/plot_runtime_error.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import glob

def plot_metrics(results_dir, metric, output_dir):
    """
    For each CSV file in results_dir, plot the metric vs. epsilon.
    metric: 'errors' or 'runtimes'
    """
    os.makedirs(output_dir, exist_ok=True)
    csv_files = glob.glob(os.path.join(results_dir, "*.csv"))
    
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        query_name = os.path.basename(csv_file).replace("_results.csv", "")
        
        plt.figure()
        # Plot individual runs as scatter points
        plt.scatter(df['epsilon'], df[metric], alpha=0.7, label="Runs")
        plt.xlabel("Epsilon")
        plt.ylabel(metric.capitalize())
        plt.title(f"{query_name}: {metric.capitalize()} vs. Epsilon")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, f"{query_name}_{metric}.png"))
        plt.close()

if __name__ == '__main__':
    # Generate plots for CDP (central)
    plot_metrics(os.path.join(os.path.dirname(__file__), "..", "results", "cdp"),
                 metric="errors",
                 output_dir=os.path.join(os.path.dirname(__file__), "..", "results", "plots", "cdp"))
    plot_metrics(os.path.join(os.path.dirname(__file__), "..", "results", "cdp"),
                 metric="runtimes",
                 output_dir=os.path.join(os.path.dirname(__file__), "..", "results", "plots", "cdp"))
    
    # Generate plots for LDP (local)
    plot_metrics(os.path.join(os.path.dirname(__file__), "..", "results", "ldp"),
                 metric="errors",
                 output_dir=os.path.join(os.path.dirname(__file__), "..", "results", "plots", "ldp"))
    plot_metrics(os.path.join(os.path.dirname(__file__), "..", "results", "ldp"),
                 metric="runtimes",
                 output_dir=os.path.join(os.path.dirname(__file__), "..", "results", "plots", "ldp"))
    
    print("Plots generated and saved in results/plots/")
