import os
import requests
from llama_cpp import Llama

llm = Llama.from_pretrained(
	repo_id="modularai/Llama-3.1-8B-Instruct-GGUF",
	filename="llama-3.1-8b-instruct-q6_k.gguf",
    n_ctx=4096,   
    n_batch=512 
)

def query_llama(prompt: str) -> str:
    results = llm(prompt, max_tokens=512)
    return results["choices"][0]["text"]