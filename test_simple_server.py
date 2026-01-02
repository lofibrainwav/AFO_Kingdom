#!/usr/bin/env python3
"""간단한 테스트 서버"""

from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok", "message": "Simple test server is running"}


@app.get("/chancellor/health")
async def chancellor_health():
    return {"status": "ok", "message": "Chancellor health endpoint"}


if __name__ == "__main__":
    import uvicorn
    print("Starting simple test server on port 8010...")
    uvicorn.run(app, host="127.0.0.1", port=8010)
