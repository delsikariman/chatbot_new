import json
import os
import logging
import functools
import time
from typing import Optional

# Import configuration
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Global cache untuk vectorstore
_vectorstore_cache = None

# Response cache dengan TTL (Time To Live)
_response_cache = {}
_response_cache_time = {}

# Lazy import Groq - hanya saat diperlukan
def _get_groq():
    from groq import Groq
    return Groq


def get_groq_client():
    """
    Inisialisasi Groq client dengan API key dari environment variable.
    Lazy-loaded untuk menghemat memory.
    
    Returns:
        Groq: Client instance
        
    Raises:
        ValueError: Jika GROQ_API_KEY tidak ditemukan
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY tidak ditemukan. Silakan set environment variable GROQ_API_KEY")
    
    Groq = _get_groq()
    return Groq(api_key=api_key)


@functools.lru_cache(maxsize=1)
def load_data() -> dict:
    """
    Load knowledge base dari data.json dengan caching.
    Data JSON hanya di-load sekali dan di-cache di memory.
    
    Returns:
        dict: Knowledge base
        
    Raises:
        FileNotFoundError: Jika data.json tidak ditemukan
        json.JSONDecodeError: Jika data.json format invalid
    """
    try:
        with open(config.DATA_JSON_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"✅ Data.json loaded and cached ({len(data)} entries)")
            return data
    except FileNotFoundError:
        logger.warning(f"data.json tidak ditemukan di {config.DATA_JSON_PATH}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"data.json format invalid: {e}")
        return {}


def load_vectorstore():
    """
    Load FAISS vectorstore dengan caching untuk performance.
    Vectorstore hanya di-load sekali dan di-cache di memory.
    OPTIMIZED: Menggunakan sentence-transformers (lebih ringan dari fastembed)
    
    Returns:
        FAISS vectorstore atau None jika tidak tersedia
    """
    global _vectorstore_cache
    
    if not os.path.exists(config.VECTORSTORE_PATH):
        logger.debug(f"Vectorstore path tidak ada: {config.VECTORSTORE_PATH}")
        return None
    
    # Cek cache terlebih dahulu
    if _vectorstore_cache is not None:
        logger.debug("Menggunakan vectorstore dari cache")
        return _vectorstore_cache
    
    try:
        logger.info("Loading vectorstore... (ini mungkin memakan waktu)")
        
        # Coba gunakan sentence-transformers (lebih ringan untuk cloud)
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_community.vectorstores import FAISS
            
            embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",  # Model ringan untuk cloud
                encode_kwargs={"normalize_embeddings": True}
            )
            logger.info("Using HuggingFaceEmbeddings (all-MiniLM-L6-v2)")
        except ImportError:
            # Fallback ke fastembed jika HuggingFace tidak tersedia
            from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
            from langchain_community.vectorstores import FAISS
            
            embeddings = FastEmbedEmbeddings()
            logger.info("Using FastEmbedEmbeddings (fallback)")
        
        _vectorstore_cache = FAISS.load_local(
            config.VECTORSTORE_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        logger.info(f"✅ Vectorstore loaded successfully (cached with {len(_vectorstore_cache.index_to_docstore_id)} docs)")
        return _vectorstore_cache
        
    except ImportError as e:
        logger.warning(f"Embedding library tidak tersedia: {e}. Lanjut tanpa RAG.")
        return None
    except Exception as e:
        logger.error(f"Gagal memuat vectorstore: {e}")
        return None


def _get_cached_response(cache_key: str) -> Optional[str]:
    """
    Ambil response dari cache jika masih valid (belum expired).
    
    Args:
        cache_key (str): Key untuk lookup cache
        
    Returns:
        str atau None: Cached response atau None jika expired/tidak ada
    """
    if not config.RESPONSE_CACHE_ENABLED:
        return None
    
    if cache_key not in _response_cache:
        return None
    
    # Cek TTL (Time To Live)
    cache_time = _response_cache_time.get(cache_key, 0)
    if time.time() - cache_time > config.RESPONSE_CACHE_TTL:
        # Cache expired, hapus
        del _response_cache[cache_key]
        del _response_cache_time[cache_key]
        logger.debug(f"Cache expired for key: {cache_key[:50]}")
        return None
    
    logger.debug(f"✓ Cache HIT for key: {cache_key[:50]}")
    return _response_cache[cache_key]


def _set_cached_response(cache_key: str, response: str) -> None:
    """
    Simpan response ke cache.
    
    Args:
        cache_key (str): Key untuk cache
        response (str): Response yang akan di-cache
    """
    if not config.RESPONSE_CACHE_ENABLED:
        return
    
    # Jika cache sudah penuh, hapus entry tertua
    if len(_response_cache) >= config.RESPONSE_CACHE_MAX_SIZE:
        # Hapus entry tertua (berdasarkan waktu)
        oldest_key = min(_response_cache_time, key=_response_cache_time.get)
        del _response_cache[oldest_key]
        del _response_cache_time[oldest_key]
        logger.debug(f"Cache full, removed oldest entry")
    
    _response_cache[cache_key] = response
    _response_cache_time[cache_key] = time.time()
    logger.debug(f"✓ Cached response for key: {cache_key[:50]}")


def get_response_from_groq(pesan: str) -> str:
    """
    Dapatkan respons dari Groq API dengan RAG (Retrieval-Augmented Generation).
    Response di-cache untuk mengurangi API calls.
    
    Args:
        pesan (str): Pertanyaan dari user
        
    Returns:
        str: Jawaban dari Groq API atau error message
    """
    # Cek response cache terlebih dahulu
    cache_key = pesan.lower().strip()
    cached_response = _get_cached_response(cache_key)
    if cached_response:
        logger.info("✅ Using cached Groq response")
        return cached_response
    
    try:
        client = get_groq_client()
        
        # Coba ambil context dari vectorstore (dengan caching)
        context_text = ""
        vectorstore = load_vectorstore()
        
        if vectorstore:
            try:
                # Cari k dokumen yang paling mirip dengan pertanyaan
                docs = vectorstore.similarity_search(pesan, k=config.K_SEARCH)
                if docs:
                    context_pieces = [f"Referensi {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)]
                    context_text = "\n\n".join(context_pieces)
                    logger.info(f"Found {len(docs)} relevant documents")
            except Exception as e:
                logger.warning(f"Gagal mencari di vectorstore: {e}")

        system_prompt = config.SYSTEM_PROMPT_BASE
        
        if context_text:
            system_prompt += config.SYSTEM_PROMPT_WITH_CONTEXT.format(context=context_text)

        chat_completion = client.chat.completions.create(
            model=config.GROQ_MODEL,
            max_tokens=config.GROQ_MAX_TOKENS,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {"role": "user", "content": pesan}
            ]
        )
        
        response = chat_completion.choices[0].message.content
        logger.info("✅ Groq API response successful")
        
        # Cache response
        _set_cached_response(cache_key, response)
        
        return response
        
    except ValueError as e:
        logger.error(f"API Key error: {e}")
        return "❌ Error: API Key tidak ditemukan. Silakan set GROQ_API_KEY."
    except TimeoutError:
        logger.error("Groq API timeout")
        return "⏱️ Groq API sedang lambat. Coba lagi nanti."
    except Exception as e:
        logger.error(f"Groq API error: {type(e).__name__}: {e}")
        return f"⚠️ Maaf, terjadi kesalahan: {str(e)[:100]}"


def respon_ai(pesan: str, use_groq: bool = True) -> str:
    """
    Process pertanyaan dan return jawaban dari knowledge base atau Groq API.
    
    Args:
        pesan (str): Pertanyaan dari user
        use_groq (bool): Gunakan Groq API jika True, default True
        
    Returns:
        str: Jawaban
    """
    # ========== VALIDATION ==========
    pesan_original = pesan
    pesan_clean = pesan.strip()
    
    # Cek apakah pertanyaan kosong
    if not pesan_clean:
        logger.warning("Empty input received")
        return "❌ Pertanyaan tidak boleh kosong. Silakan coba lagi."
    
    # Cek panjang pertanyaan (max config.MAX_INPUT_LENGTH)
    if len(pesan_clean) > config.MAX_INPUT_LENGTH:
        logger.warning(f"Input too long: {len(pesan_clean)} chars")
        return f"⚠️ Pertanyaan terlalu panjang (max {config.MAX_INPUT_LENGTH} karakter)."
    
    # ========== KNOWLEDGE BASE LOOKUP ==========
    pesan_lower = pesan_clean.lower()
    data = load_data()
    
    # Cek exact match dengan data.json
    if pesan_lower in data:
        logger.info(f"✅ Found exact match: {pesan_lower[:50]}")
        return data[pesan_lower]
    
    # Cek keyword match
    for kata_kunci, jawaban in data.items():
        if kata_kunci in pesan_lower:
            logger.info(f"✅ Found keyword match: {kata_kunci}")
            return jawaban
    
    # ========== GROQ API FALLBACK ==========
    if use_groq:
        logger.info(f"No match found, using Groq API...")
        return get_response_from_groq(pesan_original)
    
    logger.info(f"No match found and use_groq=False")
    return "📚 Pertanyaan tidak ditemukan dalam basis pengetahuan. Coba rephrase atau aktifkan Groq AI."

