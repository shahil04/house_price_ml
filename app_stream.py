import pickle
import pandas as pd
import streamlit as st

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide"
)

# =========================
# Load Model and Data
# =========================
@st.cache_resource
def load_model():
    with open("model_Final.pkl", "rb") as file:
        model = pickle.load(file)
    return model


@st.cache_data
def load_data():
    with open("locations.pkl", "rb") as file:
        locations = list(pickle.load(file))

    with open("area_type.pkl", "rb") as file:
        area_types = list(pickle.load(file))

    with open("avalibility.pkl", "rb") as file:
        available = list(pickle.load(file))

    return locations, area_types, available


model = load_model()
locations, area_types, available = load_data()


# =========================
# Prediction Function
# =========================
def predict_house_price(
    area_type,
    availability,
    location,
    size_bhk,
    total_sqft,
    bath,
    balcony
):
    try:
        # Create input data
        data = [[
            area_type,
            availability,
            location,
            int(size_bhk),
            float(total_sqft),
            int(bath),
            int(balcony)
        ]]

        # Column names must match model training
        columns = [
            "area_type",
            "availability",
            "location",
            "size_bhk",
            "total_sqft",
            "bath",
            "balcony"
        ]

        df = pd.DataFrame(data, columns=columns)

        # Prediction
        prediction = model.predict(df)

        price = round(float(prediction[0]), 2)

        return price

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


# =========================
# Streamlit UI
# =========================

st.title("🏠 House Price Prediction")

st.write(
    "Enter the property details below to predict "
    "the estimated house price."
)

st.divider()

# =========================
# Input Columns
# =========================

col1, col2 = st.columns(2)

with col1:

    area_type = st.selectbox(
        "Area Type",
        options=area_types,
        index=(
            area_types.index("Super built-up Area")
            if "Super built-up Area" in area_types
            else 0
        )
    )

    availability = st.selectbox(
        "Availability",
        options=available
    )

    location = st.selectbox(
        "Location",
        options=locations
    )

    size_bhk = st.number_input(
        "BHK Size",
        min_value=1,
        value=2,
        step=1
    )

with col2:

    total_sqft = st.number_input(
        "Total Size (sqft)",
        min_value=100.0,
        value=1000.0,
        step=50.0
    )

    bath = st.number_input(
        "Number of Bathrooms",
        min_value=1,
        value=2,
        step=1
    )

    balcony = st.number_input(
        "Number of Balconies",
        min_value=0,
        value=1,
        step=1
    )


# =========================
# Prediction Button
# =========================

st.divider()

if st.button("🔮 Predict House Price", type="primary"):

    price = predict_house_price(
        area_type,
        availability,
        location,
        size_bhk,
        total_sqft,
        bath,
        balcony
    )

    if price is not None:

        st.success(
            f"🏠 Estimated House Price: ₹{price} Lakh"
        )