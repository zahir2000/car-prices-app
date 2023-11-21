import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def app():
    # Read the data
    data = pd.read_parquet('data_with_price_changes.parquet')

    # Streamlit page layout
    st.title('📉 Track Price Changes')

    col1, col2 = st.columns(2)

    with col1:
        make_choice = st.selectbox('Select Make', sorted(data['make'].unique()))
        filtered_data = data[data['make'] == make_choice]

    with col2:
        model_choice = st.selectbox('Select Model', sorted(filtered_data['model'].unique()))
        model_data = filtered_data[filtered_data['model'] == model_choice]

    # Select Year
    year_choice = st.selectbox('Select Year', sorted(model_data['year'].unique(), reverse=True))

    final_filtered_data = model_data[model_data['year'] == year_choice]

    #emirate_choice = st.selectbox('Select Emirate', final_filtered_data['emirate'].unique())
    #final_filtered_data = final_filtered_data[final_filtered_data['emirate'] == emirate_choice]

    #aggregated_data = final_filtered_data.groupby('date_updated')['price'].mean().reset_index()

    # Group data by year or date and calculate the average price
    average_price_over_time = model_data.groupby('year')['price'].mean().reset_index()

    fig = px.line(
        final_filtered_data.sort_values('kilometers'), # Sorting by mileage
        x='kilometers', 
        y='price',
        labels={'kilometers': 'Mileage', 'price': 'Price'},
        title=f'Price vs. Mileage in {year_choice} for {make_choice} {model_choice}'
    )

    m, b = np.polyfit(final_filtered_data['kilometers'], final_filtered_data['price'], 1)
    fig.add_trace(go.Scatter(x=final_filtered_data['kilometers'], y=m*final_filtered_data['kilometers'] + b, mode='lines', name='OLS Trend Line', line_color='red',
                             opacity=0.5))
    
    fig.update_layout(
        legend=dict(
            orientation="h",  # Horizontal orientation
            yanchor="bottom",
            y=1,  # Position of the legend (just below the chart)
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(fig)

    try:
        if average_price_over_time.empty:
            st.warning(f"No data available for {make_choice} {model_choice}.")
        else:
            # Create a Plotly graph
            fig = px.line(average_price_over_time, x='year', y='price', 
                        labels={'year': 'Year', 'price': 'Average Price'}, 
                        title=f'Average Price over Year Manufacture for {make_choice} {model_choice}')

            # Update layout to show only whole years on the x-axis
            fig.update_xaxes(dtick=1, tick0=average_price_over_time['year'].min(), type='linear')
            fig.update_traces(line=dict(width=2))
            st.plotly_chart(fig)
    except:
        st.warning(f"No data available for {make_choice} {model_choice}.")