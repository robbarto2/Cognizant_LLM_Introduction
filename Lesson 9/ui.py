# ui.py — minimal Gradio client for the /rag endpoint
import gradio as gr, requests

API = "http://localhost:8000/rag/invoke"

def ask(q):
    try:
        r = requests.post(API, json={"input": {"question": q}}, timeout=10).json()
        out = r.get("output", {})
        ans = out.get("answer", "(no answer)")
        chips = " ".join(f"[{s}]" for s in out.get("sources", []))
        return f"{ans}\n\nSources: {chips}"
    except Exception as e:
        return f"Error: {e}"

gr.ChatInterface(ask, title="Module 9 — RAG Chat (Mock)").launch()
