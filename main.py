import os
import io
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List

# These imports are for local file access
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

load_dotenv()

# --- Configuration & Setup ---
API_BEARER_TOKEN = os.getenv("API_BEARER_TOKEN", "932d887435ea59d029c2e1a6844a0590c534c3601c926ebf8847bdf605474a0d")
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY is not set. Please add it to your .env file.")

# --- API Authentication ---
security = HTTPBearer()
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme != "Bearer" or credentials.credentials != API_BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token"
        )
    return credentials

# --- Pydantic Models ---
class QueryRequest(BaseModel):
    # The 'documents' field is now optional as we use a local file,
    # but we keep it for API compatibility with the hackathon platform.
    documents: str | None = None 
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

# --- FastAPI App ---
app = FastAPI(title="Intelligent Query–Retrieval System (Google Gemini)")

# --- Core Logic ---
# Load the document and create the RAG chain ONCE at startup
# This is much more efficient than reloading for every request.
PDF_PATH = "policy.pdf"
if not os.path.exists(PDF_PATH):
    raise FileNotFoundError(f"{PDF_PATH} not found. Please add it to your project directory.")

loader = PyPDFLoader(PDF_PATH)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = text_splitter.split_documents(documents)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = FAISS.from_documents(docs, embeddings)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever()
)

# --- API Endpoint ---
@app.post(
    "/api/v1/hackrx/run",
    response_model=QueryResponse,
    dependencies=[Depends(verify_token)]
)
async def run_submission(request: QueryRequest):
    """
    This endpoint processes questions against a pre-loaded policy document.
    """
    try:
        answers = []
        for question in request.questions:
            result = qa_chain.invoke({"query": question})
            answers.append(result["result"])
        return {"answers": answers}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/", include_in_schema=False)
def root():
    return {"message": "API is running. See /docs for documentation."}