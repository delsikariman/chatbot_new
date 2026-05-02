#!/usr/bin/env python
import os
import sys
from groq import Groq

def mask_key(key: str, show_chars: int = 8) -> str:
    """Mask API key untuk security"""
    if not key or len(key) < show_chars * 2:
        return "***MASKED***"
    return f"{key[:show_chars]}...{key[-show_chars:]}"

# Load API key dari environment variable atau secrets.toml
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        import toml
        secrets = toml.load(".streamlit/secrets.toml")
        api_key = secrets.get("groq_api_key")
    except:
        api_key = None

print("=" * 50)
print("Testing Groq API Connection")
print("=" * 50)

if not api_key:
    print("❌ API Key tidak ditemukan!")
    sys.exit(1)

print(f"✅ API Key ditemukan: {mask_key(api_key)}")

try:
    print("\n🔄 Membuat koneksi ke Groq...")
    client = Groq(api_key=api_key)
    
    print("🔄 Mengirim request ke Groq API...")
    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Halo, apa kabar?"}
        ]
    )
    
    response = message.choices[0].message.content
    print(f"\n✅ SUCCESS! Response dari Groq:")
    print(f"   {response}")
    print("\n✅ Koneksi ke Groq API berfungsi dengan baik!")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   {str(e)}")
    
    # Provide specific solutions
    error_msg = str(e).lower()
    if "connection" in error_msg:
        print("\n💡 SOLUSI: Masalah koneksi. Cek:")
        print("   - Koneksi internet aktif?")
        print("   - Firewall/proxy memblokir?")
        print("   - Server Groq sedang down?")
    elif "invalid" in error_msg or "unauthorized" in error_msg:
        print("\n💡 SOLUSI: API Key tidak valid. Cek:")
        print("   - API Key sudah dikopi dengan benar?")
        print("   - API Key sudah expired?")
        print("   - Buat API Key baru di https://console.groq.com/keys")
    elif "timeout" in error_msg:
        print("\n💡 SOLUSI: Request timeout. Coba:")
        print("   - Cek koneksi internet")
        print("   - Tunggu beberapa saat dan coba lagi")
