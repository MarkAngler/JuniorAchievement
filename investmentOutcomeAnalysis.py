# Python script for Scenario Analysis

import numpy as np

def scenario_analysis(initial_investment, rate_of_return_scenarios, probabilities):
    """
    Perform a simple scenario analysis.

    Parameters:
    initial_investment (float): The initial investment amount.
    rate_of_return_scenarios (list): A list of possible rates of return. Expressed as percentages (e.g., 5 for 5%).
    probabilities (list): A list of probabilities corresponding to the rates of return.

    Returns:
    dict: A dictionary containing the initial investment, and the expected, worst-case, and best-case outcomes.
    """
    # Ensure the probabilities sum to 1
    if np.sum(probabilities) != 1:
        return "Probabilities must sum to 1."
    
    # Calculate the expected rate of return
    expected_rate_of_return = np.sum(np.array(rate_of_return_scenarios) * np.array(probabilities))
    
    # Calculate the worst-case and best-case rates of return
    worst_case_rate_of_return = np.min(rate_of_return_scenarios)
    best_case_rate_of_return = np.max(rate_of_return_scenarios)
    
    # Calculate the outcomes
    expected_outcome = initial_investment * (1 + (expected_rate_of_return / 100))
    worst_case_outcome = initial_investment * (1 + (worst_case_rate_of_return / 100))
    best_case_outcome = initial_investment * (1 + (best_case_rate_of_return / 100))
    
    return {
        "Initial Investment": initial_investment,
        "Expected Outcome": round(expected_outcome, 2),
        "Worst-Case Outcome": round(worst_case_outcome, 2),
        "Best-Case Outcome": round(best_case_outcome, 2)
    }

# Example usage:
initial_investment = 10000  # $10,000
rate_of_return_scenarios = [-5, 0, 5, 10]  # -5%, 0%, 5%, 10%
probabilities = [0.2, 0.3, 0.4, 0.1]  # Probabilities corresponding to the rates of return

analysis_result = scenario_analysis(initial_investment, rate_of_return_scenarios, probabilities)
print(f"Scenario Analysis Result: {analysis_result}")
