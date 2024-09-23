import requests
import streamlit as st
import time

# Your API token and base URL
api_key = "LA-5fd947aa546e4f9fa3667f88e114cae6693ef734263240b684505facb8350c6f"
base_url = "https://api.llama-api.com"

# Set headers for authentication
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Initialize conversation history in session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []


# Function to handle the API request
def ask_llama(question, max_tokens=5000):
    api_request_json = {
        "messages": [
            {"role": "system", "content": "Assistant is a large language model trained by Llama API."},
            {"role": "user", "content": question}
        ],
        "max_tokens": max_tokens
    }

    # Make the API request
    response = requests.post(f"{base_url}/chat/completions", headers=headers, json=api_request_json)

    # Handle response
    if response.status_code == 200:
        response_data = response.json()
        if 'choices' in response_data and len(response_data['choices']) > 0:
            assistant_message = response_data['choices'][0]['message']['content']
            return assistant_message
        else:
            return "Error: No response from Llama API."
    else:
        return f"Error: {response.status_code} - {response.text}"


# Function to display responses with streaming effect
def display_streaming_response(response_text):
    response_placeholder = st.empty()  # Placeholder for dynamic updating
    full_response = ""

    # Simulate the typing effect by streaming each character
    for character in response_text:
        full_response += character
        response_placeholder.markdown(full_response)  # Update placeholder with partial response
        time.sleep(0.02)  # Adjust speed of streaming here


# Streamlit UI
st.title("Llama 3.1 Chatbot")
st.write("Ask any question, and the chatbot will answer using Llama API!")

# Input field for user question
user_question = st.text_input("Enter your question:")

# Handle user input and response generation
if st.button("Ask Llama"):
    if user_question:
        # Ask the question and get the response
        response = ask_llama(user_question, max_tokens=5000)

        # Save the conversation to history
        st.session_state.conversation_history.append({
            "user": user_question,
            "assistant": response
        })

        # Display the response with streaming effect
        display_streaming_response(response)

# Display conversation history, creating new chatboxes for each interaction
for i, entry in enumerate(st.session_state.conversation_history):
    with st.expander(f"Chat {i + 1}"):
        st.write(f"**User:** {entry['user']}")
        st.write(f"**Assistant:** {entry['assistant']}")
