# 💬 Chatbot AI Pembelajaran

Chatbot interaktif berbasis **Groq AI** dengan **RAG (Retrieval Augmented Generation)** untuk menjawab pertanyaan tentang Artificial Intelligence, Machine Learning, dan teknologi terkait berdasarkan materi Rencana Pembelajaran Semester (RPS).

## ✨ Fitur Utama

- 🤖 **AI Groq Integration**: Menggunakan model LLaMA 3.3 70B untuk respons berkualitas tinggi
- 📚 **RAG System**: Menjawab pertanyaan berdasarkan referensi materi PDF
- 🎨 **Streamlit UI**: Interface yang user-friendly dan responsif
- ⚡ **Caching**: Response caching untuk performa optimal
- 📊 **FAISS Vector Store**: Pencarian semantik cepat pada dokumen
- 🧪 **Testing Suite**: Unit tests dengan pytest
- 📝 **Knowledge Base**: Dukungan data.json dan PDF files

## 🚀 Quick Start

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Setup Groq API Key

Dapatkan API key gratis di [console.groq.com](https://console.groq.com)

**Option A: Streamlit Secrets (Recommended untuk UI)**
```bash
# Edit file .streamlit/secrets.toml
groq_api_key = "gsk_YOUR_API_KEY_HERE"
```

**Option B: Environment Variable (untuk CLI)**
```bash
# macOS/Linux
export GROQ_API_KEY="gsk_YOUR_API_KEY_HERE"

# Windows (PowerShell)
$env:GROQ_API_KEY="gsk_YOUR_API_KEY_HERE"
```

### 3️⃣ Jalankan Chatbot
```bash
streamlit run app.py
```

Aplikasi akan terbuka di `http://localhost:8501`

---

## 📁 Struktur Project

```
chatbot_new/
├── app.py                      # 🎨 Streamlit UI utama
├── main.py                     # 🖥️ CLI interface
├── config.py                   # ⚙️ Konfigurasi terpusat
├── responses.py                # 🤖 Logika AI & RAG
├── ingest.py                   # 📄 PDF ingestion & vectorstore
│
├── test_chatbot.py            # ✅ Unit tests chatbot
├── test_groq.py               # ✅ Unit tests Groq integration
├── conftest.py                # 🧪 Pytest configuration
├── pytest.ini                 # 🧪 Pytest settings
│
├── Referensi/                 # 📚 Folder untuk PDF referensi
├── vectorstore/               # 🗂️ FAISS vector store (generated)
│   └── index.faiss
│
├── .streamlit/                # 🔐 Streamlit config
│   └── secrets.toml
├── data.json                  # 📋 Knowledge base JSON
├── rps_extracted.txt          # 📄 RPS text extract
│
├── requirements.txt           # 📦 Dependencies
├── requirements-dev.txt       # 📦 Dev dependencies
├── SETUP_GROQ.md             # 📖 Groq setup guide
├── README.md                  # 📖 Dokumentasi (file ini)
│
└── htmlcov/                   # 📊 Coverage report (generated)
```

---

## ⚙️ Konfigurasi

Semua setting terpusat di **`config.py`**:

```python
# Model & API
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_MAX_TOKENS = 1024
GROQ_TIMEOUT = 30

# Vector Store
K_SEARCH = 4  # Docs to retrieve
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Cache
RESPONSE_CACHE_ENABLED = True
RESPONSE_CACHE_TTL = 3600  # 1 hour

# Knowledge Base
DATA_JSON_PATH = "data.json"
PDF_FOLDER_PATH = "Referensi"
```

---

## 📖 Cara Menggunakan

### 🎯 Menggunakan Streamlit UI
```bash
streamlit run app.py
```
- Ketik pertanyaan di chat input
- Klik tombol "Hapus Percakapan" untuk reset
- Toggle "Gunakan Groq AI" untuk on/off AI

### 💻 Menggunakan CLI
```bash
export GROQ_API_KEY="gsk_..."
python main.py
```

### 📚 Menambah Referensi PDF
1. Letakkan file PDF di folder `Referensi/`
2. Jalankan ingestion:
```bash
python ingest.py
```
3. Vector store akan di-generate di `vectorstore/`

### 🔄 Update Knowledge Base
Edit `data.json` atau tambah PDF, kemudian jalankan ingestion ulang.

---

## 🧪 Testing

### Jalankan Semua Tests
```bash
pytest
```

### Tests dengan Coverage Report
```bash
pytest --cov=. --cov-report=html
# Buka htmlcov/index.html
```

### Run Specific Test
```bash
pytest test_chatbot.py -v
pytest test_groq.py -v
```

---

## 🔧 Development Setup

### Install Dev Dependencies
```bash
pip install -r requirements-dev.txt
```

### Struktur Kode
- **`app.py`**: Streamlit UI - chat interface, session management
- **`main.py`**: CLI interface - untuk testing di terminal
- **`responses.py`**: Core logic - RAG, Groq calls, caching
- **`ingest.py`**: PDF processing - chunking, vectorstore creation
- **`config.py`**: Centralized configuration
- **`verify_setup.py`**: Check environment & dependencies
- **`verify_rag.py`**: Test RAG pipeline

---

## 🐛 Troubleshooting

### ❌ "GROQ API Key TIDAK DITEMUKAN"
```bash
# Linux/macOS
export GROQ_API_KEY="gsk_YOUR_KEY"

# Windows PowerShell
$env:GROQ_API_KEY="gsk_YOUR_KEY"

# Verify
echo $GROQ_API_KEY
```

### ❌ ".streamlit/secrets.toml" tidak ditemukan
```bash
mkdir -p .streamlit
cat > .streamlit/secrets.toml << 'EOF'
groq_api_key = "gsk_YOUR_KEY"
EOF
```

### ❌ "ModuleNotFoundError"
```bash
pip install --upgrade -r requirements.txt
```

### ❌ FAISS vectorstore tidak ditemukan
```bash
# Generate ulang dari PDF
python ingest.py
```

### ❌ Performance lambat
- Cek `RESPONSE_CACHE_TTL` di `config.py`
- Tingkatkan `K_SEARCH` untuk hasil lebih relevan
- Monitor dengan logs: `LOG_LEVEL = "DEBUG"`

---

## 🛠️ Utility Scripts

### Verifikasi Setup
```bash
python verify_setup.py
```
Check Python version, dependencies, API key, PDF folder, vectorstore.

### Verifikasi RAG Pipeline
```bash
python verify_rag.py
```
Test document retrieval & response generation.

### List Available Groq Models
```bash
python list_groq_models.py
```

### Check Configuration
```bash
python check_config.py
```

---

## 📊 Workflow Overview

```
User Input
    ↓
[Streamlit UI atau CLI]
    ↓
[Validation] → Check input length, format
    ↓
[Response Cache Check] → Jika ada cached response, return langsung
    ↓
[RAG Retrieval] → Search relevant docs dari vectorstore
    ↓
[System Prompt + Context] → Combine context dengan question
    ↓
[Groq API Call] → Generate response dengan LLaMA model
    ↓
[Cache Response] → Save untuk request serupa di masa depan
    ↓
[Display Output] → Render di UI atau print di CLI
```

---

## 🎯 Next Steps / Improvements

- [ ] Streaming responses dari Groq
- [ ] Search history / sidebar dengan recent queries
- [ ] Response quality metrics & logging
- [ ] Dark mode support
- [ ] Multi-language support
- [ ] Docker containerization
- [ ] Database backend untuk query history
- [ ] Fine-tuned system prompts per topik

---

## 📝 Lisensi

Project ini dibuat untuk tujuan pembelajaran.

---

## 📧 Support

Untuk setup Groq API, lihat [SETUP_GROQ.md](SETUP_GROQ.md)

**Dokumentasi Groq**: https://console.groq.com/docs

**LangChain Docs**: https://python.langchain.com/

---

**Happy Chatting! 🚀**
