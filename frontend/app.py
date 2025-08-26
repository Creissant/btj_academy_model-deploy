import streamlit as st
from api.prediction import predict_survival

st.title("🚢 Titanic Survival Prediction")

st.write("Enter the details of a Titanic passenger to predict whether he survived or not.")

# Input form
with st.form("prediction_form"):
    pclass = st.selectbox("Passenger Class", [1, 2, 3])
    sex = st.selectbox("Gender of the passenger", ["male", "female"])
    age = st.number_input("Age (in years)", min_value=0, max_value=100, value=25)
    sibsp = st.number_input("Number of Siblings/Spouses Aboard", min_value=0, value=0)
    parch = st.number_input("Number of Parents/Children Aboard", min_value=0, value=0)
    fare = st.number_input("Ticket Fare", min_value=0.0, value=0.0, step=0.0001, format="%.4f")
    embarked = st.selectbox("Port of Embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)", ["C", "Q", "S"])
    nametitle = st.selectbox("Passenger Name Title (Rare = Other title)", ["Mr", "Mrs", "Miss", "Master", "Rare"])

    submitted = st.form_submit_button("Predict")

# Handle submit
if submitted:
    payload = {
        "Pclass": pclass,
        "Sex": sex,
        "Age": age,
        "SibSp": sibsp,
        "Parch": parch,
        "Fare": fare,
        "Embarked": embarked,
        "NameTitle": nametitle
    }

    result = predict_survival(payload)

    if "error" in result:
        st.error(f"❌ Request failed: {result['error']}")
    else:
        st.success(
            f"✅ Prediction: {'The Passenger Survived (1)' if result['result'] == 1 else 'The Passenger did not survive (0)'}"
        )
        if "probability" in result and result["probability"]:
            st.write("Probabilities:", result["probability"])
