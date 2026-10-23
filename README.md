# My ML Project

fraud_detection/
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── chatbot/
├── tests/
├── notebooks/
├── .env
├── requirements.txt
├── pyproject.toml
└── README.md          

## Overview
One-paragraph description of what the project does.

## Project Structure
| Path | Purpose |
|:---|:---|
| `src/data/loader.py` | Loads raw claims from CSV/DB, handles missing values |
| `src/features/engineering.py` | Builds features: rejection_ratio, diag_agg, etc. |
| `src/models/fraud_model.py` | Trains & saves XGBoost classifier |
| `src/chatbot/app.py` | Streamlit UI for GenAI-powered query interface |
| `src/chatbot/chains.py` | LCEL chain definitions |
| `src/chatbot/prompts.py` | Prompt templates |

## src/chatbot/app.py
Purpose: Streamlit entrypoint
Flow: input → prompt → LLM → display
Windows Prerequisites (Step-by-Step)
Step 1: Install Ollama
Open PowerShell (no admin needed) and run:

winget install Ollama.Ollama

Or manually:

Go to ollama.com/download/windows
Download OllamaSetup.exe (~200 MB)
Double-click and follow the wizard 
After install, Ollama appears in your system tray (bottom-right).  The local server starts automatically at http://localhost:11434.

Step 2: Verify Ollama is running
Open a new PowerShell window:
ollama --version

You should see something like ollama version is 0.6.x. 

Step 3: Pull the model
ollama pull llama3.1:8b

⚠️ RAM requirement: llama3.1:8b needs ~8 GB RAM. If you have only 8 GB total system RAM, use the smaller model instead:

ollama pull llama3.2:3b

Then change model="llama3.1:8b" → model="llama3.2:3b" in the code. 

Step 4: Install Python dependencies
pip install langchain-ollama streamlit python-dotenv

Step 5: Run the app
streamlit run app.py

Your browser will open at http://localhost:8501 automatically.