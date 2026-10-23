import json
import time
import requests
import streamlit as st

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
# Increased timeout to 120 seconds to give Ollama enough time to generate
REQUEST_TIMEOUT = 120


# ---------------------------------------------------------
# FUNCTION: Check if Backend is Alive
# ---------------------------------------------------------
def check_backend():
    try:
        response = requests.get("http://localhost:8000/docs", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


# ---------------------------------------------------------
# FUNCTION: get_ollama_response (FREE)
# ---------------------------------------------------------
def get_ollama_response(input_text):
    if not input_text.strip():
        return "Please enter a topic first."

    try:
        with st.spinner(
            "Generating poem with Ollama (this may take 15–45 seconds)..."
        ):
            response = requests.post(
                "http://localhost:8000/poem/invoke",
                json={"input": {"topic": input_text}},
                timeout=REQUEST_TIMEOUT,
            )

            if response.status_code == 200:
                data = response.json()

                # --- EXTRACT OUTPUT FROM LANGSERVE RESPONSE ---
                if isinstance(data, dict):
                    output_val = data.get("output", data)

                    # 1. Output is directly a string
                    if isinstance(output_val, str):
                        return output_val

                    # 2. Output is a dict (e.g., AIMessage schema)
                    elif isinstance(output_val, dict):
                        if "content" in output_val:
                            return output_val["content"]
                        elif "text" in output_val:
                            return output_val["text"]
                        else:
                            return str(output_val)

                    # 3. Output is a list
                    elif isinstance(output_val, list):
                        return "".join([str(item) for item in output_val])

                return str(data)
            else:
                return f"Error: Server returned status {response.status_code}\n\n`{response.text}`"

    except requests.exceptions.Timeout:
        return "Error: The model took too long to respond (> 120s). Ensure Ollama is responsive."
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to localhost:8000. Is the FastAPI server running?"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


# ---------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------
st.set_page_config(page_title="LangChain Demo", page_icon="🤖")

st.title("LangChain Demo with Ollama by MyAi")

# CHECK BACKEND STATUS FIRST
if not check_backend():
    st.error("🚨 **Backend Server Not Found!**")
    st.warning(
        "Please ensure your FastAPI server (`app.py`) is running on `http://localhost:8000`."
    )
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Essay OpenAI")
    st.text_input("Topic for Essay", key="essay", disabled=True)
    st.button("Generate Essay 🚀", disabled=True)

with col2:
    st.subheader("🎵 Poem Ollama")
    poem_input = st.text_input(
        "Topic for Poem", key="poem", placeholder="e.g., Dogs, Space, Rain"
    )
    generate_btn = st.button("Generate Poem 🚀")

# ---------------------------------------------------------
# EXECUTION LOGIC
# ---------------------------------------------------------
if generate_btn:
    if poem_input:
        result = get_ollama_response(poem_input)
        if result:
            st.success("✅ Poem Generated!")
            st.markdown(result)
        else:
            st.error("Received empty response from the server.")
    else:
        st.warning("Please enter a topic before generating!")