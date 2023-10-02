# Python script to calculate Total Addressable Market (TAM)

def calculate_TAM(target_population, avg_price, purchase_frequency_per_year):
    """
    Calculate the Total Addressable Market (TAM)

    Parameters:
    target_population (int): The total number of potential customers in the target market.
    avg_price (float): The average price of the product or service.
    purchase_frequency_per_year (int): How often the product or service is purchased in a year.

    Returns:
    float: The Total Addressable Market (TAM) in monetary terms.
    """
    return target_population * avg_price * purchase_frequency_per_year

# Example usage:
# Assuming a target population of 1 million people
# Average price of the product is $50
# People purchase the product twice a year on average

target_population = 100 
avg_price = 6  
purchase_frequency_per_year = 1  

TAM = calculate_TAM(target_population, avg_price, purchase_frequency_per_year)
print(f"The Total Addressable Market (TAM) is ${TAM:,}")
