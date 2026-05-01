# Panduan Setup Groq API untuk Chatbot

## Langkah-Langkah Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Konfigurasi API Key

Ada 2 cara untuk mengonfigurasi API key Groq:

#### **Cara 1: Menggunakan Streamlit Secrets (Recommended untuk Streamlit)**
File `.streamlit/secrets.toml` sudah tersedia di project ini.

Edit file tersebut dan ganti API key Anda:
```toml
groq_api_key = "gsk_YOUR_API_KEY_HERE"
```

Kemudian jalankan:
```bash
streamlit run app.py
```

#### **Cara 2: Menggunakan Environment Variable (Recommended untuk CLI)**
Untuk `main.py` atau penggunaan terminal:

**Linux/macOS:**
```bash
export GROQ_API_KEY="gsk_YOUR_API_KEY_HERE"
python main.py
```

**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=gsk_YOUR_API_KEY_HERE
python main.py
```

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="gsk_YOUR_API_KEY_HERE"
python main.py
```

### 3. Jalankan Chatbot

#### Streamlit UI:
```bash
streamlit run app.py
```

#### CLI Interface:
```bash
python main.py
```

## Fitur

✅ **Knowledge Base Lokal**: Menjawab pertanyaan dari data.json  
✅ **Groq AI Fallback**: Jika pertanyaan tidak ditemukan, AI akan menjawab  
✅ **Model**: Menggunakan Llama 3.3 70B (model Groq terbaru dan terbaik)  
✅ **Sistem**: "You are a learning chatbot that helps answer questions about technology"  

## Troubleshooting

### Error: "GROQ_API_KEY not found"
- Pastikan API key sudah dikonfigurasi dengan benar
- Untuk Streamlit: Cek `.streamlit/secrets.toml`
- Untuk CLI: Cek environment variable dengan `echo $GROQ_API_KEY` (macOS/Linux) atau `echo %GROQ_API_KEY%` (Windows)

### Error: "Invalid API Key"
- Cek API key Anda di https://console.groq.com
- Pastikan tidak ada spasi atau karakter ekstra

### Response Lambat
- Ini normal, Groq API memproses request secara real-time
- Check koneksi internet Anda

## API Key Tersedia
Groq menyediakan 10,000 token gratis per hari untuk development.

Dapatkan API key dari: https://console.groq.com/keys

## Security Notice
⚠️ **JANGAN** commit file `.streamlit/secrets.toml` ke Git jika repository publik!
File ini sudah ada di `.gitignore` tetapi pastikan untuk double-check.

## Dokumentasi Resmi
- Groq API: https://console.groq.com/docs
- Streamlit: https://docs.streamlit.io/
