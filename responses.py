def respon_ai(pesan):
    pesan = pesan.lower().strip()

    if pesan in ["halo", "hai", "hello"]:
        return "Halo, ada yang bisa saya bantu?"
    elif "nama" in pesan:
        return "Saya adalah chatbot sederhana buatan Python."
    elif "apa itu ai" in pesan:
        return "AI atau kecerdasan buatan adalah sistem yang dirancang untuk meniru kemampuan berpikir manusia."
    elif "bantuan" in pesan:
        return "Anda bisa bertanya tentang AI, data, atau materi kuliah."
    elif pesan in ["bye", "selesai", "keluar"]:
        return "Sampai jumpa."
    else:
        return "Maaf, pertanyaan tersebut belum tersedia dalam basis pengetahuan saya."

