import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SuperKart Sales Forecaster", layout="wide")
st.title("🏪 SuperKart Sales Forecasting Dashboard")

backend_url = st.sidebar.text_input("Backend API Base URL", value="http://backend:7860")
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
        res = requests.post(f"{backend_url}/v1/predict", json=payload)
        if res.status_code == 200:
            st.success(f"Predicted Sales: ${res.json().get('prediction'):,.2f}")
        else:
            st.error(res.text)
