import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ETICKET_API = "https://eticket.railway.uz/api/v3/handbook/trains/list"

@app.get("/")
def health():
    return "UzRail Landing OK", 200

@app.get("/go")
def go():
    lang = (request.args.get("lang") or "uz").lower()
    if lang not in ("uz", "ru", "en"):
        lang = "uz"

    dep = request.args.get("dep") or ""
    arv = request.args.get("arv") or ""
    date = request.args.get("date") or ""

    # Eticket'ni natija sahifasi (lekin prefill bo‘lmasligi mumkin)
    trains_page = f"https://eticket.railway.uz/{lang}/pages/trains-page"

    return render_template(
        "go.html",
        lang=lang,
        dep=dep,
        arv=arv,
        date=date,
        trains_page=trains_page,
    )

# ✅ Backend proxy: CORS yo‘q, shu ishlaydi
@app.post("/api/trains")
def api_trains():
    data = request.get_json(force=True) or {}
    dep = str(data.get("dep", "")).strip()
    arv = str(data.get("arv", "")).strip()
    date = str(data.get("date", "")).strip()

    payload = {
        "directions": {
            "forward": {
                "date": date,
                "depStationCode": dep,
                "arvStationCode": arv
            }
        }
    }

    try:
        r = requests.post(ETICKET_API, json=payload, timeout=20)
        r.raise_for_status()
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))