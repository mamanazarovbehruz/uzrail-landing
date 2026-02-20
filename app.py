from flask import Flask, render_template, request

app = Flask(__name__)

ETICKET_BASE = "https://eticket.railway.uz"

@app.get("/")
def home():
    return "OK"

@app.get("/go")
def go_page():
    lang = (request.args.get("lang", "uz") or "uz").lower()
    if lang not in ("uz", "ru", "en"):
        lang = "uz"

    dep = (request.args.get("dep", "") or "").strip()
    arv = (request.args.get("arv", "") or "").strip()
    date = (request.args.get("date", "") or "").strip()

    # ✅ 1) Eticket trains-page (siz xohlagan sahifa)
    # Eslatma: query param’larni sayt ishlatsa — to‘g‘ridan-to‘g‘ri to‘ldirib ochadi,
    # ishlatmasa ham baribir trains-page ochiladi.
    eticket_trains = (
        f"{ETICKET_BASE}/{lang}/pages/trains-page"
        f"?date={date}&depStationCode={dep}&arvStationCode={arv}"
    )

    # ✅ 2) Oddiy home (fallback)
    eticket_home = f"{ETICKET_BASE}/{lang}/home"

    return render_template(
        "go.html",
        lang=lang,
        dep=dep,
        arv=arv,
        date=date,
        eticket_trains=eticket_trains,
        eticket_home=eticket_home,
    )

if __name__ == "__main__":
    # Lokal test
    app.run(host="0.0.0.0", port=8080)