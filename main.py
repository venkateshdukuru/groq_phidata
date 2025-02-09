import streamlit as st
import requests
import json

# Groq API credentials
GROQ_API_KEY = "API_key"  # Replace with your valid API key

# Function to interact with Groq API
def get_groq_response(user_input, language="python"):
    url = "https://api.groq.com/openai/v1/chat/completions"  # Ensure this is the correct URL
    headers = {
        "authorization": f"bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are a code assistant. Based on the user's query, you will solve coding problems using the appropriate language.
    The user can ask about solving coding problems in any language. You should:
    - Identify the problem the user is asking about.
    - Choose the appropriate language (e.g., Python, JavaScript, Java, etc.).
    - Provide the code solution in the requested language.
    - Provide a `README.md` file describing how to run the code.
    - Provide a `requirements.txt` if there are any dependencies or modules required for the project.

    The user will provide input like: "I need a program in {language} that does <describe the task>.".
    Please respond by giving the code, the `README.md`, and the `requirements.txt` in that order.

    User Query: {user_input}
    """

    data = {
        "model": "deepseek-r1-distill-llama-70b",  # Update to the correct model if needed
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6,
        "max_completion_tokens": 4096,
        "top_p": 0.95,
        "stream": False,  # Disable streaming for full response
        "reasoning_format": "raw"
    }

    try:
        # Send the POST request to the API
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the JSON response from the API
        response_json = response.json()

        # Extracting the code content from the response
        if "choices" in response_json:
            code = response_json["choices"][0]["message"]["content"]
            return code.strip()  # Clean and return the code content only
        else:
            return "No code found in response."

    except requests.exceptions.RequestException as e:
        # Handle network-related errors (e.g., timeout, connection error)
        st.error(f"Network error: {e}")
        return {"error": f"Network error: {e}"}
    except json.JSONDecodeError as e:
        # Handle errors in decoding the JSON
        st.error(f"Error parsing JSON: {e}")
        return {"error": f"Error parsing JSON: {e}"}

# Streamlit UI
st.title("Universal Code Assistant")

st.write("Ask me anything related to programming. I can help you solve problems in any language!")

# User input
user_input = st.text_area("Describe your problem or task", height=200)

# Language selection
language = st.selectbox("Choose programming language", ["Python", "JavaScript", "Java", "C++", "Ruby", "Go", "Other"])

if st.button("Get Solution"):
    if user_input:
        st.write("Generating solution...")

        # Get the response from Groq API
        response = get_groq_response(user_input, language)

        # Display the generated code
        st.subheader("Generated Code Solution")
        st.code(response, language=language.lower())

    else:
        st.warning("Please enter a problem or task.")
