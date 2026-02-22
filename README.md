🎓 Syllobot – AI Powered Syllabus-Aware Doubt Solver

Syllobot is an AI-powered student assistant that allows users to:

    📄 Upload PDFs and ask syllabus-based questions (RAG powered)
    
    🖼 Upload Images and automatically extract + solve questions using OCR
    
    💬 Ask manual questions based on uploaded study material
    
    🕐 View full history of uploads and AI responses
    
    Built using Flask, ChromaDB, Ollama, EasyOCR, and MySQL.

🚀 Features
    📄 PDF Based RAG System
    
    Extracts text from PDF using PyMuPDF
    
    Chunks and embeds content into ChromaDB
    
    Uses Retrieval-Augmented Generation (RAG)
    
    Answers strictly from uploaded document context

🖼 Image OCR AI

    Extracts text using EasyOCR
    
    Sends extracted question to a separate LLM model
    
    Also stores extracted text in vector database
    
    Allows further questioning from Ask section

💬 Ask Question Panel

    Ask follow-up questions
    
    Works for both:
    
    Uploaded PDFs
    
    Uploaded Images

🗂 History Page

    Stores:
    
    Questions
    
    Answers
    
    File name
    
    File type
    
    Timestamp
    
    Filtered per logged-in user

🏗 Architecture
    🔹 PDF Flow
    
    PDF → Text Extraction → Chunking → Embedding → ChromaDB → LLM (RAG)
    
    🔹 Image Flow
    
    Image → EasyOCR →
    
    Direct LLM Response
    
    Stored in ChromaDB for future RAG queries
    
    🔹 Manual Question Flow
    
    User Question → ChromaDB Retrieval → LLM → Answer

🛠 Tech Stack
    Backend
    
    Flask
    
    Ollama (Local LLM)
    
    ChromaDB (Vector DB)
    
    PyMuPDF
    
    EasyOCR
    
    OpenCV
    
    PyMySQL
    
    Database
    
    MySQL
    
    Frontend
    
    HTML
    
    CSS (Inline styling)
    
    Jinja2 templating

📂 Project Structure
    Hacknovation2.0/
    │
    ├── app.py
    ├── db/                  # ChromaDB storage
    ├── static/
    │   ├── files/           # Uploaded PDFs & Images
    │   └── images/
    ├── templates/
    │   ├── index.html
    │   ├── login.html
    │   ├── signup.html
    │   ├── dashboard.html
    │   └── history.html
    🗄 Database Setup
    
    Run the following SQL:
    
    DROP DATABASE IF EXISTS syllobot;
    CREATE DATABASE IF NOT EXISTS syllobot;
    USE syllobot;
    
    CREATE TABLE IF NOT EXISTS user_tb(
        fname VARCHAR(50),
        username VARCHAR(50),
        userpass VARCHAR(50),
        email VARCHAR(50)
    );
    
    CREATE TABLE IF NOT EXISTS user_dt (
        idx INT AUTO_INCREMENT PRIMARY KEY,
        user VARCHAR(50) NOT NULL,
        question TEXT NULL,
        answer TEXT NULL,
        file_name VARCHAR(100) NULL,
        file_type VARCHAR(50) NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ⚙ Installation
    1️⃣ Clone Repo
    git clone https://github.com/yourusername/syllobot.git
    cd syllobot
    2️⃣ Install Dependencies
    pip install flask
    pip install pymupdf
    pip install chromadb
    pip install nltk
    pip install pymysql
    pip install easyocr
    pip install opencv-python
    pip install ollama
    
    Download punkt tokenizer:
    
    import nltk
    nltk.download('punkt')
    🧠 Setup Ollama
    
    Install Ollama from:
    
    https://ollama.com/
    
    Pull models:
    
    ollama pull qwen2.5:0.5b
    
    (You can change model size if needed.)
    
    ▶ Run the App
    python app.py
    
    Open in browser:
    
    http://127.0.0.1:2000
    🔐 Authentication
    
    Signup new user
    
    Login required for:
    
    Upload
    
    Ask questions
    
    View history

💡 Future Improvements

    User-based vector isolation
    
    Role-based login (Admin / Student)
    
    Streaming responses
    
    Better chunking logic
    
    File preview in dashboard
    
    Math-specific model for equation solving

🎯 Use Cases

    College students
    
    Hackathon problem solvers
    
    Exam preparation
    
    Personalized AI tutor

👨‍💻 Author
K Vishal Kumar, 
Divya Ranjan Swain, 
Prachi Priyadarshini
Built for hackathon & intelligent doubt solving systems
