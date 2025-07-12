import os
import re
import pandas as pd
from sqlalchemy import create_engine
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import PGVector

#Set up variables
username = 'postgres'
password = 'postgres'
host = 'localhost'      
port = '5432'
database = 'postgres'

#Create connection string
connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_string)

# Load product table
df = pd.read_sql("SELECT * FROM product", con=engine)

#Clean the data
def clean_html(text):
    return re.sub(r'<.*?>', '', text)

df = df.fillna('NaN')
df['description'] = df['description'].apply(clean_html)

documents = [
    Document(page_content=row["description"], metadata={
        "id": row["id"], "name": row["name"], "category": row["type"], "price":row['price']
    }) for _, row in df.iterrows()
]

#Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=75, chunk_overlap=10)
chunks = splitter.split_documents(documents)

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = PGVector(
    collection_name="product_rag",
    connection_string=connection_string,
    embedding_function=embedding
)

# Upload chunks to pgvector
vectorstore.add_documents(chunks)
retriever = vectorstore.as_retriever()