import streamlit as st
from chatbot_model import predict_tag, get_response

# Apply Custom Styling
st.markdown("""
    <style>
        body {
            background-color: #f5f7fa;
        }
        .stChatMessage {
            font-family: 'Arial', sans-serif;
            font-size: 18px;
            color: #333;
            padding: 10px;
            border-radius: 10px;
        }
        .stChatMessageUser {
            background-color: #007bff;
            color: white;
            font-weight: bold;
            padding: 12px;
            border-radius: 10px;
        }
        .stChatMessageAssistant {
            background-color: #ff9800;
            color: white;
            font-weight: bold;
            padding: 12px;
            border-radius: 10px;
        }
        h1 {
            color: #4CAF50;
            font-size: 36px;
            font-family: 'Georgia', serif;
            text-align: center;
        }
        p.subtitle {
            text-align: center;
            font-size: 22px;
            font-weight: 600;
        }
        .footer {
            text-align: center;
            padding-top: 20px;
            font-size: 16px;
            color: #777;
        }
    </style>
""", unsafe_allow_html=True)

# Display App Title
st.markdown("<h1>Welcome to ShopMate 🚀</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Ask anything about orders, returns, payments, or products.</p>", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle user input
if user_input := st.chat_input("Your message"):
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Predict intent & generate response
    tag = predict_tag(user_input)
    
    if tag:
        response = get_response(tag, user_input)
    else:
        response = "I'm sorry, I couldn't understand that. Please ask about orders, payments, returns, or refunds."

    # Ensure email links are clickable
    response = response.replace("jacobdarwin070@gmail.com", "[jacobdarwin070@gmail.com](mailto:jacobdarwin070@gmail.com)")

    # Display assistant response
    st.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer Section
st.markdown("<div class='footer'>Powered by ShopMate AI 🤖</div>", unsafe_allow_html=True)