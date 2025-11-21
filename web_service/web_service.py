from flask import Flask, render_template_string, request, redirect
import requests
import os

app = Flask(_name_)

# Backend API URL (Render'daki mikro hizmetin adresi)
API_URL = ""  # 🔹 Buraya kendi backend URL'ini yaz

# Basit HTML şablonu
HTML = """
<!doctype html>
<html>
<head>
    <title>Ziyaretçi Defteri</title>
    <style>
        body {
            font-family: Arial;
            text-align: center;
            padding: 50px;
            background: #eef2f3;
        }
        h1 {
            color: #333;
        }
        input {
            padding: 10px;
            font-size: 16px;
            margin: 5px;
        }
        button {
            padding: 10px 15px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        li {
            background: white;
            margin: 5px auto;
            width: 220px;
            padding: 8px;
            border-radius: 5px;
            list-style-type: none;
        }
    </style>
</head>
<body>
    <h1>Ziyaretçi Defteri</h1>
    <form method="POST">
        <input type="text" name="isim" placeholder="Adını yaz" required>
        <input type="text" name="sehir" placeholder="Şehrini yaz" required>
        <button type="submit">Gönder</button>
    </form>

    <h3>Ziyaretçiler:</h3>
    <ul>
        {% for kisi in isimler %}
            <li>{{ kisi.isim }} ({{ kisi.sehir }})</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        isim = request.form.get("isim")
        sehir = request.form.get("sehir")

        # Backend API'ye POST isteği gönder
        try:
            requests.post(API_URL + "/ziyaretciler", json={"isim": isim, "sehir": sehir})
        except Exception as e:
            print("API'ye bağlanılamadı:", e)
        return redirect("/")

    # Ziyaretçi listesini backend'den al
    try:
        resp = requests.get(API_URL + "/ziyaretciler")
        isimler = resp.json() if resp.status_code == 200 else []
    except Exception as e:
        print("API isteği başarısız:", e)
        isimler = []

    return render_template_string(HTML, isimler=isimler)

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
