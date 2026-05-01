#!/usr/bin/env python3
"""
Script untuk mendapatkan daftar model yang tersedia di Groq
"""
import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        import streamlit as st
        if "groq_api_key" in st.secrets:
            api_key = st.secrets["groq_api_key"]
    except:
        pass

if not api_key:
    print("❌ GROQ_API_KEY tidak ditemukan")
    exit(1)

client = Groq(api_key=api_key)

print("Daftar model yang tersedia di Groq:")
print("=" * 50)

try:
    # Coba akses models
    models = client.models.list()
    for model in models.data:
        print(f"- {model.id}")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMencoba model yang umum digunakan:")
    common_models = [
        "llama-3.2-90b-vision-preview",
        "llama-3.2-1b-preview",
        "mixtral-8x7b-32768",
        "gemma-2-9b-it",
    ]
    print("\n".join(f"- {model}" for model in common_models))
