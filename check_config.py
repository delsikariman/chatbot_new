#!/usr/bin/env python3
import os
import toml

def mask_key(key: str, show_chars: int = 8) -> str:
    """Mask API key untuk security (show hanya awal dan akhir)"""
    if not key or len(key) < show_chars * 2:
        return "***MASKED***"
    return f"{key[:show_chars]}...{key[-show_chars:]}"

print("=" * 60)
print("VERIFIKASI KONFIGURASI GROQ API")
print("=" * 60)

# 1. Cek environment variable
print("\n1️⃣ Environment Variable:")
env_key = os.getenv("GROQ_API_KEY")
if env_key:
    print(f"✅ GROQ_API_KEY ditemukan: {mask_key(env_key)}")
else:
    print("❌ GROQ_API_KEY tidak ditemukan")

# 2. Cek secrets.toml
print("\n2️⃣ Streamlit Secrets (.streamlit/secrets.toml):")
try:
    secrets = toml.load(".streamlit/secrets.toml")
    if "groq_api_key" in secrets:
        key = secrets["groq_api_key"]
        print(f"✅ groq_api_key ditemukan: {mask_key(key)}")
    else:
        print("❌ groq_api_key tidak ada di secrets.toml")
except Exception as e:
    print(f"❌ Error membaca secrets.toml: {e}")

# 3. Test Groq Connection
print("\n3️⃣ Test Groq API Connection:")
try:
    from groq import Groq
    
    # Coba ambil API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        secrets = toml.load(".streamlit/secrets.toml")
        api_key = secrets.get("groq_api_key")
    
    if not api_key:
        print("❌ Tidak ada API key yang ditemukan!")
    else:
        print("🔄 Menghubungi Groq API...")
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=50,
            messages=[{"role": "user", "content": "Halo!"}]
        )
        
        print(f"✅ SUCCESS! Response: {response.choices[0].message.content[:50]}...")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
