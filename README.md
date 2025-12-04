# AI & LLMs Course Repository

This repository contains the code, notebooks, and supporting assets for a video course on modern AI and Large Language Models (LLMs).

Each `Lesson X` folder corresponds to a module in the course and contains runnable examples, notebooks, or scripts that illustrate the concepts from that module.

---

## Course Overview

1. **Orientation**  
2. **Natural Language Processing (NLP)**  
3. **Large Language Models (LLMs)**  
4. **Loss, Hyperparameters and Optimizers**  
5. **Training Strategies**  
6. **LLM Optimizations**  
7. **Inference and APIs**  
8. **Prompt Engineering**  
9. **Apps and RAG**  
10. **Evaluation & Observability**  
11. **Packaging and Deployment**  
12. **Responsible & Ethical**  

This repo focuses primarily on the hands-on parts of modules 4–12.

---

## Repository Structure

At the top level:

- `Lesson 4/` – Gradient descent and loss landscapes using PyTorch and Matplotlib.  
- `Lesson 5/` – Training strategies (regularization, learning rate schedules) in Jupyter notebooks.  
- `Lesson 6/` – LLM fine-tuning (before/after instruction fine-tuning) in notebooks.  
- `Lesson 7/` – Inference and APIs: OpenAI HTTP calls, FastAPI router, and AWS Bedrock + Streamlit chatbot.  
- `Lesson 8/` – Prompt engineering demos with Dolly and other prompting notebooks.  
- `Lesson 9/` – Apps and RAG: LangChain / LangServe backend and a Gradio UI client, plus RAG notebooks and vector indexes.  
- `Lesson 10/` – Evaluation & observability with LangSmith, LangChain agents, Chroma vector store, and Ollama-backed RAG.  
- `Lesson 11/` – Packaging and deployment (placeholder / course-specific assets).  
- `Lesson 12/` – Responsible & ethical AI: guardrails, bias & fairness, red-teaming and safety evaluation notebooks and data.  
- `requirements.txt` – Python dependencies for running the scripts and apps in this repo.  
- `venv/` – (Optional) A local virtual environment; you do **not** need to use this exact one.

---

## Environment Setup

You can use this repo with any recent Python 3.10+ environment.

### 1. Clone the repository

```bash
git clone <YOUR-REPO-URL>
cd Cognizant
```

### 2. Create and activate a virtual environment

It is strongly recommended to create a fresh virtual environment:

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\\Scripts\\Activate.ps1
```

If you already have a virtual environment (for example `venv/`), you can activate that instead.

### 3. Install dependencies with `requirements.txt`

This repo includes a `requirements.txt` file at the project root with conservative lower bounds:

```text
boto3>=1.28.0
chromadb>=0.5.0
fastapi>=0.110.0
gradio>=4.0.0
langchain>=0.2.0
langchain-community>=0.2.0
langchain-ollama>=0.1.0
langchain-text-splitters>=0.2.0
langserve>=0.2.0
langsmith>=0.1.0
matplotlib>=3.7.0
numpy>=1.24.0
pydantic>=2.0.3
python-dotenv>=1.0.0
requests>=2.31.0
streamlit>=1.30.0
torch>=2.0.0
uvicorn>=0.22.0
wikipedia>=1.4.0
```

Install everything with:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If you prefer fully reproducible environments, you can later replace these `>=` constraints with exact `==` pins based on your own `pip freeze` output.

---

## Lesson-by-Lesson Guide

### Lesson 4 – Loss, Hyperparameters and Optimizers

Folder: `Lesson 4/`

Key scripts (PyTorch + Matplotlib):

- `Gradient Descent.py` – Neural network trained with gradient descent, animated real-time visualization of the fit.  
- `Large Learning Rate.py` – Demonstrates instability / divergence with an overly large learning rate.  
- `Small Learning Rate.py` – Demonstrates slow convergence with a very small learning rate.  
- `Linear_Regression_Animated_Training.py` – Animated linear regression training showing gradient descent convergence over epochs.  

Run these scripts from the repo root (after activating your environment):

```bash
python "Lesson 4/Gradient Descent.py"
python "Lesson 4/Large Learning Rate.py"
python "Lesson 4/Small Learning Rate.py"
python "Lesson 4/Linear_Regression_Animated_Training.py"
```

These visuals support the module on loss surfaces, learning rates, and optimization dynamics.

---

### Lesson 5 – Training Strategies

Folder: `Lesson 5/`

Contains Jupyter notebooks covering training strategies such as regularization, learning rate schedules, and experiment tracking:

- `01_Training_strategies_fully_annotated.ipynb`  
- `02_Training_strategy_llm_regularization.ipynb`  
- `03_Training_Strategy_lr_schedule.ipynb`  
- `data/` – Supporting data files.  

Launch Jupyter (or VS Code / another notebook environment) and open the notebooks:

```bash
jupyter notebook
# then navigate to Lesson 5 and open the notebooks
```

---

### Lesson 6 – LLM Optimizations

Folder: `Lesson 6/`

Notebooks focused on instruction tuning and related LLM optimization strategies:

- `Before_Instruction_Fine_Tuning.ipynb`  
- `Instruction Fine-Tuning.ipynb`  

Open these in your notebook environment and follow along with the course videos.

---

### Lesson 7 – Inference and APIs

Folder: `Lesson 7/`

This lesson demonstrates several ways to work with LLMs via APIs:

- `OpenAI API Scripts/openAI API with python.py`  
  - Minimal example calling the OpenAI Chat Completions API via `requests` using the `OPENAI_API_KEY` environment variable.

- `FastAPI/openai_fastapi_router.py`  
  - A FastAPI application that proxies and rate-limits OpenAI chat completions.  
  - Includes non-streaming and streaming endpoints, simple usage tracking, and admin endpoints.

- `AWS Bedrock/Bedrock Chatbot.py`  
  - Streamlit chatbot UI powered by an AWS Bedrock-hosted Mistral model via `langchain_community.llms.Bedrock`.

#### Running the FastAPI router

From the repo root (after installing dependencies and setting `OPENAI_API_KEY`):

```bash
export OPENAI_API_KEY=...    # macOS / Linux
# setx / PowerShell equivalent on Windows

python "Lesson 7/FastAPI/openai_fastapi_router.py"
# or with uvicorn directly:
# uvicorn "Lesson 7.FastAPI.openai_fastapi_router:app" --reload --port 8000
```

#### Running the Bedrock Streamlit app

You need AWS credentials configured (profile, region, and Bedrock access):

```bash
export AWS_PROFILE=your-profile
streamlit run "Lesson 7/AWS Bedrock/Bedrock Chatbot.py"
```

---

### Lesson 8 – Prompt Engineering

Folder: `Lesson 8/`

Prompting demos using Dolly and other patterns:

- `01_Dolly_prompting.ipynb`  
- `Prompting_Demo2.ipynb`  
- `Prompting_Demo3.ipynb`  

Open these notebooks to explore different prompting strategies and techniques discussed in the course.

---

### Lesson 9 – Apps and RAG

Folder: `Lesson 9/`

RAG (Retrieval-Augmented Generation) examples using LangChain, vector indexes, and a simple UI.

Key pieces:

- Notebooks:
  - `01_RAG_Demo.ipynb`  
  - `02_Demo_Notebook.ipynb`  
  - `03_LlamaIndex_RAG_Demo.ipynb`  

- Backend:
  - `server.py` – FastAPI app using `langserve` to expose a (mock) RAG chain at `/rag`.  
  - `env_check.py` – Utility script to print LangSmith-related environment variables.

- Frontend:
  - `ui.py` – Minimal Gradio client that sends questions to the `/rag` endpoint and displays answers + sources.

- Vector indexes and data:
  - `index-faiss/`, `index_demo/` – Stored indexes used in the notebooks.

#### Running the RAG server and UI

From the repo root:

```bash
# Start the FastAPI/LangServe backend
uvicorn "Lesson 9.server:app" --reload --port 8000

# In another terminal, launch the Gradio UI
python "Lesson 9/ui.py"
```

Open the Gradio URL printed in the terminal to interact with the RAG app.

---

### Lesson 10 – Evaluation & Observability

Folder: `Lesson 10/`

Focuses on LangSmith-based tracing and feedback, LangChain agents, and local RAG with Ollama.

Key files:

- `LangSmith_Feedback.py` – Main script that:
  - Loads environment variables via `python-dotenv`.
  - Configures LangSmith tracing and project settings.  
  - Builds a Chroma vector store from `Noclimate.txt` using `OllamaEmbeddings`.  
  - Creates a `RetrievalQA` chain and wraps it in a ReAct-style agent with tools (local doc + Wikipedia).  
  - Runs an example query, then prompts you for a 1–5 rating and logs feedback to LangSmith.

- `Noclimate.txt` – Example document for the local RAG tool.  
- `lc_agent_chroma/` – Persisted Chroma vector store directory.

To run (after configuring LangSmith and Ollama):

```bash
# Set LangSmith variables (or put them in a .env file)
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
export LANGCHAIN_API_KEY=...
export LANGCHAIN_PROJECT="Agentic Tracing"

# Ensure Ollama and the required models are available locally
python "Lesson 10/LangSmith_Feedback.py"
```

---

### Lesson 11 – Packaging and Deployment

Folder: `Lesson 11/`

Contains course-specific assets (for example, deployment notes or stubs).  

- `Readme.md` – Placeholder / lesson-specific notes for packaging and deployment, which you can adapt as needed.

---

### Lesson 12 – Responsible & Ethical AI

Folder: `Lesson 12/`

Notebooks and data focused on guardrails, bias/fairness, and safety evaluation:

- `01_guardrail_demo.ipynb`  
- `02_bias_fairness_demo.ipynb`  
- `03-Safety_evaluation.ipynb`  
- `04_redteam_demo.ipynb`  
- `data/` – Supporting CSVs and configuration files (`demo01_triage_results.csv`, `redteam_report.csv`, `safety_eval_log.csv`, `seeds.yaml`, etc.).  
- `Modelfile` – Example configuration file related to model setup for safety/red-teaming scenarios.

Open these notebooks to follow along with the responsible AI and safety-focused parts of the course.

---

## Tips for Using This Repo with the Course

- Always **activate your virtual environment** before running notebooks or scripts.  
- Some lessons rely on **external services** (OpenAI, AWS Bedrock, LangSmith, Ollama); make sure the required environment variables and credentials are set before running those parts.  
- Start with the video for each module, then open the corresponding `Lesson X` folder and run the scripts/notebooks shown in the video.  
- If you run into dependency issues, check `requirements.txt` first, then verify your Python version and virtual environment.

Happy learning and experimenting with AI and LLMs!
