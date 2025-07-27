# 🧠 Intelligent Query–Retrieval System
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-RAG-yellow?logo=chainlink)
![Google-Gemini](https://img.shields.io/badge/Gemini-1.5--flash-ffca28?logo=google)
![FAISS](https://img.shields.io/badge/FAISS-VectorStore-9cf?logo=data)
![Gunicorn](https://img.shields.io/badge/Gunicorn-Server-009688?logo=gunicorn)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-121212?logo=uvicorn&logoColor=white)

This project is an intelligent query–retrieval system powered by **RAG (Retrieval-Augmented Generation)** and **LLMs**. It allows users to ask natural language questions and receive highly accurate answers based solely on the content of a given PDF document. Ideal for automating document comprehension, the system transforms any policy, guideline, or manual into a smart, searchable knowledge base.

---

## 🚀 How It Works

The system implements a **Retrieval-Augmented Generation (RAG)** pipeline to ensure accurate and contextually-aware responses:

1. **Document Loading**: Loads a source PDF document (`policy.pdf`) from the local directory at startup.
2. **Indexing**: Splits the document into smaller chunks, converts them into embeddings using Google's Generative AI, and stores them in an in-memory FAISS vector store.
3. **Retrieval**: Searches the FAISS index for the most relevant chunks when a question is asked.
4. **Generation**: Feeds the question and relevant chunks to the Gemini model to generate a precise answer strictly based on the document.

---

## 🧰 Tech Stack

- **Backend**: FastAPI  
- **Language**: Python  
- **LLM**: Google Gemini (`gemini-1.5-flash-latest`)  
- **Embeddings & Vector Store**: Google Generative AI Embeddings + FAISS  
- **Core Library**: LangChain  
- **Production Server**: Gunicorn + Uvicorn workers  

---

## ✨ Key Features

- 📄 Converts PDF into a searchable knowledge base  
- 💬 Natural language Q&A with high accuracy  
- 🚫 Minimizes hallucinations via RAG pipeline  
- 🔐 Secure API endpoint using Bearer Token  
- ⚡ Preloads document and vector index at startup  

---

## 🔌 API Endpoint

### `POST /api/v1/hackrx/run`

Processes a list of natural language questions and returns precise answers based on `policy.pdf`.

---

### 🔐 Authentication

```http
Authorization: Bearer <your_token>
```

---

## 📥 Request Body Example

``` json
{
  "documents": "http://localhost:8001/policy.pdf",
  "questions": [
    "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
    "What is the waiting period for pre-existing diseases (PED) to be covered?",
    "Does this policy cover maternity expenses, and what are the conditions?",
    "What is the waiting period for cataract surgery?",
    "Are the medical expenses for an organ donor covered under this policy?",
    "What is the No Claim Discount (NCD) offered in this policy?",
    "Is there a benefit for preventive health check-ups?",
    "How does the policy define a 'Hospital'?",
    "What is the extent of coverage for AYUSH treatments?",
    "Are there any sub-limits on room rent and ICU charges for Plan A?"
  ]
}
```

---

## ✅ Success Response Example (200 OK)

```
{
  "answers": [
    "The provided text states that if the insured person has opted for installment payments (half-yearly, quarterly, or monthly), there is a 15-day grace period to pay the installment premium.  During this grace period, coverage is not available.  If the payment isn't received within the grace period, the policy is cancelled.",
    "The waiting period for pre-existing diseases (PED) is 36 months of continuous coverage after the date of inception of the first policy with the insurer.  This waiting period can be reduced if the insured has continuous coverage without a break, as defined by IRDAI portability regulations.",
    "No, this policy does not cover expenses related to pregnancy, childbirth, or their consequences.",
    "The provided text does not specify a waiting period for cataract surgery.  While cataract surgery is listed as a covered procedure (item 6), there's no mention of a waiting period associated with it.",
    "Yes, but only under specific conditions.  The policy covers medical expenses incurred by an organ donor during hospitalization for organ harvesting for the insured person, provided the donation conforms to the Transplantation of Human Organs Act 1994, the expenses are reasonable and customary charges, and the claim is subject to the annual sum insured limit.  Importantly, pre- and post-hospitalization expenses, screening expenses, other medical expenses resulting from harvesting, and costs associated with organ acquisition (other than hospitalization costs) are excluded.",
    "I'm sorry, but this document does not contain information about a No Claim Discount (NCD).",
    "Yes, there is a benefit for preventive health check-ups.  The specifics depend on the policy variant and whether it's an individual or family floater policy.  The benefit is available once per year per insured person on a cashless basis, using a pre-defined package at network providers.  For long-term policies (2 or 3 years), all policy years' check-ups are provided at the start of the first year.  There are also additional benefits available after a certain number of claim-free years.",
    "The policy defines a Hospital as any institution established for inpatient care and day care treatment of illness and/or injuries, registered as a hospital with local authorities under the Clinical Establishments (Registration and Regulation) Act, 2010, or under enactments specified in Section 56(1) of that Act, or meeting specific minimum criteria.  These criteria include having qualified nursing staff and medical practitioners on-site 24/7, a minimum number of inpatient beds (10 or 15 depending on location), a fully equipped operating theatre, and maintaining accessible daily patient records.",
    "The provided text states that coverage for AYUSH treatments will cover Medical Expenses incurred during the Policy Period up to the Annual Sum Insured specified in the Policy Schedule.  This is provided that the expenses are reasonable and customary charges, the treatment occurs at an AYUSH hospital or day-care center, hospitalization commences and continues on the advice of a medical practitioner, and the total expenses don't exceed the annual sum insured.",
    "The provided text states that if a room/ICU accommodation is chosen where the room rent or category is higher than the eligible limit for the insured person, the associated medical expenses will be pro-rated according to the applicable limits.  However, the specific limits for Plan A are not included in this text."
  ]
}
```

---

## 🧪 Running Locally
Follow these steps to run the project locally:

### 1. Clone the Repository
``` bash
git clone https://github.com/PriyanshuSingh44/Hackathon.git
cd Hackathon
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory and add your Google API key:
```bash
GOOGLE_API_KEY="your_google_api_key_here"
```

### 3. Install Dependencies
``` bash
pip install -r requirements.txt
```

### 4. Run the Development Server
``` bash
uvicorn main:app --reload
```
Visit: [http://localhost:8000](http://localhost:8000)

---

# ☁️ Deployment
To launch a production-ready server, use the following command:
``` bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```
This application is ready for deployment on cloud platforms like Render, Railway, Fly.io, etc.

---

## 🌐 Live Preview

[![Live Preview](https://img.shields.io/badge/Live%20Preview-Open-blue?style=for-the-badge)](https://hackrx-submission.onrender.com)
(Refresh once if not loaded correclty) 