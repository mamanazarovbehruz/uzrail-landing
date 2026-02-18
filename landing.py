import os
from flask import Flask, request, Response

app = Flask(__name__)

@app.get("/")
def health():
    return "UzRail Landing is running ✅", 200

@app.get("/go")
def go():
    lang = (request.args.get("lang") or "uz").lower()
    dep = request.args.get("dep") or ""
    arv = request.args.get("arv") or ""
    date = request.args.get("date") or ""

    # Hozircha eticket home. Keyin real search URL'ga almashtiramiz.
    target = f"https://eticket.railway.uz/{lang}/home"

    # Android uchun Chrome intent (har doim 100% emas, lekin ko‘p hollarda Chrome ochadi)
    chrome_intent = (
        "intent://" + target.replace("https://", "").replace("http://", "")
        + "#Intent;scheme=https;package=com.android.chrome;end"
    )

    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Chipta ochish</title>
  <style>
    body {{ font-family: Arial, sans-serif; background:#0b1220; color:#fff; margin:0;
           display:flex; align-items:center; justify-content:center; height:100vh; }}
    .card {{ width:min(520px, 92vw); background:#111a2e; border:1px solid #26314d;
            border-radius:16px; padding:22px; }}
    h2 {{ margin:0 0 8px; font-size:18px; }}
    p {{ margin:0 0 18px; opacity:.85; }}
    .btn {{ display:block; width:100%; padding:14px 16px; border-radius:12px;
           text-decoration:none; color:#fff; text-align:center; margin:10px 0;
           border:1px solid #2b3a63; }}
  </style>
</head>
<body>
  <div class="card">
    <h2>Qayerda ochamiz?</h2>
    <p>📍 <b>{dep} → {arv}</b><br/>📅 <b>{date}</b></p>

    <a class="btn" href="{chrome_intent}">🌐 Google Chrome’da ochish</a>
    <a class="btn" href="{target}">🚆 Uz Rail Ticket (web/ilova)</a>

    <p style="margin-top:14px; font-size:12px; opacity:.7">
      Eslatma: iOS’da Chrome/ilovani majburlash cheklangan bo‘lishi mumkin.
    </p>
  </div>
</body>
</html>
"""
    return Response(html, mimetype="text/html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
