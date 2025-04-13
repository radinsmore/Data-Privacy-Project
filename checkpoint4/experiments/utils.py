# experiments/utils.py

import numpy as np
import time

def laplace_mechanism(true_value, sensitivity, epsilon):
    """
    Apply Laplace noise to the true_value.
    """
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale)
    return true_value + noise

def randomized_response(value, epsilon):
    """
    A simple randomized response for binary attributes.
    For each binary value: with probability p, report the true value;
    with probability 1-p, flip the value.
    Here, we define p based on epsilon.
    """
    # For demonstration, assume p = exp(epsilon) / (exp(epsilon) + 1)
    p = np.exp(epsilon) / (np.exp(epsilon) + 1)
    if np.random.rand() < p:
        return value
    else:
        return 1 - value  # assuming binary 0/1

def compute_error(true_val, noisy_val):
    """
    Compute absolute error.
    """
    return abs(true_val - noisy_val)

def time_function(func, *args, **kwargs):
    """
    Time a function call.
    """
    start = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start
    return result, elapsed
