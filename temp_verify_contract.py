import json
import time
import urllib.request

time.sleep(1)
u = "http://127.0.0.1:8010/api/health/comprehensive"
try:
    with urllib.request.urlopen(u) as f:
        d = json.loads(f.read().decode())

    print("== health snapshot ==")
    print(f"has_organs: {isinstance(d.get('organs'), dict)}")
    print(f"organs_count: {len(d.get('organs') or {})}")
    print(f"has_security: {bool(d.get('security'))}")
    print(f"has_contract_v2: {bool(d.get('contract_v2'))}")
    print(
        f"contract_expected: {(d.get('contract_v2') or {}).get('organs_keys_expected')}"
    )
    # Handle breakdown key variation (breakdown vs trinity_breakdown)
    b = d.get("breakdown") or d.get("trinity_breakdown")
    print(f"has_breakdown: {bool(b)}")
    print(f"breakdown_keys: {sorted(list(b.keys())) if b else []}")
    print(f"iccls_gap: {d.get('iccls_gap')}")
    print(f"sentiment: {d.get('sentiment')}")

except Exception as e:
    print(f"Error: {e}")
