import os
import urllib.parse
from flask import Flask, render_template, request

app = Flask(__name__)

PLAY_URL = "https://play.google.com/store/apps/details?id=com.axonlogic.uzrailway&hl=ru"
APPLE_URL = "https://apps.apple.com/uz/app/uzrailways-tickets/id1497456207"
APP_PACKAGE = "com.axonlogic.uzrailway"


@app.get("/")
def health():
    return "UzRail Landing is running ✅", 200


@app.get("/go")
def go():
    lang = (request.args.get("lang") or "uz").strip().lower()
    dep = (request.args.get("dep") or "").strip()
    arv = (request.args.get("arv") or "").strip()
    date = (request.args.get("date") or "").strip()

    # Hozircha home (keyin deep-link topilsa o'zgartiramiz)
    target = f"https://eticket.railway.uz/{lang}/home"

    # 1) Chrome intent (tashqi Chrome brauzerga chiqarish)
    chrome_intent = (
        "intent://" + target.replace("https://", "").replace("http://", "")
        + "#Intent;scheme=https;package=com.android.chrome;end"
    )

    # 2) UzRail app intent (app bo'lsa ochiladi, bo'lmasa Play Market fallback)
    fallback = urllib.parse.quote(PLAY_URL, safe="")
    app_intent = (
        f"intent://eticket.railway.uz/{lang}/home"
        f"#Intent;scheme=https;package={APP_PACKAGE};"
        f"S.browser_fallback_url={fallback};end"
    )

    return render_template(
        "go.html",
        lang=lang,
        dep=dep,
        arv=arv,
        date=date,
        target=target,
        chrome_intent=chrome_intent,
        app_intent=app_intent,
        play_url=PLAY_URL,
        apple_url=APPLE_URL,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))