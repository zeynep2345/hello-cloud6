from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2, os

app = Flask(_name_)
CORS(app)

# Veritabanı bağlantısı
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://sevval:C2TbUsmgDpeSO5zG34kl2cLqd94IoUaC@dpg-d426lkpr0fns739009mg-a.oregon-postgres.render.com/hello_cloud2_db_n274"
)

def connect_db():
    return psycopg2.connect(DATABASE_URL)

# 🔹 Ana sayfa rotası (Render ve tarayıcı testleri için)
@app.route("/")
def home():
    return "Ziyaretçi API çalışıyor 🚀"

# 🔹 Ziyaretçi kayıt & listeleme endpoint'i
@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()
    
    # Tabloyu şehir alanıyla birlikte oluştur
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ziyaretciler (
            id SERIAL PRIMARY KEY,
            isim TEXT,
            sehir TEXT
        )
    """)

    # POST isteği ile yeni kayıt ekleme
    if request.method == "POST":
        data = request.get_json()
        isim = data.get("isim")
        sehir = data.get("sehir")

        if isim and sehir:
            cur.execute("INSERT INTO ziyaretciler (isim, sehir) VALUES (%s, %s)", (isim, sehir))
            conn.commit()

    # Son 10 kaydı listele (isim + şehir)
    cur.execute("SELECT isim, sehir FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    kayitlar = [{"isim": row[0], "sehir": row[1]} for row in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify(kayitlar)

# 🔹 Uygulama yerel çalıştırma ayarı
if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5001)
