import os
from flask import Flask, render_template, request

PLAY_URL = "https://play.google.com/store/apps/details?id=com.axonlogic.uzrailway&hl=ru"
APPLE_URL = "https://apps.apple.com/uz/app/uzrailways-tickets/id1497456207"
APP_PACKAGE = "com.axonlogic.uzrailway"

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

    # keyin buni real search url'ga almashtiramiz
    target = f"https://eticket.railway.uz/{lang}/home"

    fallback = urllib.parse.quote(PLAY_URL, safe="")
    app_intent = (
        f"intent://eticket.railway.uz/{lang}/home"
        f"#Intent;scheme=https;package={APP_PACKAGE};"
        f"S.browser_fallback_url={fallback};end"
    )

    # Android Chrome intent (har doim 100% majbur emas)
    chrome_intent = (
        "intent://" + target.replace("https://", "").replace("http://", "")
        + "#Intent;scheme=https;package=com.android.chrome;end"
    )

    return render_template(
        "go.html",
        lang=lang, dep=dep, arv=arv, date=date,
        target=target,
        chrome_intent=chrome_intent,
        app_intent=app_intent,
        play_url=PLAY_URL,
        apple_url=APPLE_URL,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
