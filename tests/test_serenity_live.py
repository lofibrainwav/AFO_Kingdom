import sys

import requests


def test_serenity_live():
    url = "http://localhost:8010/api/serenity/create"
    payload = {
        "prompt": "Create a simple React button component with a blue gradient background and white text. It should say 'Serenity Button'."
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()

        code = data.get("code", "")
        if "export default function" in code or "const" in code:
            pass
        else:
            sys.exit(1)

    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    test_serenity_live()
