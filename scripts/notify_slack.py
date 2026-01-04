import os, json, sys
from datetime import datetime
from urllib import request

WEBHOOK = os.getenv("AFO_SLACK_WEBHOOK_URL", "").strip()
SENDER = os.getenv("AFO_NOTIFY_SENDER", "AFO Kingdom").strip()
TAG = os.getenv("AFO_NOTIFY_TAG", "").strip()

def post(payload: dict):
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(WEBHOOK, data=data, headers={"Content-Type":"application/json"})
    with request.urlopen(req, timeout=10) as r:
        r.read()

def main():
    if not WEBHOOK:
        print("AFO_SLACK_WEBHOOK_URL is empty", file=sys.stderr)
        sys.exit(2)

    title = sys.argv[1] if len(sys.argv) > 1 else "Notification"
    body = sys.argv[2] if len(sys.argv) > 2 else ""
    extra = sys.argv[3] if len(sys.argv) > 3 else ""

    ts = datetime.now().isoformat(timespec="seconds")
    text = f"{TAG} *{title}*\n{body}\n{extra}\n_{ts}_".strip()

    payload = {"username": SENDER, "text": text}
    post(payload)
    print("ok")

if __name__ == "__main__":
    main()
