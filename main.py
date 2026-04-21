from responses import respon_ai

print("=== Chatbot Sederhana ===")
print("Ketik 'keluar' untuk berhenti.\n")

while True:
    pertanyaan = input("Anda: ")
    jawaban = respon_ai(pertanyaan)
    print("Bot:", jawaban)

    if pertanyaan.lower().strip() in ["bye", "selesai", "keluar"]:
        break
