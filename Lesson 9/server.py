# server.py — expose your chain via LangServe/FastAPI
from fastapi import FastAPI
from langserve import add_routes

# NOTE: replace this stub with your real LCEL chain object named `chain`.
# For demo purposes, we mock the same contract.
class MockChain:
    def invoke(self, inp):
        q = (inp or {}).get("question", "")
        return {"answer": f"(mock) You asked: {q}", "sources": []}

chain = MockChain()

app = FastAPI(title="Module9 RAG")
add_routes(app, chain, path="/rag")

# Run in a terminal:
# uvicorn server:app --reload --port 8000
