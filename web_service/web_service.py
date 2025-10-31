from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

API_URL = "https://hello-cloud6.onrender.com"

HTML = """
<!doctype html>
<html>
<head>
    <title>NERELİSİN BACIM</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
        h1 { color: #333; }
        input { padding: 10px; font-size: 16px; margin: 5px; }
        button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
        li { background: white; margin: 5px auto; width: 250px; padding: 8px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Mikro Hizmetli Selam!</h1>
    <p>Adını ve şehrini yaz:</p>
    <form method="POST">
        <input type="text" name="isim" placeholder="Adını yaz" required>
        <input type="text" name="şehir" placeholder="Şehir yaz" required>
        <button type="submit">Gönder</button>
    </form>

    <h3>Ziyaretçiler:</h3>
    <ul>
       {% for kisi in isimler %}
         <li>{{ kisi.isim }} {{ kisi.şehir }}</li>
       {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        isim = request.form.get("isim")
        şehir = request.form.get("şehir")

        if isim and şehir:
            try:
                # API'ye POST isteği at
                requests.post(API_URL + "/ziyaretciler", json={"isim": isim, "şehir": şehir})
            except Exception as e:
                print("API bağlantı hatası:", e)
        return redirect("/")

    # GET isteği → ziyaretçi listesini çek
    try:
        resp = requests.get(API_URL + "/ziyaretciler")
        isimler = resp.json() if resp.status_code == 200 else []
    except Exception as e:
        print("API bağlantı hatası:", e)
        isimler = []

    return render_template_string(HTML, isimler=isimler)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
