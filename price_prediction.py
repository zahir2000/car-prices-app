import streamlit as st
import pickle
import pandas as pd
import json

def app():
    def custom_sort(value):
        try:
            return int(value)  # Convert to integer if possible
        except ValueError:
            return float('inf')  # Assign a high value to non-numeric strings

    with open('unique_values.json', 'r') as f:
        unique_values = json.load(f)

    super_luxury = ['Rolls Royce', 'Bentley', 'Lamborghini', 'Ferrari', 'Bugatti', 'Pagani', 'Koenigsegg', 'Aston Martin', 'McLaren', 'Maybach']
    luxury = ['Porsche', 'Maserati', 'Mercedes-Benz', 'BMW', 'Audi', 'Tesla', 'Lexus', 'Jaguar', 'Mercedes-Maybach', 'Mercedes-AMG', 'Genesis', 'Alfa Romeo', 'BMW Alpina', 'Cadillac', 'Infiniti', 'Acura', 'Lincoln']
    highend = ['Volvo', 'Land Rover', 'MINI', 'Hummer', 'Jeep', 'Dodge', 'GMC', 'Chrysler', 'Opel', 'RAM', 'Subaru', 'Saab', 'MG']
    standard = ['Ford', 'Toyota', 'Chevrolet', 'Honda', 'Nissan', 'Volkswagen', 'Kia', 'Hyundai', 'Mazda', 'Mitsubishi', 'Peugeot', 'Renault', 'Fiat', 'Suzuki', 'Seat', 'Mercury', 'BYD', 'Buick', 'Oldsmobile']
    economy = ['Proton', 'TATA', 'GAC', 'Jetour', 'Haval', 'Chery', 'Changan', 'Great Wall', 'Geely', 'Hongqi', 'JAC', 'SsangYong', 'Zotye', 'Citroen', 'Datsun', 'Daewoo', 'Daihatsu', 'Lancia', 'Foton', 'CMC', 'Denza', 'DongFeng', 'GAC Gonow', 'Luxgen', 'Bufori', 'Zhongxing', 'Soueast']

    make_to_category = {}
    for category, makes in zip(['super luxury', 'luxury', 'highend', 'standard', 'economy'],
                            [super_luxury, luxury, highend, standard, economy]):
        for make in makes:
            make_to_category[make] = category

    make_category_mapping = {value.title(): value for value in unique_values['make_category']}
    sorted_make_category = sorted(make_category_mapping.keys())

    sorted_no_of_cylinders = sorted(unique_values['no_of_cylinders'], key=custom_sort)
    no_of_cylinders_mapping = {value: value for value in sorted_no_of_cylinders}

    horsepower_mapping = {value: value for value in unique_values['horsepower']}
    sorted_horsepower = sorted(horsepower_mapping.keys())

    engine_capacity_cc_mapping = {value: value for value in unique_values['engine_capacity_cc']}
    sorted_engine_capacity_cc = sorted(engine_capacity_cc_mapping.keys())

    exterior_color_mapping = {value: value for value in unique_values['exterior_color']}
    sorted_exterior_color = sorted(exterior_color_mapping.keys())

    body_type_mapping = {value: value for value in unique_values['body_type']}
    sorted_body_type = sorted(body_type_mapping.keys())

    regional_specs_mapping = {value: value for value in unique_values['regional_specs']}
    sorted_regional_specs = sorted(regional_specs_mapping.keys())

    # Load the saved model
    #model = joblib.load('xgb_model2.pkl')
    with open('xgb_model3.pkl', 'rb') as file:
        model = pickle.load(file)
    residuals_std_per_category = {
        'luxury': 145.43160204589725 * 1000,
        'standard': 48.47367882168356 * 1000,
        'super luxury': 663.3193665958463 * 1000,
        'highend': 97.9971238300231 * 1000,
        'economy': 65.47313716443578 * 1000
    }

    # Streamlit app layout
    st.title('🚗 Car Price Prediction')

    # User input fields
    with st.form("user_inputs"):
        #make_category_display = st.selectbox('Make Category', sorted_make_category)
        car_make = st.selectbox('Car Make', sorted(make_to_category.keys()))
        regional_specs_display = st.selectbox('Regional Specs', sorted_regional_specs)

        col1, col2, col3 = st.columns(3)
        with col1:
            no_of_cylinders_display = st.selectbox('Number of Cylinders', sorted_no_of_cylinders)
        with col2:
            horsepower_display = st.selectbox('Horsepower', sorted_horsepower)
        with col3:
            engine_capacity_cc_display= st.selectbox('Engine Capacity (cc)', sorted_engine_capacity_cc)

        col4, col5 = st.columns(2)
        with col4:
            body_type_display = st.selectbox('Body Type', sorted_body_type)
        with col5:
            seating_capacity = st.selectbox('Seating Capacity', unique_values['seating_capacity'])
        
        col6, col7 = st.columns(2)
        with col6:
            warranty = st.selectbox('Warranty', unique_values['warranty'])
        with col7:
            exterior_color_display = st.selectbox('Exterior Color', sorted_exterior_color)

        col8, col9 = st.columns(2)
        with col8:
            year = st.number_input('Year of Manufacture', min_value=1932, max_value=2024, value=2023)
        with col9:
            mileage = st.number_input('Mileage (in km)', min_value=0)

        # Form submission button with full width
        submitted = st.form_submit_button("Predict Price", help='Click to predict the price')

    if submitted:
        #make_category = make_category_mapping[make_category_display]
        make_category = make_to_category[car_make]
        no_of_cylinders = no_of_cylinders_mapping[no_of_cylinders_display]
        horsepower = horsepower_mapping[horsepower_display]
        engine_capacity_cc = engine_capacity_cc_mapping[engine_capacity_cc_display]
        exterior_color = exterior_color_mapping[exterior_color_display]
        body_type = body_type_mapping[body_type_display]
        regional_specs = regional_specs_mapping[regional_specs_display]

        # Create a DataFrame for the input features
        input_data = pd.DataFrame([[make_category, no_of_cylinders, horsepower, exterior_color, 
                                    body_type, regional_specs, warranty, seating_capacity, 
                                    engine_capacity_cc, year, mileage]],
                                columns=['make_category', 'no_of_cylinders', 'horsepower', 'exterior_color', 
                                        'body_type', 'regional_specs', 'warranty', 'seating_capacity', 
                                        'engine_capacity_cc', 'year', 'mileage'])

        # Predict the price
        predicted_price = model.predict(input_data)

        # Since price = price / 1000
        predicted_price = predicted_price * 1000

        # Get the standard deviation of residuals for the selected make_category
        selected_category_std = residuals_std_per_category[make_category]

        # Calculate the prediction interval for the selected category
        lower_bound = predicted_price - 1.96 * selected_category_std
        upper_bound = predicted_price + 1.96 * selected_category_std

        # Display the prediction and interval
        st.success(f'Predicted Price: **AED{predicted_price[0]:.2f}** \n \n 95% Prediction Interval: **AED{lower_bound[0]:.2f}** - **AED{upper_bound[0]:.2f}**')