# Deploy ke Streamlit Cloud (Free Tier)

## ⚠️ Batasan Streamlit Cloud Free
- **Memory**: ~1GB
- **CPU**: Shared
- **Storage**: Limited disk
- **Timeout**: 24 jam inactivity
- **Concurrent users**: 1 (free tier)

## 🔧 Setup untuk Deploy

### 1. Persiapan Files
```bash
# Pastikan .gitignore sudah ada
cat .gitignore  # Harus exclude: Referensi/, vectorstore/, *.pdf

# Hapus file besar sebelum push
rm -rf Referensi/
rm -rf htmlcov/
# JANGAN hapus vectorstore/ - buat di cloud atau upload lightweight version
```

### 2. Update requirements.txt
```bash
# Gunakan requirements-cloud.txt untuk cloud
cat requirements-cloud.txt
```

Perbedaan utama:
- ❌ Hapus: `fastembed` (berat, 200MB+)
- ✅ Ganti dengan: `sentence-transformers` (lebih ringan)
- ✅ Buang: `langchain-huggingface` (tidak perlu jika pakai groq)

### 3. Setup Git & Push
```bash
git init
git add .
git config user.email "you@example.com"
git config user.name "Your Name"
git commit -m "Initial commit - Streamlit Cloud ready"
git remote add origin https://github.com/yourusername/chatbot.git
git branch -M main
git push -u origin main
```

### 4. Deploy ke Streamlit Cloud
1. Buka https://share.streamlit.io/
2. Click "New app"
3. Pilih repository, branch=main, main file=app.py
4. Deploy

### 5. Tambah Secrets di Streamlit Cloud
Dashboard → Settings → Secrets
```toml
groq_api_key = "gsk_your_key_here"
```

## 📊 Optimasi Memory

### Jika masih OOM (Out of Memory):

#### Opsi A: Lazy Load Vectorstore
```python
# Di responses.py, ubah ini:
@st.cache_resource
def load_vectorstore():
    # Load only when needed, not at startup
    try:
        from langchain_community.vectorstores import FAISS
        return FAISS.load_local("vectorstore", ...)
    except:
        return None
```

#### Opsi B: Cloud Vectorstore
Alih ke cloud vectorstore (hemat disk):
- **Pinecone** (free tier: 100K vectors)
- **Weaviate Cloud** (free tier available)
- **Supabase pgvector** (PostgreSQL with embeddings)

#### Opsi C: Reduce Vectorstore Size
```bash
# Compress vectorstore
cd vectorstore
zip -r vectorstore_compressed.zip *
# Kemudian extract di cloud
```

## 🚀 Tips Performa

1. **Cache aggressively**
   ```python
   @st.cache_resource
   def load_vectorstore():
       # Load sekali aja
       
   @st.cache_data(ttl=3600)
   def search_documents(query):
       # Cache hasil search 1 jam
   ```

2. **Lazy imports**
   ```python
   # Jangan import di top level, import saat diperlukan
   from langchain_community.vectorstores import FAISS  # Import inside function
   ```

3. **Monitoring**
   - Check Streamlit Cloud logs untuk OOM errors
   - Monitor app runtime dengan `time` metrics

## 📦 Alternatif: Deploy Lokal dengan Ngrok

Jika Streamlit Cloud tidak cukup:
```bash
pip install pyngrok
streamlit run app.py &
ngrok http 8501
```
Dapatkan public URL dari Ngrok

## ⚡ Checklist Sebelum Deploy
- [ ] `.gitignore` exclude: `Referensi/`, `*.pdf`, `htmlcov/`
- [ ] `requirements-cloud.txt` tanpa dependencies berat
- [ ] `.streamlit/secrets.toml` di `.gitignore` (tidak di-commit)
- [ ] Git repository public
- [ ] Groq API key sudah ada
- [ ] Test locally: `streamlit run app.py`
- [ ] Push ke GitHub
