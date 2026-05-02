import streamlit as st
import os
import sys
import logging
import config

# Suppress langchain warnings
logging.getLogger("langchain").setLevel(logging.ERROR)

# Configure Streamlit for cloud
st.set_page_config(
    page_title=config.STREAMLIT_PAGE_TITLE,
    page_icon=config.STREAMLIT_PAGE_ICON,
    layout=config.STREAMLIT_LAYOUT,
    initial_sidebar_state="collapsed"
)

# Lazy import responses (avoid loading heavy dependencies at startup)
@st.cache_resource
def get_response_functions():
    from responses import respon_ai
    return respon_ai

respon_ai = get_response_functions()

st.title(config.STREAMLIT_PAGE_TITLE)
st.caption("Chatbot dengan AI berbasis Groq")

# Setup API key dari Streamlit secrets atau environment variable
api_key = None

# Priority 1: Gunakan st.secrets (Streamlit built-in, paling reliable)
try:
    if "groq_api_key" in st.secrets:
        api_key = st.secrets.get("groq_api_key", "").strip()
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
except Exception as e:
    pass

# Priority 2: Cek environment variable
if not api_key:
    env_key = os.getenv("GROQ_API_KEY", "").strip()
    if env_key:
        api_key = env_key

# Priority 3: Direct read dari secrets.toml file
if not api_key:
    try:
        import toml
        secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit/secrets.toml")
        if os.path.exists(secrets_path):
            with open(secrets_path, 'r') as f:
                secrets_data = toml.load(f)
                if "groq_api_key" in secrets_data:
                    api_key = secrets_data["groq_api_key"].strip()
                    os.environ["GROQ_API_KEY"] = api_key
    except Exception as e:
        pass

# Inisialisasi session state
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = api_key

# Tampilkan status
if not api_key:
    st.error("❌ GROQ API Key TIDAK DITEMUKAN!")
    st.warning(
        "Untuk mengaktifkan AI Groq:\n"
        "1. Pastikan file `.streamlit/secrets.toml` ada\n"
        "2. Format: `groq_api_key = 'gsk_....'`\n"
        "3. Restart aplikasi Streamlit"
    )
    use_groq = False
else:
    st.success(f"✅ GROQ API Key berhasil dimuat!")
    use_groq = True

# Inisialisasi session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "use_groq" not in st.session_state:
    st.session_state.use_groq = use_groq

# Tombol reset
col1, col2 = st.columns(2)
with col1:
    if st.button("Hapus Percakapan", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

with col2:
    st.session_state.use_groq = st.checkbox(
        "Gunakan Groq AI", 
        value=st.session_state.use_groq, 
        disabled=not api_key
    )

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
            response = respon_ai(prompt, use_groq=st.session_state.use_groq)
        st.markdown(response)
    
    # Simpan jawaban bot
    st.session_state.messages.append({"role": "assistant", "content": response})