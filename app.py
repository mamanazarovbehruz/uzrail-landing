import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.get("/")
def health():
    return "UzRail Landing is running ✅", 200

@app.get("/go")
def go():
    lang = (request.args.get("lang") or "uz").lower()
    if lang not in ("uz", "ru", "en"):
        lang = "uz"

    dep = request.args.get("dep") or ""
    arv = request.args.get("arv") or ""
    date = request.args.get("date") or ""

    # ✅ 2-rasmdagi sahifa
    trains_url = f"https://eticket.railway.uz/{lang}/pages/trains-page"

    # ✅ shu yerda paramlar bilan yuboramiz (agar qabul qilsa — zo‘r)
    # Eslatma: param nomlari ishlamasa, keyingi qadamda JS bilan to‘ldiramiz
    trains_url_with_params = (
        f"{trains_url}"
        f"?dep={dep}&arv={arv}&date={date}"
    )

    # ✅ Chrome intent (Android’da Chrome’ni majburiy ochishga urinadi)
    chrome_intent = (
        "intent://" + trains_url_with_params.replace("https://", "").replace("http://", "")
        + "#Intent;scheme=https;package=com.android.chrome;end"
    )

    # (fallback) oddiy link
    normal_link = trains_url_with_params

    return render_template(
        "go.html",
        lang=lang,
        dep=dep,
        arv=arv,
        date=date,
        chrome_intent=chrome_intent,
        normal_link=normal_link,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))