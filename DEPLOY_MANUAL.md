# 🚀 Panduan Deploy Streamlit Cloud - Step by Step Visual

## 📌 Status Saat Ini
✅ Code sudah di GitHub: https://github.com/delsikariman/chatbot_new
✅ Optimasi sudah dilakukan
⏳ Tinggal deploy ke Streamlit Cloud

---

## 🎯 Step 1: Buka Streamlit Cloud
**URL**: https://share.streamlit.io/

Klik tombol **"Sign in with GitHub"** atau **"Continue with GitHub"**

---

## 🎯 Step 2: Login GitHub
- Masukkan GitHub username: `delsikariman`
- Masukkan GitHub password
- Authorize Streamlit Cloud untuk akses ke repository

---

## 🎯 Step 3: Klik "New app" (Tombol Biru)
Di dashboard Streamlit Cloud, cari tombol **"New app"** berwarna biru di sudut kanan atas.

---

## 🎯 Step 4: Isi Form Deploy

Isi field-field ini:

```
📦 Repository URL (atau pilih dari dropdown):
   delsikariman/chatbot_new

🌿 Branch:
   main

📄 Main file path:
   app.py
```

**Contoh form:**
```
┌─────────────────────────────────────┐
│ Repository                          │
│ delsikariman/chatbot_new      ▼     │
├─────────────────────────────────────┤
│ Branch                              │
│ main                          ▼     │
├─────────────────────────────────────┤
│ Main file path                      │
│ app.py                              │
└─────────────────────────────────────┘
```

---

## 🎯 Step 5: PENTING - Advanced Settings ⚠️

**JANGAN lewatkan step ini!**

1. Scroll ke bawah, cari: **"Advanced settings"**
2. Klik untuk membuka

### Di Advanced Settings:
```
Python version: 
  → Pilih 3.9 atau 3.10 (atau biarkan auto)

Secrets:
  → Kosongkan (akan diisi di dashboard nanti)

Secret files:
  → Kosongkan

Requirements file:
  → UBAH dari "requirements.txt" menjadi "requirements-cloud.txt"
  
  ✅ Ini PENTING untuk menghemat memory!
```

---

## 🎯 Step 6: Deploy!
Klik tombol **"Deploy"** berwarna biru di bawah

**⏳ Tunggu 2-3 menit untuk deployment...**

Anda akan melihat:
- "Building..." (kuning)
- "Running..." (hijau) ← Deploy selesai!

---

## 🎯 Step 7: Tambah Groq API Key (SANGAT PENTING!)

Setelah app sudah "Running", ikuti langkah ini:

1. **Klik hamburger menu** (☰) di **kanan atas app**
2. Pilih **"Settings"**
3. Klik tab **"Secrets"**
4. **Paste ini di text area:**

```toml
groq_api_key = "gsk_your_actual_key_here"
```

**Ganti `gsk_your_actual_key_here` dengan API key Groq Anda yang sebenarnya**
(Contoh: `gsk_xEwPq2nRj7sK9vB3mL8dC`)

5. Klik **"Save"**
6. App akan **auto-reboot** (mungkin perlu 1-2 menit)

---

## ✅ Selesai! App Sudah Deployed!

Anda akan dapat URL seperti:
```
https://chatbot-delsikariman.streamlit.app/
```

Buka URL ini di browser untuk test chatbot! 🎉

---

## 🧪 Testing Setelah Deploy

1. **Buka app** dari URL yang diberikan
2. **Tunggu loading** (first load mungkin lambat)
3. **Test dengan pertanyaan sederhana**, contoh:
   - "Halo"
   - "Apa itu AI?"
   - "Jelaskan machine learning"

### Jika berjalan lancar:
✅ Chat berfungsi
✅ Groq API terhubung
✅ App siap digunakan!

### Jika error:
- Check **App logs** (menu hamburger → Logs)
- Common issues di bagian troubleshooting di bawah

---

## 🔗 Links Penting

| Link | Keterangan |
|------|-----------|
| https://share.streamlit.io/ | Streamlit Cloud Dashboard |
| https://github.com/delsikariman/chatbot_new | Repository Code |
| https://console.groq.com | Groq API Console (cek API key) |
| https://chatbot-delsikariman.streamlit.app/ | URL App Anda (setelah deploy) |

---

## 🐛 Troubleshooting

### ❌ "App crashed" atau "Error loading app"

**Check logs:**
1. Dashboard → pilih app Anda
2. Klik "View logs"
3. Cari error message

**Common fixes:**
- Pastikan `requirements-cloud.txt` digunakan
- Pastikan `app.py` di repo
- Pastikan Groq API key di Secrets

### ❌ "OOM" atau "Out of Memory"

Berarti app terlalu besar untuk free tier. Solusi:
1. Disable RAG: Edit `app.py` set `use_rag = False`
2. Atau gunakan cloud vectorstore (Pinecone)
3. Push update → app auto-update

### ❌ "API Key not found"

Pastikan sudah add API key di **Secrets**:
- Menu hamburger (☰) → Settings → Secrets
- Paste: `groq_api_key = "gsk_..."`
- Save & reboot app

### ❌ Vectorstore tidak load

Normal! Jika first query lambat:
- ✅ Biarkan, sedang load vectorstore ke memory
- Query ke-2 akan jauh lebih cepat (cached)
- Jika tetap error, check console logs

---

## ℹ️ Info Penting

### Batasan Free Tier Streamlit Cloud:
- 💾 Memory: ~1GB
- ⏰ Timeout: 24 jam (auto sleep jika tidak dipakai)
- 👥 Concurrent users: 1 (free tier)
- 🌐 Shared resources

### Kapan app re-deploy otomatis:
- ⚙️ Setiap push ke GitHub (otomatis)
- 🔧 Update settings (manual reboot)
- 🐛 Crash recovery (otomatis)

### Monitoring:
- Dashboard → Logs: lihat error/warning
- Developer info: lihat performance metrics
- Sharing: generate public link

---

## 📝 Checklist Final

Sebelum deploy:
- [ ] Buka https://share.streamlit.io/
- [ ] Login dengan GitHub (delsikariman)
- [ ] Klik "New app"
- [ ] Repository: `delsikariman/chatbot_new`
- [ ] Branch: `main`
- [ ] Main file: `app.py`
- [ ] **Advanced Settings:**
  - [ ] Requirements file: `requirements-cloud.txt`
- [ ] Klik "Deploy"
- [ ] Tunggu sampai "Running" (hijau)
- [ ] Tambah Groq API key di Secrets
- [ ] Test app

---

## 🎉 Done!

Your AI chatbot is now **LIVE** on the internet! 🚀

Share dengan teman, dosen, atau pengguna lain!

```
https://chatbot-delsikariman.streamlit.app/
```

---

**Butuh bantuan? Ada error?** Beri tahu saya error message-nya! 💬
