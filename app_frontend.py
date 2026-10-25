import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="SuperKart Sales Forecaster", layout="wide")
st.title("🏪 SuperKart Sales Forecasting Dashboard")

@st.cache_resource
def load_model():
    return joblib.load('superkart_model.joblib')

try:
    model = load_model()
    st.sidebar.success("Model loaded successfully!")
except Exception as e:
    st.sidebar.error(f"Error loading model: {str(e)}")

tab1, tab2 = st.tabs(["Single Prediction", "Batch Prediction"])

with tab1:
    st.header("Predict Sales")
    product_weight = st.number_input("Product Weight", value=12.66)
    product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
    allocated_area = st.number_input("Product Allocated Area", value=0.027)
    product_mrp = st.number_input("Product MRP", value=117.08)
    product_id_char = st.selectbox("Product Id Category Char", ["FD", "DR", "NC"])
    store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
    store_location = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
    store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
    store_age = st.number_input("Store Age (Years)", value=16)
    product_type_cat = st.selectbox("Product Type Category", ["Perishables", "Non Perishables", "Others"])

    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar,
        "Product_Allocated_Area": allocated_area,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location,
        "Store_Type": store_type,
        "Product_Id_char": product_id_char,
        "Store_Age_Years": store_age,
        "Product_Type_Category": product_type_cat
    }

    if st.button("Forecast Sales"):
        try:
            input_df = pd.DataFrame([payload])
            prediction = model.predict(input_df)[0]
            st.success(f"💰 Predicted Store Sales Revenue: ${prediction:,.2f}")
        except Exception as e:
            st.error(f"Error generating prediction: {str(e)}")

with tab2:
    st.header("Upload CSV for Batch Sales Predictions")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)
        st.subheader("Uploaded Data Preview")
        st.dataframe(input_df.head())
        
        if st.button("Process Batch Forecast"):
            try:
                predictions = model.predict(input_df)
                out_df = input_df.copy()
                out_df['Predicted_Sales'] = predictions
                st.success("🎉 Batch Forecasting Completed!")
                st.subheader("Results Summary Preview")
                st.dataframe(out_df.head())
                csv_data = out_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Completed Forecasts (CSV)",
                    data=csv_data,
                    file_name="SuperKart_Sales_Forecasts.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error processing batch: {str(e)}")
