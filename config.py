"""
Centralized configuration for Chatbot AI
All constants and settings in one place for easy tuning and maintenance.
"""

# ==================== GROQ API SETTINGS ====================
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_MAX_TOKENS = 1024
GROQ_TIMEOUT = 30  # seconds

# ==================== VECTORSTORE SETTINGS ====================
VECTORSTORE_PATH = "vectorstore"
K_SEARCH = 4  # Number of documents to retrieve from vectorstore
CHUNK_SIZE = 1000  # When ingesting PDFs
CHUNK_OVERLAP = 200  # When ingesting PDFs

# ==================== INPUT VALIDATION ====================
MAX_INPUT_LENGTH = 5000  # Maximum question length (characters)
MIN_INPUT_LENGTH = 1  # Minimum question length (characters)

# ==================== KNOWLEDGE BASE ====================
DATA_JSON_PATH = "data.json"
PDF_FOLDER_PATH = "Referensi"

# ==================== CACHE SETTINGS ====================
CACHE_MAX_SIZE = 128  # LRU cache max size for data.json
RESPONSE_CACHE_ENABLED = True
RESPONSE_CACHE_TTL = 3600  # Cache response for 1 hour (seconds)
RESPONSE_CACHE_MAX_SIZE = 256  # Max cached responses

# ==================== LOGGING ====================
LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# ==================== STREAMLIT SETTINGS ====================
STREAMLIT_PAGE_TITLE = "Chatbot Pembelajaran"
STREAMLIT_PAGE_ICON = "💬"
STREAMLIT_LAYOUT = "centered"

# ==================== RAG SYSTEM PROMPT ====================
SYSTEM_PROMPT_BASE = (
    "Kamu adalah asisten AI untuk mata kuliah Artificial Intelligence. "
    "Tugas utamamu adalah menjawab pertanyaan pengguna berdasarkan referensi materi yang diberikan, "
    "karena referensi tersebut adalah bagian dari Rencana Pembelajaran Semester (RPS). "
    "Topik RPS mencakup luas dari Pengantar AI, Revolusi Industri 4.0, Society 5.0 "
    "(termasuk teknologi terkait seperti IoT dan Big Data), konsep dasar AI, Machine Learning, "
    "Generative AI, Etika AI, hingga AI dalam pendidikan. "
    "Jangan terlalu kaku menolak topik yang masih berhubungan dengan ekosistem teknologi "
    "(seperti IoT, Cloud, Data) selama itu relevan dengan perkembangan AI atau ada di dalam referensi yang disisipkan. "
    "HANYA tolak pertanyaan jika benar-benar di luar konteks akademis teknologi/AI "
    "(misal: resep masakan, gosip, atau topik yang sangat melenceng). "
    "Berikan jawaban yang jelas, akademis, namun mudah dipahami dalam bahasa Indonesia.\n\n"
)

SYSTEM_PROMPT_WITH_CONTEXT = (
    "Berikut adalah potongan teks langsung dari buku/referensi PDF perkuliahan yang WAJIB kamu jadikan "
    "sumber utama untuk menjawab:\n"
    "{context}\n\n"
    "Silakan baca referensi di atas. Jika jawaban dari pertanyaan pengguna ada atau tersirat di dalam "
    "referensi tersebut, WAJIB gunakan informasi itu dan jelaskan konteksnya."
)
