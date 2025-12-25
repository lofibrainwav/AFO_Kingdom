import psycopg2
import redis
import requests

print("=== TRUTH VERIFICATION START ===")

# 1. Database Verification
print("\n[1] Checking PostgreSQL (15432)...")
try:
    conn = psycopg2.connect(
        host="localhost",
        port=15432,
        dbname="afo_memory",
        user="afo",
        password="afo_secret_change_me",
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    print(f"✅ SUCCESS: Connected to DB. Version: {version}")
    conn.close()
except Exception as e:
    print(f"❌ FAILURE: Database Connection Failed: {e}")

# 2. Redis Verification
print("\n[2] Checking Redis (6379)...")
try:
    r = redis.Redis(host="localhost", port=6379, socket_timeout=2)
    response = r.ping()
    print(f"✅ SUCCESS: Redis PING response: {response}")
except Exception as e:
    print(f"❌ FAILURE: Redis Connection Failed: {e}")

# 3. API Verification
print("\n[3] Checking Soul Engine (8010)...")
try:
    url = "http://localhost:8010/api/system/kingdom-status"
    res = requests.get(url, timeout=2)
    if res.status_code == 200:
        print(f"✅ SUCCESS: API Status 200. Data sample: {str(res.json())[:100]}...")
    else:
        print(f"❌ FAILURE: API returned {res.status_code}")
except Exception as e:
    print(f"❌ FAILURE: API Unreachable: {e}")

# 4. Dashboard Verification
print("\n[4] Checking Dashboard (3000)...")
try:
    url = "http://localhost:3000"
    res = requests.get(url, timeout=2)
    if res.status_code == 200:
        if (
            "AFO Kingdom" in res.text
            or "Trinity Score" in res.text
            or "<html" in res.text
        ):
            print(f"✅ SUCCESS: Dashboard responding (Length: {len(res.text)} chars)")
        else:
            print(
                f"⚠️ WARNING: Dashboard 200 OK but content suspicious (Length: {len(res.text)})"
            )
    else:
        print(f"❌ FAILURE: Dashboard returned {res.status_code}")
except Exception as e:
    print(f"❌ FAILURE: Dashboard Unreachable: {e}")

print("\n=== TRUTH VERIFICATION END ===")
