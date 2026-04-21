import streamlit as st

st.set_page_config(
    page_title="Chatbot Pembelajaran",
    page_icon="💬",
    layout="centered"
)

st.title("Chatbot Pembelajaran")
st.caption("Chatbot sederhana untuk tanya jawab materi pembelajaran")

# Inisialisasi session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tombol reset
if st.button("Hapus Percakapan"):
    st.session_state.messages = []
    st.rerun()

# Basis pengetahuan sederhana
knowledge_base = {
    "halo": "Halo, ada yang bisa saya bantu?",
    "apa itu ai": "AI atau Artificial Intelligence adalah cabang ilmu komputer yang mempelajari bagaimana sistem dapat meniru kemampuan cerdas manusia.",
    "apa itu machine learning": "Machine Learning adalah bagian dari AI yang memungkinkan sistem belajar dari data tanpa harus diprogram secara eksplisit untuk setiap aturan.",
    "apa itu deep learning": "Deep Learning adalah cabang dari Machine Learning yang menggunakan jaringan saraf tiruan berlapis untuk mempelajari pola yang kompleks.",
    "siapa kamu": "Saya adalah chatbot pembelajaran berbasis Streamlit."
}

# Tampilkan seluruh riwayat percakapan
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input chat
prompt = st.chat_input("Masukkan pertanyaan Anda...")

if prompt:
    # Tampilkan pertanyaan pengguna
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Proses jawaban
    user_text = prompt.lower().strip()

    if user_text in knowledge_base:
        response = knowledge_base[user_text]
    else:
        response = (
            "Maaf, saya belum memiliki jawaban untuk pertanyaan tersebut. "
            "Silakan tambahkan ke basis pengetahuan chatbot."
        )

    # Simpan jawaban bot
    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()
