import numpy as np
from scipy.stats import beta
# import matplotlib.pyplot as plt


def calcScenarios(surveyed,yeses,marketSize):
    # Set up Beta distribution parameters (adding 1 as a prior)
    alpha = yeses + 1
    beta_param = (surveyed - yeses) + 1

    # Generate Bayesian posterior distribution
    x = np.linspace(0, 1, 1000)
    y = beta.pdf(x, alpha, beta_param)

    # Plot the distribution
    # plt.figure(figsize=(12, 6))
    # plt.plot(x, y, label='Posterior distribution')
    # plt.title('Bayesian Posterior Distribution of "Yes" Probability')
    # plt.xlabel('Probability of "Yes"')
    # plt.ylabel('Density')
    # plt.legend()
    # plt.show()

    # Calculate percentiles for worst, expected, and best case scenarios
    worst_case = beta.ppf(0.1, alpha, beta_param)
    expected_case = beta.ppf(0.5, alpha, beta_param)
    best_case = beta.ppf(0.95, alpha, beta_param)

    # Assuming a target market size of 10,000
    target_market_size = marketSize

    # Calculate expected sales for different scenarios
    expected_sales_worst_case = worst_case * target_market_size
    expected_sales_expected_case = expected_case * target_market_size
    expected_sales_best_case = best_case * target_market_size

    return x,y,expected_sales_worst_case, expected_sales_expected_case, expected_sales_best_case
