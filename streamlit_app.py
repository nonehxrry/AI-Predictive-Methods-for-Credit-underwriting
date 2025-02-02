import streamlit as st
import pandas as pd
import joblib
from io import BytesIO
from fpdf import FPDF

# Set page configuration
st.set_page_config(
    page_title="AI Predictive Methods for Credit Underwriting",
    page_icon="💸",
    layout="wide"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(to right, #f0f4f8, #d9e4f5);
            font-family: 'Verdana', sans-serif;
        }
        .header-container {
            background: linear-gradient(to right, #007BFF, #66B2FF);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
        }
        .header-container h1 {
            font-size: 42px;
            font-weight: bold;
        }
        .header-container p {
            font-size: 22px;
            margin-top: 5px;
        }
        footer {
            text-align: center;
            margin-top: 50px;
            font-size: 16px;
            color: #444;
        }
        .stButton>button {
            background-color: #28a745;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #218838;
        }
        .stSlider>div {
            color: #007BFF;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown(
    """
    <div class="header-container">
        <h1>AI Predictive Methods for Credit Underwriting</h1>
        <p>Revolutionizing credit underwriting with AI-driven predictive analytics for smarter, faster decisions!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Load the trained model
model_path = 'best_features_model.pkl'
try:
    model = joblib.load(model_path)
    st.success("Model loaded successfully!")
except FileNotFoundError:
    st.error(f"Model file not found: {model_path}")
    st.stop()

# Initialize session state
if "loan_details" not in st.session_state:
    st.session_state["loan_details"] = {
        "full_name": "",
        "email": "",
        "phone": "",
        "cibil_score": 750,
        "income_annum": 5000000,
        "loan_amount": 2000000,
        "loan_term": 24,
        "loan_percent_income": 20.0,
        "active_loans": 1,
        "gender": "Men",
        "marital_status": "Single",
        "employee_status": "employed",
        "residence_type": "OWN",
        "loan_purpose": "Personal",
        "emi": None,
        "id_proof": None,
        "address_proof": None
    }

# Navigation menu
step = st.radio(
    "Navigate through the steps:",
    ["Personal Information", "Loan Details", "Upload Documents", "Final Decision"]
)

# Step 1: Personal Information
if step == "Personal Information":
    st.markdown("### Step 1: Personal Information")
    st.session_state["loan_details"]["full_name"] = st.text_input("Full Name", st.session_state["loan_details"]["full_name"])
    st.session_state["loan_details"]["email"] = st.text_input("Email Address", st.session_state["loan_details"]["email"])
    st.session_state["loan_details"]["phone"] = st.text_input("Phone Number", st.session_state["loan_details"]["phone"])

# Step 2: Loan Details
elif step == "Loan Details":
    st.markdown("### Step 2: Loan Details")
    st.session_state["loan_details"]["cibil_score"] = st.slider("CIBIL Score (300-900):", 300, 900, st.session_state["loan_details"]["cibil_score"])
    st.session_state["loan_details"]["income_annum"] = st.number_input("Annual Income (INR):", min_value=0, step=10000, value=st.session_state["loan_details"]["income_annum"])
    st.session_state["loan_details"]["loan_amount"] = st.number_input("Loan Amount (INR):", min_value=0, step=10000, value=st.session_state["loan_details"]["loan_amount"])
    st.session_state["loan_details"]["loan_term"] = st.number_input("Loan Term (Months):", min_value=1, step=1, value=st.session_state["loan_details"]["loan_term"])
    st.session_state["loan_details"]["loan_percent_income"] = st.number_input("Loan Percent of Income (%):", min_value=0.0, step=0.1, value=st.session_state["loan_details"]["loan_percent_income"])
    st.session_state["loan_details"]["active_loans"] = st.number_input("Number of Active Loans:", min_value=0, step=1, value=st.session_state["loan_details"]["active_loans"])
    st.session_state["loan_details"]["gender"] = st.selectbox("Gender:", ["Men", "Women"], index=0 if st.session_state["loan_details"]["gender"] == "Men" else 1)
    st.session_state["loan_details"]["marital_status"] = st.selectbox("Marital Status:", ["Single", "Married"], index=0 if st.session_state["loan_details"]["marital_status"] == "Single" else 1)
    st.session_state["loan_details"]["employee_status"] = st.selectbox("Employment Status:", ["employed", "self employed", "unemployed", "student"], index=["employed", "self employed", "unemployed", "student"].index(st.session_state["loan_details"]["employee_status"]))
    st.session_state["loan_details"]["residence_type"] = st.selectbox("Residence Type:", ["MORTGAGE", "OWN", "RENT"], index=["MORTGAGE", "OWN", "RENT"].index(st.session_state["loan_details"]["residence_type"]))
    st.session_state["loan_details"]["loan_purpose"] = st.selectbox("Loan Purpose:", ["Vehicle", "Personal", "Home Renovation", "Education", "Medical", "Other"], index=["Vehicle", "Personal", "Home Renovation", "Education", "Medical", "Other"].index(st.session_state["loan_details"]["loan_purpose"]))

    # EMI Calculator
    st.markdown("### Loan EMI Calculator")
    loan_amount = st.session_state["loan_details"]["loan_amount"]
    loan_term_years = st.session_state["loan_details"]["loan_term"] / 12
    interest_rate = st.number_input("Interest Rate (%):", min_value=0.1, max_value=15.0, step=0.1, value=7.5)
    monthly_rate = interest_rate / (12 * 100)
    tenure_months = loan_term_years * 12
    if loan_amount > 0 and tenure_months > 0:
        emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
        st.session_state["loan_details"]["emi"] = emi
        st.write(f"**Estimated EMI:** ₹{emi:,.2f}")
    else:
        st.session_state["loan_details"]["emi"] = None
        st.write("Please provide valid loan amount and term.")

# Step 3: Upload Documents
elif step == "Upload Documents":
    st.markdown("### Step 3: Upload Documents")
    st.session_state["loan_details"]["id_proof"] = st.file_uploader("Upload ID Proof")
    st.session_state["loan_details"]["address_proof"] = st.file_uploader("Upload Address Proof")

# Step 4: Final Decision
elif step == "Final Decision":
    st.markdown("### Step 4: Final Decision")
    loan_details = st.session_state["loan_details"]

    # Prepare input data for prediction
    input_data = pd.DataFrame({
        "cibil_score": [loan_details["cibil_score"]],
        "income_annum": [loan_details["income_annum"]],
        "loan_amount": [loan_details["loan_amount"]],
        "loan_term": [loan_details["loan_term"]],
        "loan_percent_income": [loan_details["loan_percent_income"]],
        "active_loans": [loan_details["active_loans"]],
        "gender": [1 if loan_details["gender"] == "Women" else 0],
        "marital_status": [1 if loan_details["marital_status"] == "Married" else 0],
        "employee_status_self_employed": [1 if loan_details["employee_status"] == "self employed" else 0],
        "employee_status_unemployed": [1 if loan_details["employee_status"] == "unemployed" else 0],
        "employee_status_student": [1 if loan_details["employee_status"] == "student" else 0],
        "residence_type_OWN": [1 if loan_details["residence_type"] == "OWN" else 0],
        "residence_type_RENT": [1 if loan_details["residence_type"] == "RENT" else 0],
        "loan_purpose_Personal": [1 if loan_details["loan_purpose"] == "Personal" else 0],
        "loan_purpose_Home_Renovation": [1 if loan_details["loan_purpose"] == "Home Renovation" else 0],
        "loan_purpose_Education": [1 if loan_details["loan_purpose"] == "Education" else 0],
        "loan_purpose_Vehicle": [1 if loan_details["loan_purpose"] == "Vehicle" else 0],
    })

    input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

    # Prediction
    try:
        prediction = model.predict(input_data)
        prediction_proba = model.predict_proba(input_data)

        if prediction[0] == 1:
            st.markdown("### Loan Rejected ❌")
            st.error(f"Rejection Probability: {prediction_proba[0][1]:.2f}")
        else:
            st.markdown("### Loan Approved ✅")
            st.success(f"Approval Probability: {prediction_proba[0][0]:.2f}")

        # Generate PDF Report
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('FreeSerif', '', 'FreeSerif.ttf', uni=True)
        pdf.set_font("FreeSerif", size=12)

        pdf.cell(200, 10, txt="Loan Approval Prediction Report", ln=True, align="C")
        pdf.ln(10)

        # Personal Information
        pdf.cell(200, 10, txt="Personal Information:", ln=True)
        pdf.cell(200, 10, txt=f"Full Name: {loan_details.get('full_name', 'N/A')}", ln=True)
        pdf.cell(200, 10, txt=f"Email: {loan_details.get('email', 'N/A')}", ln=True)
        pdf.cell(200, 10, txt=f"Phone: {loan_details.get('phone', 'N/A')}", ln=True)
        pdf.ln(10)

        # Loan Details
        pdf.cell(200, 10, txt="Loan Details:", ln=True)
        pdf.cell(200, 10, txt=f"CIBIL Score: {loan_details.get('cibil_score', 'N/A')}", ln=True)
        pdf.cell(200, 10, txt=f"Loan Amount: ₹{loan_details.get('loan_amount', 'N/A')}", ln=True)
        pdf.cell(200, 10, txt=f"Loan Term: {loan_details.get('loan_term', 'N/A')} months", ln=True)
        emi_value = loan_details.get("emi", None)
        if emi_value is not None:
            pdf.cell(200, 10, txt=f"Estimated EMI: ₹{emi_value:,.2f}", ln=True)
        else:
            pdf.cell(200, 10, txt="Estimated EMI: Not Calculated", ln=True)
        pdf.ln(10)

        # Prediction Results
        pdf.cell(200, 10, txt="Prediction Results:", ln=True)
        pdf.cell(200, 10, txt=f"Prediction: {'Approved' if prediction[0] == 0 else 'Rejected'}", ln=True)
        pdf.cell(200, 10, txt=f"Approval Probability: {prediction_proba[0][0]:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Rejection Probability: {prediction_proba[0][1]:.2f}", ln=True)

        # Save PDF to buffer
        buffer = BytesIO()
        pdf.output(buffer, "S")
        buffer.seek(0)

        st.download_button(
            label="Download Report as PDF",
            data=buffer,
            file_name="loan_prediction_report.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Prediction failed: {e}")

# Footer
st.markdown(
    """
    <footer>
        <p>© 2025 AI Predictive Methods for Credit Underwriting. All rights reserved.</p>
    </footer>
    """,
    unsafe_allow_html=True
)
