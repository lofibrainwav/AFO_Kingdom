#!/usr/bin/env python3
"""Antigravity 상태 확인 스크립트"""

try:
    from AFO.config.antigravity import antigravity
    print("✅ Antigravity loaded successfully")
    print(f"ENVIRONMENT: {antigravity.ENVIRONMENT}")
    print(f"AUTO_DEPLOY: {antigravity.AUTO_DEPLOY}")
    print(f"DRY_RUN_DEFAULT: {antigravity.DRY_RUN_DEFAULT}")
except Exception as e:
    print(f"❌ Antigravity error: {e}")

try:
    from AFO.chancellor_graph import chancellor_graph
    print("✅ Chancellor Graph loaded successfully")
except Exception as e:
    print(f"❌ Chancellor Graph error: {e}")

try:
    from AFO.api_server import app
    print("✅ API Server app loaded successfully")
except Exception as e:
    print(f"❌ API Server error: {e}")