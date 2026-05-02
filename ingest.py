#!/usr/bin/env python3
"""
Script untuk memproses file PDF di folder Referensi
dan menyimpannya ke dalam FAISS Vector Store.
"""

import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS
import config

def main():
    pdf_folder = config.PDF_FOLDER_PATH
    vectorstore_path = config.VECTORSTORE_PATH

    if not os.path.exists(pdf_folder):
        print(f"❌ Folder '{pdf_folder}' tidak ditemukan.")
        return

    # 1. Mencari semua file PDF
    pdf_files = glob.glob(os.path.join(pdf_folder, "*.pdf"))
    if not pdf_files:
        print(f"❌ Tidak ada file PDF di dalam folder '{pdf_folder}'.")
        return

    print(f"Ditemukan {len(pdf_files)} file PDF. Memulai proses pembacaan...")

    documents = []
    # 2. Membaca setiap PDF
    for pdf_file in pdf_files:
        print(f" Membaca: {os.path.basename(pdf_file)}...")
        try:
            loader = PyPDFLoader(pdf_file)
            docs = loader.load()
            documents.extend(docs)
        except Exception as e:
            print(f" ⚠️ Gagal membaca {os.path.basename(pdf_file)}: {e}")

    if not documents:
        print("❌ Tidak ada halaman PDF yang berhasil diekstrak.")
        return

    print(f"\nBerhasil mengekstrak {len(documents)} halaman. Memecah teks menjadi potongan...")

    # 3. Memecah dokumen menjadi potongan kecil (chunking)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Menghasilkan {len(chunks)} potongan teks.")

    # 4. Membuat Embeddings menggunakan FastEmbed
    print("Mengunduh/Memuat model embedding (FastEmbed)...")
    embeddings = FastEmbedEmbeddings()

    # 5. Membuat FAISS Vector Store
    print("Membuat FAISS Vector Database... (Ini mungkin memakan waktu)")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # 6. Menyimpan Vector Store secara lokal
    os.makedirs(vectorstore_path, exist_ok=True)
    vectorstore.save_local(vectorstore_path)
    
    print(f"\n✅ Selesai! Database vektor disimpan di folder '{vectorstore_path}'.")

if __name__ == "__main__":
    main()
