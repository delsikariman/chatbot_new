#!/usr/bin/env python3
"""
Script untuk verifikasi setup Groq API dengan better error handling
"""
import os
import sys
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def mask_key(key: str, show_chars: int = 8) -> str:
    """Mask API key untuk security"""
    if not key or len(key) < show_chars * 2:
        return "***MASKED***"
    return f"{key[:show_chars]}...{key[-show_chars:]}"

def check_groq_setup():
    print("=" * 50)
    print("Verifikasi Setup Groq API")
    print("=" * 50)
    
    # Check 1: Library groq sudah terinstall?
    print("\n1. Checking groq library...")
    try:
        import groq
        print("   ✅ groq library terinstall")
    except ImportError:
        print("   ❌ groq library TIDAK terinstall")
        print("   Fix: Run 'pip install -r requirements.txt'")
        return False
    
    # Check 2: API Key tersedia?
    print("\n2. Checking GROQ_API_KEY...")
    api_key = os.getenv("GROQ_API_KEY")
    
    if api_key:
        print(f"   ✅ GROQ_API_KEY ditemukan: {mask_key(api_key)}")
    else:
        # Cek di Streamlit secrets
        try:
            import streamlit as st
            if "groq_api_key" in st.secrets:
                print("   ✅ API Key ditemukan di .streamlit/secrets.toml")
                api_key = st.secrets["groq_api_key"]
            else:
                print("   ⚠️  API Key TIDAK ditemukan!")
                print("   Fix: Set GROQ_API_KEY atau edit .streamlit/secrets.toml")
                return False
        except:
            print("   ⚠️  API Key TIDAK ditemukan!")
            print("   Fix: Set GROQ_API_KEY environment variable")
            return False
    
    # Check 3: Test koneksi Groq API
    print("\n3. Testing Groq API connection...")
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=100,
            messages=[
                {
                    "role": "system",
                    "content": "Kamu adalah chatbot yang helpful dan ramah"
                },
                {"role": "user", "content": "Hai, apakah kamu bisa mendengarku?"}
            ]
        )
        
        print("   ✅ Groq API berfungsi!")
        print(f"   Response: {chat_completion.choices[0].message.content[:100]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False
    
    # Check 4: Data JSON tersedia?
    print("\n4. Checking data.json...")
    if os.path.exists("data.json"):
        import json
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"   ✅ data.json ditemukan ({len(data)} entries)")
        except Exception as e:
            print(f"   ❌ data.json error: {e}")
            return False
    else:
        print("   ⚠️  data.json tidak ditemukan (tidak kritis)")
    
    # Check 5: Vectorstore tersedia?
    print("\n5. Checking vectorstore...")
    if os.path.exists("vectorstore"):
        print("   ✅ vectorstore folder ditemukan (RAG siap)")
    else:
        print("   ⚠️  vectorstore tidak ditemukan (jalankan ingest.py untuk setup)")
    
    print("\n" + "=" * 50)
    print("✅ Setup berhasil! Siap digunakan.")
    print("=" * 50)
    print("\nJalankan chatbot:")
    print("  - Streamlit: streamlit run app.py")
    print("  - CLI:       python main.py")
    
    return True

if __name__ == "__main__":
    success = check_groq_setup()
    sys.exit(0 if success else 1)
