import os
import urllib.parse
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ETICKET_BASE = "https://eticket.railway.uz"
ETICKET_API = f"{ETICKET_BASE}/api/v3/handbook/trains/list"

def _get_xsrf_from_session(sess: requests.Session) -> str | None:
    # XSRF-TOKEN odatda cookie ichida bo‘ladi (URL-encoded bo‘lishi mumkin)
    token = sess.cookies.get("XSRF-TOKEN")
    if not token:
        return None
    return urllib.parse.unquote(token)

@app.post("/api/trains")
def api_trains():
    data = request.get_json(force=True) or {}
    dep = str(data.get("dep", "")).strip()
    arv = str(data.get("arv", "")).strip()
    date = str(data.get("date", "")).strip()
    lang = (str(data.get("lang", "uz")).strip().lower() or "uz")
    if lang not in ("uz", "ru", "en"):
        lang = "uz"

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
        sess = requests.Session()

        # 1) Brauzer kabi avval HOME sahifani ochib cookie/xsrf olamiz
        home_url = f"{ETICKET_BASE}/{lang}/home"
        common_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "uz,en;q=0.9,ru;q=0.8",
            "Referer": home_url,
            "Origin": ETICKET_BASE,
        }

        r0 = sess.get(home_url, headers=common_headers, timeout=20)
        # Home 200 bo‘lmasa ham, cookie kelishi mumkin; lekin baribir tekshiramiz
        xsrf = _get_xsrf_from_session(sess)

        # 2) API call: X-XSRF-TOKEN header qo‘shamiz (bor bo‘lsa)
        headers = dict(common_headers)
        headers["Content-Type"] = "application/json;charset=UTF-8"
        headers["X-Requested-With"] = "XMLHttpRequest"
        if xsrf:
            headers["X-XSRF-TOKEN"] = xsrf

        r = sess.post(ETICKET_API, json=payload, headers=headers, timeout=25)

        if r.status_code >= 400:
            # debug uchun: status + kichik body
            return jsonify({
                "ok": False,
                "status": r.status_code,
                "home_status": r0.status_code,
                "has_xsrf": bool(xsrf),
                "body": (r.text or "")[:500]
            }), 502

        return jsonify(r.json())

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 502