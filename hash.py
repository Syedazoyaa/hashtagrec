from dotenv import load_dotenv
import streamlit as st
import base64
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI with your API key
genai.configure(api_key="AIzaSyDl2nIaYT9ef8vJ6NDhXnIOUj-Z_UmYfXU")  # Replace with your actual API key variable name

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-1.0-pro")
chat = model.start_chat(history=[])
st.set_page_config(page_title="Hashtags GEN", layout="wide")
def get_gemini_response(caption):
    try:
        prompt = f"Generate relevant 50 hashtags for the following caption: '{caption}'"
        response = chat.send_message(prompt, stream=True)
        return response
    except Exception as e:
        st.error(f"Error: {e}")

# Function to set background image using base64 encoding
def set_background_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Error: Image file '{image_path}' not found.")
    except Exception as e:
        st.error(f"Error: {e}")

# Set background image (assuming "hashbg.png" is in the same directory as main.py)
current_dir = os.path.dirname(__file__)
image_path = os.path.join(current_dir, "hashbg.png")
set_background_image(image_path)

# Initialize Streamlit app
# st.set_page_config(page_title="Hashtags GEN", layout="wide")
st.header("Generate Hashtags")

# User input
user_input = st.text_input("Enter your caption or tweet:", key="user_input")
submit = st.button("Generate Hashtags")

if submit and user_input:
    response = get_gemini_response(user_input)
    if response:
        st.subheader("Generated Hashtags:")
        hashtags = []
        for chunk in response:
            hashtags.append(chunk.text)
        st.write(", ".join(hashtags))
    else:
        st.error("Failed to get a response. Please try again later.")
elif submit and not user_input:
    st.warning("Please input a caption or tweet before submitting.")
