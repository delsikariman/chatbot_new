import streamlit as st
import os
from responses import respon_ai

st.set_page_config(
    page_title="Chatbot Pembelajaran",
    page_icon="💬",
    layout="centered"
)

st.title("Chatbot Pembelajaran")
st.caption("Chatbot dengan AI berbasis Groq")

# Setup API key dari Streamlit secrets
if "groq_api_key" not in st.session_state:
    try:
        # Coba ambil dari Streamlit secrets
        if "groq_api_key" in st.secrets:
            st.session_state.groq_api_key = st.secrets["groq_api_key"]
            os.environ["GROQ_API_KEY"] = st.secrets["groq_api_key"]
        else:
            st.session_state.groq_api_key = None
    except:
        st.session_state.groq_api_key = None

# Tampilkan peringatan jika API key tidak tersedia
if not st.session_state.groq_api_key and not os.getenv("GROQ_API_KEY"):
    st.warning(
        "⚠️ GROQ API Key belum dikonfigurasi. "
        "Chatbot hanya akan menggunakan basis pengetahuan lokal.\n\n"
        "Untuk mengaktifkan AI Groq:\n"
        "1. Buat file `.streamlit/secrets.toml` di folder project\n"
        "2. Tambahkan: `groq_api_key = 'gsk_....'`\n"
        "3. Restart aplikasi Streamlit"
    )

# Inisialisasi session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tombol reset
col1, col2 = st.columns(2)
with col1:
    if st.button("Hapus Percakapan", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

with col2:
    use_groq = st.checkbox("Gunakan Groq AI", value=True, disabled=not (st.session_state.groq_api_key or os.getenv("GROQ_API_KEY")))

# Tampilkan seluruh riwayat percakapan
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input chat
prompt = st.chat_input("Masukkan pertanyaan Anda...")

if prompt:
    # Tampilkan pertanyaan pengguna
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses jawaban
    with st.chat_message("assistant"):
        with st.spinner("Memproses..."):
            response = respon_ai(prompt, use_groq=use_groq)
        st.markdown(response)
    
    # Simpan jawaban bot
    st.session_state.messages.append({"role": "assistant", "content": response})