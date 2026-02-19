import os
from flask import Flask, render_template, request

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

    # Android Chrome intent (har doim 100% majbur emas)
    chrome_intent = (
        "intent://" + target.replace("https://", "").replace("http://", "")
        + "#Intent;scheme=https;package=com.android.chrome;end"
    )

    return render_template(
        "go.html",
        lang=lang,
        dep=dep,
        arv=arv,
        date=date,
        target=target,
        chrome_intent=chrome_intent,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
