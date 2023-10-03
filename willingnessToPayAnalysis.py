
import numpy as np
from scipy.stats import sem, t


def calculate_and_print_optimal_price(survey_data, confidence_level=0.95):
    # Create a list to hold the actual data points
    actual_data = []
    for price, count in survey_data.items():
        actual_data.extend([price] * count)
    
    # Check if data is empty
    if not actual_data:
        print("No data available for calculations.")
        return
    
    # Convert the list to a NumPy array
    actual_data = np.array(actual_data)
    
    # Calculate descriptive statistics
    mean_price = np.mean(actual_data)
    std_deviation = np.std(actual_data)
    
    # Calculate the confidence interval
    degrees_freedom = len(actual_data) - 1
    confidence_interval = t.interval(confidence_level, degrees_freedom, mean_price, sem(actual_data))
    
    return mean_price, std_deviation, confidence_interval



