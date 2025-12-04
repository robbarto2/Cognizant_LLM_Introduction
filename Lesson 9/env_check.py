# env_check.py — optional: confirm LangSmith env vars are visible
import os
print("LANGCHAIN_TRACING_V2:", os.getenv("LANGCHAIN_TRACING_V2"))
print("LANGCHAIN_PROJECT   :", os.getenv("LANGCHAIN_PROJECT"))
