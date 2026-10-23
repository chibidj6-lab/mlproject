import streamlit as st
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ─── Environment ───────────────────────────────────────────────
load_dotenv()

# Optional: enable LangSmith tracing (remove if not using)
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")

# ─── Cached LLM (created once, reused across Streamlit reruns) ─
@st.cache_resource
def get_llm():
    return ChatOllama(
        model="llama3.2:3b",
        temperature=0.7,
        num_predict=512,
        num_ctx=4096,        # ← limit context to reduce memory pressure
        options={"num_thread": 4}  # ← limit CPU threads (avoid OOM on CPU)
    )

llm = get_llm()

# ─── Prompt Template ───────────────────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Respond clearly and concisely."),
    ("human", "Question: {question}"),
])

# ─── LCEL Chain ────────────────────────────────────────────────
chain = prompt | llm | StrOutputParser()

# ─── Streamlit UI ──────────────────────────────────────────────
st.set_page_config(page_title="LangChain + Ollama Demo", layout="centered")
st.title("LangChain Project using Llama3.2 by MyAi")

input_text = st.text_input("How may I help you?", placeholder="e.g., Explain about insurance services")

if input_text:
    with st.spinner("Generating response..."):
        try:
            response = chain.invoke({"question": input_text})
            st.write(response)
        except ConnectionResetError:
            st.error("Connection to Ollama was reset. The model may have run out of memory.")
            st.info("Try a shorter question, or switch to a smaller model (e.g., llama3.2:3b).")
        except Exception as e:
            st.error(f"Error: {e}")


# in the chatbot folder, run the following command to start the Streamlit app:
# streamlit run src/chatbot/app.py

# before that ensure the ollama is running on your local machine. 

# You can start the Ollama server by running the following command in your terminal:
# ollama serve