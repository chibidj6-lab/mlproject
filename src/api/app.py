# Import FastAPI to create the web server
from fastapi import FastAPI

# Import LangChain components for prompts and models
# UPDATE: LangChain imports have moved to specific packages (langchain-openai, langchain-ollama)
from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI  # Replaces deprecated langchain.chat_models
from langserve import add_routes
import uvicorn
import os
from langchain_ollama import ChatOllama  # Replaces langchain_community.llms.Ollama
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set the OpenAI API key from the environment
# WARNING: This line allows the script to use OpenAI, which incurs costs.
# If you don't have a key, comment this line out to avoid errors.
# os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"  # FIXED: Corrected typo 'decsription'
)

# ---------------------------------------------------------
# COST WARNING:
# The following block initializes an OpenAI model and adds a route.
# Every time someone calls /openai, you will be charged by OpenAI.
# ---------------------------------------------------------
# COMMENT OUT THE NEXT 3 LINES IF YOU DO NOT WANT TO PAY FOR OPENAI

# add_routes(
#     app,
#     ChatOpenAI(),
#     path="/openai"
# )

# Initialize a default OpenAI model instance
# WARNING: Creating this object is free, but USING it (sending requests) costs money.
# COMMENT OUT THE NEXT LINE IF YOU DO NOT WANT TO PAY FOR OPENAI
# model = ChatOpenAI() 
# model = None # Set to None to prevent errors if the line above is commented

# Initialize Ollama (Llama 2)
# This is FREE if you have Ollama installed and running locally on your Windows machine.
llm = ChatOllama(model="llama3.2:3b")

# Create a prompt template for an essay
# {topic} is a placeholder that will be replaced when you send a request
prompt1 = ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words")

# Create a prompt template for a children's poem
prompt2 = ChatPromptTemplate.from_template("Write me an poem about {topic} for a 5 years child with 100 words")

# ---------------------------------------------------------
# COST WARNING:
# The following route uses the 'model' variable.
# If 'model' is using OpenAI, this route will cost money.
# If 'model' is None (commented out), this route will crash unless handled.
# ---------------------------------------------------------
# COMMENT OUT THE NEXT 3 LINES IF YOU DO NOT WANT TO PAY FOR OPENAI
# if model:
#     add_routes(
#         app,
#         prompt1 | model,
#         path="/essay"
#     )

# This route uses Ollama (Llama 2), which is FREE locally.
add_routes(
    app,
    prompt2 | llm,
    path="/poem"
)

if __name__ == "__main__":
    # Start the server on localhost port 8000
    # You can access it at http://localhost:8000
    uvicorn.run(app, host="localhost", port=8000)


# to run this file, use the following command in your terminal in the api directoty:
# python app.py  