import urllib.parse
import re
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ETICKET_BASE = "https://eticket.railway.uz"
ETICKET_API  = f"{ETICKET_BASE}/api/v3/handbook/trains/list"

def _cookie_xsrf(sess: requests.Session) -> str | None:
    token = sess.cookies.get("XSRF-TOKEN")
    return urllib.parse.unquote(token) if token else None

def _html_csrf_token(html: str) -> str | None:
    # <meta name="csrf-token" content="...">
    m = re.search(r'name="csrf-token"\s+content="([^"]+)"', html or "", re.I)
    return m.group(1).strip() if m else None

def _prime_csrf(sess: requests.Session, lang: str) -> tuple[str | None, dict]:
    """
    CSRF olishga urinadi:
    1) /sanctum/csrf-cookie
    2) /{lang}/home HTML meta
    """
    debug = {"csrf_from": None, "home_status": None, "csrf_status": None}

    # 1) Sanctum usuli
    try:
        csrf_url = f"{ETICKET_BASE}/sanctum/csrf-cookie"
        r_csrf = sess.get(csrf_url, timeout=20, headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": f"{ETICKET_BASE}/{lang}/home",
        })
        debug["csrf_status"] = r_csrf.status_code
        xsrf = _cookie_xsrf(sess)
        if xsrf:
            debug["csrf_from"] = "cookie:/sanctum/csrf-cookie"
            return xsrf, debug
    except Exception:
        pass

    # 2) Home HTML’dan meta token olish
    home_url = f"{ETICKET_BASE}/{lang}/home"
    r0 = sess.get(home_url, timeout=20, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "uz,en;q=0.9,ru;q=0.8",
    })
    debug["home_status"] = r0.status_code

    xsrf = _cookie_xsrf(sess)
    if xsrf:
        debug["csrf_from"] = "cookie:/home"
        return xsrf, debug

    meta = _html_csrf_token(r0.text or "")
    if meta:
        # ba’zi backendlar meta tokenni X-CSRF-TOKEN sifatida qabul qiladi
        debug["csrf_from"] = "meta:/home"
        return meta, debug

    return None, debug


@app.post("/api/trains")
def api_trains():
    data = request.get_json(force=True) or {}
    dep  = str(data.get("dep", "")).strip()
    arv  = str(data.get("arv", "")).strip()
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

        token, dbg = _prime_csrf(sess, lang)

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": ETICKET_BASE,
            "Referer": f"{ETICKET_BASE}/{lang}/home",
        }

        # 2 xil token headerni ham berib ko‘ramiz (qaysi biri kerak bo‘lsa ishlaydi)
        if token:
            headers["X-XSRF-TOKEN"] = token
            headers["X-CSRF-TOKEN"] = token

        r = sess.post(ETICKET_API, json=payload, headers=headers, timeout=25)

        if r.status_code >= 400:
            return jsonify({
                "ok": False,
                "status": r.status_code,
                "csrf_debug": dbg,
                "has_token": bool(token),
                "set_cookies": {k: v for k, v in sess.cookies.get_dict().items()},
                "body": (r.text or "")[:500]
            }), 502

        return jsonify(r.json())

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 502