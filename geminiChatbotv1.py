import streamlit as st
import google.generativeai as genai  # type: ignore

# Configure the Generative AI model
genai.configure(api_key="AIzaSyBbftyvw5CMaf_Jx0UYWc9LNbHFyiLoF8k")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="tunedModels/fashionqna-v8km73kjdcwc",
    generation_config=generation_config,
)

# Streamlit UI components
st.set_page_config(page_title="Shophoria AI", page_icon="🛍️")

# Display logo and title in a horizontal layout
col1, col2 = st.columns([1, 4])
with col1:
    st.image("C:/Users/AARISH/OneDrive/Desktop/capstone123/AARISH SIS/Shophira/images/logo.png", width=100)
with col2:
    st.title("Shophoria AI - Fashion Recommendations")

st.write("Welcome to Shophoria's AI-powered fashion recommendation app!")

# Input fields for additional user information
skin_tone = st.selectbox("Select your skin tone:", ["Fair", "Medium", "Olive", "Brown", "Dark"])
gender = st.selectbox("Select your gender:", ["Male", "Female", "Non-binary", "Other"])
age = st.number_input("Enter your age:", min_value=1, max_value=120, step=1)

# Input text box for user message
user_message = st.text_input("Enter your message for recommendation:")

# Process user message and generate response
if user_message:
    try:
        # Combine user inputs into a comprehensive prompt
        full_prompt = (
            f"User Details: Skin tone - {skin_tone}, Gender - {gender}, Age - {age}. "
            f"User Request: {user_message}"
        )

        # Start a new chat session
        chat_session = model.start_chat(history=[])

        # Send the combined prompt to the model and get the response
        response = chat_session.send_message(full_prompt)

        # Display the response in Streamlit
        st.subheader("AI Recommendation:")
        st.write(response.text)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Suggestion Box for feedback
st.subheader("Your Feedback/Suggestions:")
suggestion_box = st.text_area("Please provide your feedback or suggestions here:")

# Rating for the chatbot
st.subheader("Rate the Chatbot:")
rating = st.slider("Rate your experience:", 1, 5, 3)

# Display Thank You quote from the team
st.markdown(
    """
    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 10px; margin-top: 30px; text-align: center;">
        <h3 style="color: #2E86C1;">Thank you for using Shophoria AI!</h3>
        <p style="font-size: 16px; color: #34495E;">- Team Shophoria</p>
    </div>
    """,
    unsafe_allow_html=True
)
