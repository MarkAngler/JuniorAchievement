import streamlit as st
import pandas as pd
import numpy as np
import random
from scipy.stats import beta
import bayesianScenarios as bs
import willingnessToPayAnalysis as wtpa
import matplotlib.pyplot as plt


st.set_page_config(layout="wide")
st.title('Junior Achievement')


marketResearch, explanations = st.columns(2)

with marketResearch:
    st.subheader('Survey Data')

    surveyed = st.number_input('Total Surveyed: ')
    marketSize = st.number_input('Target Market Size: ')

    numProducts = st.slider('Number of Different Products:', min_value=1, max_value=10)
    products = {}
    for product in range(numProducts):

        wouldBuy = st.number_input('Amount that said they would buy: ', key=f'wouldBuy_{product}')
        products[product] = wouldBuy

    # Streamlit app
    st.subheader('Willingness to Pay Survey Data')

    # User input for the number of price points
    num_price_points = st.slider('Number of Different Price Points:', min_value=1, max_value=10)

    # Initialize an empty dictionary to hold survey data
    priceData = {}

    # User input for each price point and its frequency
    for i in range(num_price_points):
        st.write(f'Price Point {i + 1}')
        price = st.number_input(f'Price:', step=1.0, key=f'Price_{i}')
        count = st.number_input(f'Number of Responses:', min_value=0, step=1, key=f'Count_{i}')
        priceData[price] = count

    st.button("Reset", type="primary")
    if st.button('Calculate'):
        data_load_state = st.text('Loading data...')

        productExpectations = {}
        for product,results in products.items():
            x,y,worst_case, expected_case, best_case, expectedPercent = bs.calcScenarios(surveyed=surveyed,yeses=results,marketSize=marketSize)
            productExpectations[product] = expectedPercent
            print(productExpectations)

            # Plotting
            st.metric('Worst Case: ', worst_case)
            st.metric('Expected Case: ', expected_case)
            st.metric('Best Case: ', best_case)
            plt.figure(figsize=(10, 6))
            plt.plot(x, y, label='Posterior distribution')
            plt.axvline(x=worst_case, color='r', linestyle='--', label='Worst-case Scenario')
            plt.axvline(x=expected_case, color='g', linestyle='--', label='Median-case Scenario')
            plt.axvline(x=best_case, color='b', linestyle='--', label='Best-case Scenario')
            plt.title('Bayesian Posterior Distribution of "Yes" Probability')
            plt.xlabel('Probability of "Yes"')
            plt.ylabel('Density')
            plt.legend()
            
            st.pyplot(plt)

        if numProducts > 1:
            multiProductProbabilities = bs.calculate_exclusive_choice_probabilities(productExpectations)
            st.caption(multiProductProbabilities)


        # Willingness to Pay Plot
        mean_price, std_deviation, confidence_interval = wtpa.calculate_and_print_optimal_price(priceData)
        actual_data = [price for price, count in priceData.items() for _ in range(count)]
        
        st.metric('mean price: ',mean_price)
        st.metric('stdDev: ', std_deviation)
        st.metric('95% Confidence: ',str(confidence_interval))
        st.caption(f"""In the context of your data, the 95% confidence interval means that you can be 95% confident that the true average price people are willing to pay falls within this range. This is a way to understand the reliability of your sample mean; it gives you an idea of how much you can expect this sample mean to fluctuate if you were to collect more data.""")

        plt.figure(figsize=(10, 6))
        plt.subplot(1, 2, 2)
        plt.hist(actual_data, bins=20, edgecolor='black', alpha=0.7)
        plt.axvline(x=mean_price, color='r', linestyle='--', label=f'Mean: {mean_price:.2f}')
        plt.axvline(x=confidence_interval[0], color='g', linestyle='--', label=f'Lower CI: {confidence_interval[0]:.2f}')
        plt.axvline(x=confidence_interval[1], color='b', linestyle='--', label=f'Upper CI: {confidence_interval[1]:.2f}')
        plt.title('Willingness to Pay')
        plt.xlabel('Price')
        plt.ylabel('Frequency')
        plt.legend()
        
        # plt.tight_layout()
        st.pyplot(plt)


        data_load_state.text("Done! (using st.cache_data)")


    else:
        st.write('Reset')

with explanations:
    st.markdown("""
                ### Bayesian Scenarios:

Imagine you're trying to figure out how popular different flavors of ice cream are at your school. 
You ask a bunch of students if they like vanilla or chocolate. Not everyone says yes, and you end up 
with a mix of answers.

Now, you want to use this info to predict how many ice creams you'd sell if you opened a little ice 
cream stand. The Bayesian part helps you take the answers you got and make an educated guess.

So, if you asked 100 people about vanilla and 40 said "Yes," you'd use some fancy math (Bayesian statistics) 
to predict that maybe around 40% of all students would buy vanilla ice cream. The same goes for chocolate 
or any other flavor.

### Multinomial Logit Model:

Now, let's say you realize something: What if some students who said they liked both vanilla and chocolate 
end up buying just one? They can't eat both at the same time, right?

Here's where the Multinomial Logit Model comes in. This is another fancy math thing that helps you figure 
out what people would choose when they have more than one option they like.

It's like asking, "Okay, if you like both vanilla and chocolate, which one would you pick if you could 
only have one?" This model helps you adjust your earlier predictions so they're more accurate.

### How They Work Together:

First, you use the Bayesian stuff to get a basic idea of how many people like each flavor. Think of this 
as your starting point. Then you use the Multinomial Logit Model to fine-tune those numbers based on the 
fact that people might have to choose just one flavor.

By combining these two methods, you get a more accurate prediction of how many ice creams of each flavor 
you might sell if you set up a stand at your school.
""")

# with financials:
#     st.subheader('Financials')
#     cogs = st.number_input('Cost of Goods Sold: ')
#     price = st.number_input('Price: ')

