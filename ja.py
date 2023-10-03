import streamlit as st
import pandas as pd
import numpy as np
import random
from scipy.stats import beta
import bayesianScenarios as bs
import willingnessToPayAnalysis as wtpa
import matplotlib.pyplot as plt

st.title('Junior Achievement')


col1, col2 = st.columns(2)

with col1:
    st.title('Survey Data')
    surveyed = st.number_input('Total Surveyed: ')
    wouldBuy = st.number_input('Amount that said they would buy: ')
    marketSize = st.number_input('Target Market Size: ')

    # Streamlit app
    st.title('Willingness to Pay Survey Data')

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

        x,y,worst_case, expected_case, best_case = bs.calcScenarios(surveyed=surveyed,yeses=wouldBuy,marketSize=marketSize)



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

        # Willingness to Pay Plot
        mean_price, std_deviation, confidence_interval = wtpa.calculate_and_print_optimal_price(priceData)
        actual_data = [price for price, count in priceData.items() for _ in range(count)]
        st.metric('mean price: ',mean_price)
        st.metric('stdDev: ', std_deviation)
        st.write('95% Confidence: ',confidence_interval)
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