import streamlit as st
import os
import json
import requests
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import load_model
from googletrans import Translator


st.set_page_config(page_title="AgroVision", layout="wide")
# Cache model to optimize performance
@st.cache_resource
def load_plant_model():
    import gdown
    file_id = "1s3jAEpMWxfxMmGRc5h0ydkfHhjy7WY2L"
    model_path = os.path.join(os.path.dirname(__file__), "plant_disease_prediction_model.h5")
    if not os.path.exists(model_path):
        gdown.download(f"https://drive.google.com/uc?id={file_id}", model_path, quiet=False)
    
    return load_model(model_path, compile=False)

# Load static JSON data once
@st.cache_resource
def load_json(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as file:
        return json.load(file)

working_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize Model & Data
model = load_plant_model()
class_indices = load_json("class_indices.json")
recommendations = load_json("recommendations.json")
market_data = load_json("market.json")
fertilizer_stores = load_json("maharashtra_fertilizer_stores.json")
crop_npk_data = load_json("crop_npk.json")


# API Configuration
OPENWEATHER_API_KEY = "e904ee2b79326aba2a44970e6ddce3d1"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

# Language Selection
translator = Translator()
LANG_DICT = {
    "English": {
        "Home": "Home",
        "Disease Detection": "Disease Detection",
        "Market Analysis": "Market Analysis",
        "Weather Analysis": "Weather Analysis",
        "Pesticides Hub": "Pesticides Hub",
        "Crop Analysis": "Crop Analysis",
        "Farma Bot": "Farma Bot"
    },
    "मराठी": {
        "Home": "मुख्यपृष्ठ",
        "Disease Detection": "रोग शोध",
        "Market Analysis": "बाजार विश्लेषण",
        "Weather Analysis": "हवामान विश्लेषण",
        "Pesticides Hub": "नजीकची खते दुकाने",
        "Crop Analysis": "पिक अनुमान",
        "Farma Bot": "फार्मा बॉट"
    }
}

# Custom CSS for green buttons
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #2E3B55;
        padding-top: 20px;
    }
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        padding: 12px;
        margin: 8px 0;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        font-weight: 600;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .language-radio {
        margin-top: 20px;
        margin-bottom: 20px;
    }
    div[role="radiogroup"] > label {
        color: white;
        padding: 8px 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar with green buttons
image = Image.open("logo.jpg")
image_resized = image.resize((200, 100))  # Set both width and height

st.sidebar.image(image_resized)
language = st.sidebar.radio("Select Language / भाषा निवडा", ["English", "मराठी"], key="lang", horizontal=True)

def t(text):
    if language == "मराठी":
        translated_text = LANG_DICT[language].get(text, translator.translate(text, dest="mr").text)
        translated_text = translated_text.replace("अॅप", "अ‍ॅप").replace("प्लांट", "वनस्पती").replace("हेल्थ", "आरोग्य")
        return translated_text
    return text

# Navigation using buttons
if 'current_page' not in st.session_state:
    st.session_state.current_page = t("Home")

# Create navigation buttons
nav_options = list(LANG_DICT[language].values())
for option in nav_options:
    if st.sidebar.button(option, key=f"nav_{option}"):
        st.session_state.current_page = option

# Add social media links
st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align: center; color: white;'>{t('Connect with us')}</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: center;'><a href='https://github.com/' style='color: white; margin: 0 5px;'>GitHub</a> | <a href='https://twitter.com/' style='color: white; margin: 0 5px;'>Twitter</a> | <a href='https://www.facebook.com/' style='color: white; margin: 0 5px;'>Facebook</a></div>", unsafe_allow_html=True)

# UI Components
def navbar():
    st.markdown(f"<nav style='background:#008000;padding:10px;text-align:center;color:white;'>"
                f"<h1>{t('AgroVision')}</h1></nav>", unsafe_allow_html=True)

def footer():
    st.markdown(f"<footer style='background:#222;padding:10px;text-align:center;color:white;'>"
                f"&copy; 2025 {t('AgroVision. All Rights Reserved.')}</footer>", unsafe_allow_html=True)

# Pages
def home():
    navbar()
    st.header(t("Welcome to AgroVision 🌿"))
    st.write(t("This app helps in plant disease detection, market analysis for crops, and weather updates."))
    st.markdown(f"<h2 style='color:#008000;'>{t('What can you do with this app?')}</h2>", unsafe_allow_html=True)
    st.write(t("1. **Disease Detection**: Upload a leaf photo to identify the disease and get treatment advice."))
    st.write(t("2. **Market Analysis**: Check crop prices and make smart buying or selling decisions."))
    st.write(t("3. **Weather Updates**: Stay up-to-date with the latest weather forecasts, and plan your farming activities accordingly."))
    st.write(t("4. **Nearby Stores**: Find fertilizer stores near your location, and purchase the necessary supplies for your crops."))
    st.write(t("5. **Crop Prediction**: Get personalized crop recommendations based on your soil type, climate, and other factors."))
    st.markdown(f"<h3 style='color:#008000;'>{t('Get started now!')}</h3>", unsafe_allow_html=True)
    st.write(t("Explore the different features of this app, and start improving your farming practices today!"))
    footer()

def disease_detection():
    navbar()
    st.title(t('🌿 Plant Disease Detection'))
    uploaded_image = st.file_uploader(t("📤 Upload an image..."), type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image.resize((150, 150)), caption=t("Uploaded Image"))
        if st.button(t('🔍 Classify')):
            with st.spinner(t("Processing...")):
                prediction = predict_image_class(model, image)
                st.success(f'✅ {t("Prediction")}: {t(prediction)}')
                if prediction in recommendations:
                    for key, value in recommendations[prediction].items():
                        st.write(f"{t(key)}: {t(value)}")
    footer()

def market_analysis():
    navbar()
    st.title(t("📊 Market Analysis"))
    selected_crop = st.selectbox(t("Select a Crop:"), list(market_data["crops"].keys()))
    if selected_crop:
        crop_prices = market_data["crops"][selected_crop]
        min_price, max_price = crop_prices["min_price"], crop_prices["max_price"]
        st.success(f'{t("Current market price range for")} {t(selected_crop)}: ₹{min_price} - ₹{max_price}')
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot([0, 1], [min_price, max_price], marker='o', color='black', linestyle='-', linewidth=3)
        ax.set_xticks([0, 1])
        ax.set_xticklabels([t("Min"), t("Max")])  
        ax.set_ylabel(t("Price (₹)"))
        ax.set_title(t(f"Market Price Trend for {selected_crop}"))
        ax.grid(axis='y', linestyle='--', alpha=0.6)
        st.pyplot(fig, use_container_width=False)
    footer()

def weather_analysis():
    navbar()
    st.title(t("🌦 Weather Analysis"))
    city = st.text_input(t("Enter city name:"))
    if city and st.button(t("Get Weather")):
        with st.spinner(t("Fetching data...")):
            weather_data = get_weather(city)
        if weather_data:
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            description = t(weather_data['weather'][0]['description'].capitalize())
            temp_color = "#FF5733" if temp > 30 else "#3498DB"
            
            st.success(f"{t('Weather in')} {city}")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"### 🌡 *{t('Temperature')}*")
                st.markdown(f"<h2 style='color:{temp_color};'>{temp}°C</h2>", unsafe_allow_html=True)

            with col2:
                st.markdown(f"### 💧 *{t('Humidity')}*")
                st.markdown(f"<h2 style='color:#1ABC9C;'>{humidity}%</h2>", unsafe_allow_html=True)

            with col3:
                st.markdown(f"### 💨 *{t('Wind Speed')}*")
                st.markdown(f"<h2 style='color:#F39C12;'>{wind_speed} m/s</h2>", unsafe_allow_html=True)

            st.markdown(
                f"<div style='background:#2C3E60;padding:10px;border-radius:10px;color:white;text-align:center;'>"
                f"<h3>☁ {t('Weather Condition')}</h3>"
                f"<h4>{description}</h4></div> <br>",
                unsafe_allow_html=True,
            )
        else:
            st.error(t("City not found or API error."))
    footer()

def nearby_stores():
    navbar()
    st.title(t("🛒 Nearby Fertilizer Stores"))
    stores_path = os.path.join(working_dir, "maharashtra_fertilizer_stores.json")
    with open(stores_path, "r") as file:
        store_data = json.load(file)
    selected_city = st.selectbox(t("🌍 Select City:"), list(store_data.keys()))
    if st.button(t("🔍 Search Stores")):
        st.subheader(f"{t('Stores in')} {selected_city}:")
        for store in store_data[selected_city]:
            st.write(f"{store['name']} - {store['address']}")
        st.map(pd.DataFrame(store_data[selected_city]))
    footer()

def crop_prediction():
    navbar()
    st.title(t("🌾 Crop Prediction"))
    N = st.number_input(t("Enter Nitrogen (N) value"), min_value=0, max_value=300)
    P = st.number_input(t("Enter Phosphorus (P) value"), min_value=0, max_value=300)
    K = st.number_input(t("Enter Potassium (K) value"), min_value=0, max_value=300)
    if st.button(t("🔍 Predict Best Crops")):
        matching_crops = [
            crop for crop, values in crop_npk_data.items()
            if values["N"][0] <= N <= values["N"][1] and
               values["P"][0] <= P <= values["P"][1] and
               values["K"][0] <= K <= values["K"][1]
        ]
        if matching_crops:
            st.success(f"{t('Best Crops for given NPK values')}: 🌾 {', '.join(map(t, matching_crops))}")
        else:
            st.warning(t("No exact match found. Consider adjusting NPK values."))
    footer()

# Utility Functions
def get_weather(city):
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    try:
        response = requests.get(WEATHER_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None
    
def load_and_preprocess_image(image, target_size=(224, 224)):
    img = image.resize(target_size)
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def predict_image_class(model, image):
    preprocessed_img = load_and_preprocess_image(image)
    predictions = model.predict(preprocessed_img)
    return class_indices.get(str(np.argmax(predictions, axis=1)[0]), "Unknown")

# Page routing
if st.session_state.current_page == t("Home"):
    home()
elif st.session_state.current_page == t("Disease Detection"):
    disease_detection()
elif st.session_state.current_page == t("Market Analysis"):
    market_analysis()
elif st.session_state.current_page == t("Weather Analysis"):
    weather_analysis()
elif st.session_state.current_page == t("Pesticides Hub"):
    nearby_stores()
elif st.session_state.current_page == t("Crop Analysis"):
    crop_prediction()
elif st.session_state.current_page == t("Farma Bot"):
    st.title("🤖 Farma Bot")
    with open("chat.py", "r", encoding="utf-8") as f:
        exec(f.read())
