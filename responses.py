import json
import os
from groq import Groq

# Inisialisasi Groq client
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY tidak ditemukan. Silakan set environment variable GROQ_API_KEY")
    return Groq(api_key=api_key)


def load_data():
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def get_response_from_groq(pesan):
    """Dapatkan respons dari Groq API dengan RAG (jika tersedia)"""
    try:
        client = get_groq_client()
        
        # Coba muat FAISS vectorstore jika ada
        context_text = ""
        vectorstore_path = "vectorstore"
        if os.path.exists(vectorstore_path):
            try:
                # Import lambat agar aplikasi tetap cepat jika RAG tidak digunakan
                from langchain_huggingface import HuggingFaceEmbeddings
                from langchain_community.vectorstores import FAISS
                
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'}
                )
                vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
                
                # Cari 4 bagian dokumen yang paling mirip dengan pertanyaan
                docs = vectorstore.similarity_search(pesan, k=4)
                context_pieces = [f"Referensi {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)]
                context_text = "\n\n".join(context_pieces)
            except Exception as e:
                print(f"Peringatan: Gagal memuat/mencari di vectorstore: {e}")

        system_prompt = (
            "Kamu adalah asisten AI untuk mata kuliah Artificial Intelligence. "
            "Tugas utamamu adalah menjawab pertanyaan pengguna berdasarkan referensi materi yang diberikan, karena referensi tersebut adalah bagian dari Rencana Pembelajaran Semester (RPS). "
            "Topik RPS mencakup luas dari Pengantar AI, Revolusi Industri 4.0, Society 5.0 (termasuk teknologi terkait seperti IoT dan Big Data), konsep dasar AI, Machine Learning, Generative AI, Etika AI, hingga AI dalam pendidikan. "
            "Jangan terlalu kaku menolak topik yang masih berhubungan dengan ekosistem teknologi (seperti IoT, Cloud, Data) selama itu relevan dengan perkembangan AI atau ada di dalam referensi yang disisipkan. "
            "HANYA tolak pertanyaan jika benar-benar di luar konteks akademis teknologi/AI (misal: resep masakan, gosip, atau topik yang sangat melenceng). "
            "Berikan jawaban yang jelas, akademis, namun mudah dipahami dalam bahasa Indonesia.\n\n"
        )
        
        if context_text:
            system_prompt += (
                "Berikut adalah potongan teks langsung dari buku/referensi PDF perkuliahan yang WAJIB kamu jadikan sumber utama untuk menjawab:\n"
                f"{context_text}\n\n"
                "Silakan baca referensi di atas. Jika jawaban dari pertanyaan pengguna ada atau tersirat di dalam referensi tersebut, WAJIB gunakan informasi itu dan jelaskan konteksnya."
            )

        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1024,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {"role": "user", "content": pesan}
            ]
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Maaf, terjadi kesalahan saat menghubungi Groq API: {str(e)}"


def respon_ai(pesan, use_groq=True):
    pesan_original = pesan
    pesan = pesan.lower().strip()
    data = load_data()

    # Cek apakah pertanyaan user cocok dengan data.json
    if pesan in data:
        return data[pesan]

    # Cek apakah kata kunci dari data.json ada di dalam pesan user
    for kata_kunci, jawaban in data.items():
        if kata_kunci in pesan:
            return jawaban

    # Jika tidak ditemukan di knowledge base dan use_groq=True, gunakan Groq API
    if use_groq:
        return get_response_from_groq(pesan_original)
    
    return "Maaf, pertanyaan tersebut belum tersedia dalam basis pengetahuan saya."

