from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
import uuid

class Question(BaseModel):
    question: str


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres"
    )

app = FastAPI()

from rag_model import retriever
from llm_model import query_llama

@app.post("/api/v1/messaging/chatbot")
def query_rag(data: Question):
    docs = retriever.get_relevant_documents(data.question)
    context = "\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are a helpful assistant. Use the following context to answer.


Context:
{context}

Question:
{data.question}
"""

    answer = query_llama(prompt)
    print(answer)
    return {"answer": answer}