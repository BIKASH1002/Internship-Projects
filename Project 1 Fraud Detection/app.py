import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

model = joblib.load("fraud_detection_pipeline.pkl")

st.set_page_config(page_title="Fraud Detection", layout="centered")
st.title("💸 Real-Time Fraud Detection System")
st.markdown("Enter transaction details to predict if it's **fraudulent** or **legitimate**.")

amount = st.number_input("Transaction Amount", min_value=0.0)
type_ = st.selectbox("Transaction Type", options=['CASH_OUT', 'PAYMENT', 'TRANSFER', 'DEBIT', 'CASH_IN'])
step = st.number_input("Step (Hour in Simulation)", min_value=1, max_value=744, value=1)
oldbalanceOrg = st.number_input("Old Balance of Origin Account", min_value=0.0)
newbalanceOrig = st.number_input("New Balance of Origin Account", min_value=0.0)
oldbalanceDest = st.number_input("Old Balance of Destination Account", min_value=0.0)
newbalanceDest = st.number_input("New Balance of Destination Account", min_value=0.0)

isFlaggedFraud = 1 if type_ == 'TRANSFER' and amount > 200000 else 0

type_encoder = LabelEncoder()
type_encoder.fit(['CASH_OUT', 'PAYMENT', 'TRANSFER', 'DEBIT', 'CASH_IN'])
type_encoded = type_encoder.transform([type_])[0]

input_data = [[
    step, type_encoded, amount, oldbalanceOrg, newbalanceOrig,
    oldbalanceDest, newbalanceDest, isFlaggedFraud
]]
input_df = pd.DataFrame(input_data, columns=[
    'step', 'type', 'amount', 'oldbalanceOrg', 'newbalanceOrig',
    'oldbalanceDest', 'newbalanceDest', 'isFlaggedFraud'
])

if st.button("Predict Fraud"):
    probability = model.predict_proba(input_df)[0][1]
    custom_threshold = 0.3  
    prediction = 1 if probability >= custom_threshold else 0  

    if prediction == 1:
        st.error(f"❌ Fraudulent Transaction Detected! (Confidence: {probability:.2%})")
    else:
        st.success(f"✅ Legitimate Transaction (Confidence: {1 - probability:.2%})")
