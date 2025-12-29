#!/usr/bin/env python3
"""
AFO Wallet Service - API Wallet을 위한 독립 서비스
Phase 20: API Wallet & Vault 흡수
"""

import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from AFO.api.routes.wallet import wallet_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup validation
    try:
        kms_type = os.getenv("API_WALLET_KMS", "local").strip().lower()
        if kms_type == "vault":
            print("🔍 Validating vault connectivity on startup...")
            from AFO.api_wallet import APIWallet
            test_wallet = APIWallet()
            if not test_wallet.use_vault:
                raise RuntimeError("Vault mode required but vault initialization failed")
            print("✅ Vault connectivity validated")
    except Exception as e:
        print(f"❌ Startup validation failed: {e}")
        # Fail-closed: vault 모드인데 vault 연결 실패 시 애플리케이션 시작 자체를 막음
        if os.getenv("API_WALLET_KMS", "local").strip().lower() == "vault":
            print("💥 Vault mode startup failed - exiting")
            raise e
        else:
            print("⚠️  Local mode - continuing despite vault issues")

    yield

    # Shutdown
    pass

app = FastAPI(
    title="AFO Wallet Service",
    description="API Wallet 서비스 - 키 관리 및 보안",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "wallet-service"}

# Wallet routes
app.include_router(wallet_router)

if __name__ == "__main__":
    uvicorn.run(
        "wallet_server:app",
        host="0.0.0.0",
        port=8011,
        reload=False
    )
