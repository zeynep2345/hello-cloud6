from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://zeynep:0bZZUwTFDFNoUjJxyMPPJWFaiY6HoCMV@dpg-d3tjfg1r0fns73ahsbtg-a.oregon-postgres.render.com/hellocloud2_db"
)

def connect_db():
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print("Database bağlantı hatası:", e)
        raise

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Tabloyu oluştur veya güncelle
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ziyaretciler (
                id SERIAL PRIMARY KEY,
                isim TEXT NOT NULL,
                şehir TEXT NOT NULL
            )
        """)
        # Eski tabloda şehir yoksa ekle
        cur.execute("ALTER TABLE ziyaretciler ADD COLUMN IF NOT EXISTS şehir TEXT;")

        if request.method == "POST":
            data = request.get_json(silent=True)
            isim = data.get("isim") if data else None
            şehir = data.get("şehir") if data else None

            if not isim or not şehir:
                return jsonify({"error": "İsim ve şehir alanları boş olamaz."}), 400

            cur.execute(
                "INSERT INTO ziyaretciler (isim, şehir) VALUES (%s, %s)",
                (isim, şehir)
            )
            conn.commit()

        # Son 10 ziyaretçiyi getir
        cur.execute("SELECT isim, şehir FROM ziyaretciler ORDER BY id DESC LIMIT 10")
        kayitlar = [{"isim": row["isim"], "şehir": row["şehir"]} for row in cur.fetchall()]

        return jsonify(kayitlar)

    except Exception as e:
        print("Hata:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5001)))
