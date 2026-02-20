# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/go")
def go():
    lang = (request.args.get("lang", "uz") or "uz").lower()
    if lang not in ("uz", "ru", "en"):
        lang = "uz"

    dep = request.args.get("dep")
    arv = request.args.get("arv")
    date = request.args.get("date")

    # ✅ Siz xohlagan: Chrome bosilganda jadval sahifasi ochilsin
    schedule_url = f"https://eticket.railway.uz/{lang}/pages/schedule"

    # (ixtiyoriy) oddiy home link ham qoldiramiz (fallback)
    home_url = f"https://eticket.railway.uz/{lang}/home"

    return render_template(
        "go.html",
        lang=lang,
        dep=dep,
        arv=arv,
        date=date,
        schedule_url=schedule_url,
        home_url=home_url,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)