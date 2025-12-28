#!/usr/bin/env python3
"""
AFO Wallet Service - API Wallet을 위한 독립 서비스
Phase 20: API Wallet & Vault 흡수
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from AFO.api.routes.wallet import wallet_router

app = FastAPI(
    title="AFO Wallet Service",
    description="API Wallet 서비스 - 키 관리 및 보안",
    version="1.0.0"
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
