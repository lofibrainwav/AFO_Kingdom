# Trinity Score: 90.0 (Established by Chancellor)
# ⚔️ 점수는 Truth Engine (scripts/calculate_trinity_score.py)에서만 계산됩니다.
# LLM은 consult_the_lens MCP 도구를 통해 점수를 확인하세요.
# 이 파일은 AFO 왕국의 眞善美孝 철학을 구현합니다

"""
Input Server - 사령관의 입력 통로 (input.brnestrm.com)

역할: API 키 및 설정 입력을 받아 API Wallet에 저장
기능:
1. HTML 폼 (API 키 입력)
2. API Wallet으로 전송
3. PostgreSQL preferences 테이블 연동

포트: 4200
위치: 胃 (Stomach) - 11장기 시스템

설계: 2025-11-06
작성자: 좌의정 Claude
"""

from __future__ import annotations

import hashlib
import os
import re
from datetime import datetime
from typing import Any

import httpx
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

# Input Storage 모듈 import
try:
    from input_storage import get_input_history, get_input_statistics, save_input_to_db

    INPUT_STORAGE_AVAILABLE = True
except ImportError:
    INPUT_STORAGE_AVAILABLE = False
    print("⚠️  WARNING: input_storage module not available. PostgreSQL storage disabled.")

# FastAPI 앱 초기화
app = FastAPI(
    title="AFO Input Server",
    description="API 키 입력 및 관리 서버 (胃 Stomach)",
    version="1.0.0",
)

# API Wallet 서버 URL (중앙 설정 사용 - Phase 1 리팩토링)
try:
    from AFO..config.settings import import get_settings

    settings = get_settings()
    API_WALLET_URL = settings.API_WALLET_URL
except ImportError:
    API_WALLET_URL = os.getenv("API_WALLET_URL", "http://localhost:8000")

# 환경 변수 파싱 패턴
ENV_PATTERNS = [
    (r"^([A-Z_][A-Z0-9_]*)\s*=\s*(.+)$", "key_value"),
    (r"^([A-Z_][A-Z0-9_]*)\s*:\s*(.+)$", "key_colon"),
    (r'"([A-Z_][A-Z0-9_]*)":\s*"([^"]+)"', "json"),
    (r'^([A-Z_][A-Z0-9_]*)\s+"([^"]+)"$', "key_quoted"),
]

# 서비스 매핑
SERVICE_MAPPING = {
    "OPENAI_API_KEY": "openai",
    "ANTHROPIC_API_KEY": "anthropic",
    "N8N_URL": "n8n",
    "API_YUNGDEOK": "n8n",
    "N8N_API_TOKEN": "n8n",
    "REDIS_URL": "redis",
    "POSTGRES_PASSWORD": "postgres",
    "DISCORD_BOT_TOKEN": "discord",
    "CLOUDFLARE_API_TOKEN": "cloudflare",
    "HETZNER_API_TOKEN": "hetzner",
    "GITHUB_TOKEN": "github",
}


def parse_env_text(text: str) -> list[tuple[str, str, str]]:
    """긴 텍스트에서 환경 변수 파싱"""
    parsed = []
    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        for pattern, _ in ENV_PATTERNS:
            match = re.match(pattern, line)
            if match:
                key, value = match.groups()
                if (value.startswith('"') and value.endswith('"')) or (
                    value.startswith("'") and value.endswith("'")
                ):
                    value = value[1:-1]
                service = SERVICE_MAPPING.get(key, "other")
                parsed.append((key, value.strip(), service))
                break

    return parsed


# Health check endpoint
@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy", "service": "AFO Input Server", "organ": "胃 (Stomach)"}


@app.get("/", response_class=HTMLResponse)
async def home_page(
    request: Request, success: str | None = None, error: str | None = None
) -> HTMLResponse:
    """
    홈페이지 - API 키 입력 폼

    Query Parameters:
    - success: 성공 메시지
    - error: 에러 메시지
    """
    # 현재 등록된 API 키 목록 조회
    api_keys = []
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{API_WALLET_URL}/api/wallet/list")
            if response.status_code == 200:
                data = response.json()
                api_keys = data.get("keys", [])
    except Exception as e:
        print(f"⚠️  API Wallet 조회 실패: {e}")

    # HTML 폼 렌더링
    html_content = _get_home_template(success, error, api_keys)
    return HTMLResponse(content=html_content)


def _get_home_template(
    success: str | None, error: str | None, api_keys: list[dict[str, Any]]
) -> str:
    """홈페이지 HTML 템플릿 생성 (Beauty refactoring)"""

    # 키 리스트 HTML 생성
    if api_keys:
        keys_html = "".join(
            [
                f"""
                <div class="key-item">
                    <div>
                        <div class="key-name">{key.get("name", "Unknown")}</div>
                        <div style="font-size: 12px; color: #999; margin-top: 4px;">
                            등록: {key.get("created_at", "Unknown")[:10]}
                        </div>
                    </div>
                    <div class="key-provider">{key.get("provider", "Unknown")}</div>
                </div>
                """
                for key in api_keys
            ]
        )
    else:
        keys_html = '<p style="color: #999; text-align: center;">아직 등록된 키가 없습니다</p>'

    return f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AFO Input Server - API 키 관리</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 600px;
            width: 100%;
            padding: 40px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 14px;
        }}
        .header .organ {{
            font-size: 48px;
            margin-bottom: 10px;
        }}
        .form-group {{
            margin-bottom: 20px;
        }}
        .form-group label {{
            display: block;
            color: #333;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 14px;
        }}
        .form-group input,
        .form-group select,
        .form-group textarea {{
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }}
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {{
            outline: none;
            border-color: #667eea;
        }}
        .form-group .hint {{
            font-size: 12px;
            color: #999;
            margin-top: 5px;
        }}
        .submit-btn {{
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .submit-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }}
        .submit-btn:active {{
            transform: translateY(0);
        }}
        .message {{
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        .message.success {{
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}
        .message.error {{
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
        .key-list {{
            margin-top: 30px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
        }}
        .key-list h2 {{
            color: #333;
            font-size: 20px;
            margin-bottom: 15px;
        }}
        .key-item {{
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .key-item .key-name {{
            font-weight: 600;
            color: #333;
        }}
        .key-item .key-provider {{
            font-size: 12px;
            color: #666;
            background: white;
            padding: 4px 8px;
            border-radius: 4px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="organ">🍽️</div>
            <h1>AFO Input Server</h1>
            <p class="subtitle">胃 (Stomach) - API 키 입력 및 관리</p>
        </div>

        {'<div class="message success">✅ ' + success + "</div>" if success else ""}
        {'<div class="message error">❌ ' + error + "</div>" if error else ""}

        <!-- 탭 전환 버튼 -->
        <div style="display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #e0e0e0;">
            <button type="button" onclick="showForm('single')" id="tab-single" style="flex: 1; padding: 12px; background: #667eea; color: white; border: none; border-radius: 8px 8px 0 0; cursor: pointer; font-weight: 600;">🔑 하나씩 입력</button>
            <button type="button" onclick="showForm('bulk')" id="tab-bulk" style="flex: 1; padding: 12px; background: #e0e0e0; color: #666; border: none; border-radius: 8px 8px 0 0; cursor: pointer; font-weight: 600;">📋 대량 입력 (복붙)</button>
        </div>

        <!-- 하나씩 입력 폼 -->
        <div id="form-single">
        <form action="/add_key" method="post">
            <div class="form-group">
                <label for="name">API 키 이름 *</label>
                <input type="text" id="name" name="name" required placeholder="예: openai_primary">
                <div class="hint">영문, 숫자, 언더스코어만 사용 가능</div>
            </div>

            <div class="form-group">
                <label for="provider">제공자 *</label>
                <select id="provider" name="provider" required>
                    <option value="">-- 선택하세요 --</option>
                    <option value="openai">OpenAI</option>
                    <option value="anthropic">Anthropic (Claude)</option>
                    <option value="google">Google (Gemini)</option>
                    <option value="n8n">n8n</option>
                    <option value="github">GitHub</option>
                    <option value="other">기타</option>
                </select>
            </div>

            <div class="form-group">
                <label for="key">API 키 *</label>
                <textarea id="key" name="key" required placeholder="sk-..." rows="3"></textarea>
                <div class="hint">암호화되어 안전하게 저장됩니다 (AES-256)</div>
            </div>

            <div class="form-group">
                <label for="description">설명 (선택)</label>
                <input type="text" id="description" name="description" placeholder="예: 프로덕션 환경용">
            </div>

            <button type="submit" class="submit-btn">🔐 API 키 저장</button>
        </form>
        </div>

        <!-- 대량 입력 폼 -->
        <div id="form-bulk" style="display: none;">
        <form action="/bulk_import" method="post" onsubmit="return confirm('정말로 모든 API 키를 저장하시겠습니까?');">
            <div class="form-group">
                <label for="bulk_text">긴 문자열 복붙 (KEY=VALUE 형식) *</label>
                <textarea id="bulk_text" name="bulk_text" required placeholder="OPENAI_API_KEY=sk-proj-xxxxx&#10;ANTHROPIC_API_KEY=sk-ant-xxxxx&#10;N8N_URL=https://n8n.brnestrm.com&#10;API_YUNGDEOK=eyJhbGciOiJIUzI1NiIs...&#10;..." rows="15" style="font-family: monospace; font-size: 12px;"></textarea>
                <div class="hint">모든 환경 변수를 한 번에 복붙하세요. 자동으로 파싱하고 검증해서 저장합니다.</div>
            </div>
            <button type="submit" class="submit-btn" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">🚀 대량 저장 시작</button>
        </form>
        </div>

        <script>
        function showForm(type) {{
            if (type === 'single') {{
                document.getElementById('form-single').style.display = 'block';
                document.getElementById('form-bulk').style.display = 'none';
                document.getElementById('tab-single').style.background = '#667eea';
                document.getElementById('tab-single').style.color = 'white';
                document.getElementById('tab-bulk').style.background = '#e0e0e0';
                document.getElementById('tab-bulk').style.color = '#666';
            }} else {{
                document.getElementById('form-single').style.display = 'none';
                document.getElementById('form-bulk').style.display = 'block';
                document.getElementById('tab-single').style.background = '#e0e0e0';
                document.getElementById('tab-single').style.color = '#666';
                document.getElementById('tab-bulk').style.background = '#667eea';
                document.getElementById('tab-bulk').style.color = 'white';
            }}
        }}
        </script>

        <div class="key-list">
            <h2>📋 등록된 API 키 ({len(api_keys)}개)</h2>
            {keys_html}
        </div>

        <div class="footer">
            <p>AFO Kingdom - 弘益人間 (Hongik Ingan)</p>
            <p style="margin-top: 5px;">眞善美孝 - Truth, Goodness, Beauty, Serenity</p>
        </div>
    </div>
</body>
</html>
    """


@app.post("/add_key", response_model=None)
async def add_api_key(
    name: str = Form(...),
    provider: str = Form(...),
    key: str = Form(...),
    description: str | None = Form(None),
) -> RedirectResponse | JSONResponse:
    """
    API 키 추가 (API Wallet으로 전송 + PostgreSQL 저장)

    Form Parameters:
    - name: API 키 이름
    - provider: 제공자
    - key: API 키 값
    - description: 설명 (선택)
    """
    try:
        # 1. API Wallet으로 전송 (암호화 저장)
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{API_WALLET_URL}/api/wallet/add",
                json={
                    "name": name,
                    "provider": provider,
                    "key": key,
                    "description": description or "",
                    "metadata": {
                        "source": "input_server",
                        "timestamp": datetime.utcnow().isoformat(),
                    },
                },
            )

            if response.status_code != 200:
                error_detail = response.json().get("detail", "Unknown error")
                print(f"❌ API 키 저장 실패: {error_detail}")
                return RedirectResponse(url=f"/?error=저장 실패: {error_detail}", status_code=303)

        # 2. PostgreSQL에 메타데이터 저장 (API 키는 제외, 善 - Goodness 원칙)
        if INPUT_STORAGE_AVAILABLE:
            # API 키의 해시값만 저장 (보안)
            key_hash = hashlib.sha256(key.encode()).hexdigest()[:16]

            save_input_to_db(
                category="api_key",
                key=f"api_key_{name}_{key_hash}",
                value=None,  # API 키 값은 저장하지 않음 (보안)
                metadata={
                    "name": name,
                    "provider": provider,
                    "description": description,
                    "key_hash": key_hash,  # 해시만 저장
                    "source": "input_server",
                },
                confidence=1.0,
                source="input_server",
            )

        print(f"✅ API 키 저장 성공: {name} ({provider})")
        return RedirectResponse(
            url=f"/?success=API 키 '{name}'이(가) 성공적으로 저장되었습니다",
            status_code=303,
        )

    except httpx.ConnectError:
        print(f"❌ API Wallet 서버 연결 실패 ({API_WALLET_URL})")
        return RedirectResponse(
            url="/?error=API Wallet 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.",
            status_code=303,
        )
    except Exception as e:
        print(f"❌ API 키 저장 중 에러: {e}")
        return RedirectResponse(url=f"/?error=저장 중 오류가 발생했습니다: {e!s}", status_code=303)


@app.get("/api/status")
async def api_status() -> dict[str, Any]:
    """
    Input Server 상태 조회

    Returns:
        JSON: 서버 상태 정보
    """
    # API Wallet 연결 확인
    api_wallet_connected = False
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f"{API_WALLET_URL}/health")
            api_wallet_connected = response.status_code == 200
    except Exception:
        pass

    # PostgreSQL 연결 확인
    postgres_connected = False
    input_stats: dict[str, Any] = {}
    if INPUT_STORAGE_AVAILABLE:
        try:
            stats = get_input_statistics()
            if stats:
                postgres_connected = True
                input_stats = stats
        except Exception:
            pass

    return {
        "status": "healthy",
        "service": "AFO Input Server",
        "organ": "胃 (Stomach)",
        "port": 4200,
        "api_wallet_url": API_WALLET_URL,
        "api_wallet_connected": api_wallet_connected,
        "postgres_connected": postgres_connected,
        "input_statistics": input_stats,
        "timestamp": datetime.utcnow().isoformat(),
    }


async def _is_api_server_available(url: str) -> bool:
    """API Wallet 서버 가용성 확인"""
    async with httpx.AsyncClient(timeout=2.0) as client:
        try:
            resp = await client.get(f"{url}/health")
            return resp.status_code == 200
        except Exception:
            return False


async def _import_single_key(
    name: str, value: str, service: str, wallet: Any, api_server_url: str | None
) -> str:
    """단일 키 임포트 수행 (Success, Skipped, or Error)"""
    # 1. API Wallet 직접 저장 시도
    if wallet:
        try:
            if wallet.get(name, decrypt=False):
                return "skipped"
            wallet.add(
                name=name,
                api_key=value,
                key_type="api",
                read_only=True,
                service=service,
                description=f"Bulk import: {name}",
            )
            return "success"
        except Exception as e:
            if "already exists" in str(e).lower():
                return "skipped"
            return str(e)

    # 2. API Wallet 서버 저장 시도 (Fallback)
    if api_server_url:
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                # 존재 여부 확인 (중복 방지)
                chk = await client.get(f"{api_server_url}/api/wallet/get/{name}", timeout=2.0)
                if chk.status_code == 200:
                    return "skipped"

                # 추가 요청 (POST)
                resp = await client.post(
                    f"{api_server_url}/api/wallet/add",
                    json={
                        "name": name,
                        "api_key": value,
                        "key_type": "api",
                        "read_only": True,
                        "service": service,
                        "description": f"Bulk import: {name}",
                    },
                )
                if resp.status_code == 200:
                    return "success"

                # 에러 응답 처리
                err_detail = resp.json().get("detail", "Unknown error")
                return "skipped" if "already exists" in err_detail.lower() else err_detail
            except Exception as e:
                # 네트워크 에러 등
                return str(e)

    return "API Wallet unavailable"


@app.post("/bulk_import")
async def bulk_import(bulk_text: str = Form(...)) -> RedirectResponse:
    """대량 환경 변수 임포트 (Refactored)"""
    try:
        parsed = parse_env_text(bulk_text)
        if not parsed:
            return RedirectResponse(url="/?error=파싱된 환경 변수가 없습니다.", status_code=303)

        # Wallet 인스턴스 준비
        wallet = None
        try:
            from api_wallet import APIWallet

            wallet = APIWallet()
        except Exception:
            pass

        server_url = API_WALLET_URL if await _is_api_server_available(API_WALLET_URL) else None

        counts = {"success": 0, "skipped": 0, "failed": 0}
        failed_names = []

        for name, value, service in parsed:
            res = await _import_single_key(name, value, service, wallet, server_url)
            if res == "success":
                counts["success"] += 1
            elif res == "skipped":
                counts["skipped"] += 1
            else:
                counts["failed"] += 1
                failed_names.append(f"{name}({res})")

        # 요약 메시지 생성
        summary = []
        if counts["success"]:
            summary.append(f"✅ {counts['success']}개 성공")
        if counts["skipped"]:
            summary.append(f"⚠️ {counts['skipped']}개 스킵")
        if counts["failed"]:
            summary.append(f"❌ {counts['failed']}개 실패")

        result_msg = " | ".join(summary)
        if failed_names:
            result_msg += (
                f" (실패: {', '.join(failed_names[:3])}{'...' if len(failed_names) > 3 else ''})"
            )

        return RedirectResponse(url=f"/?success={result_msg}", status_code=303)

    except Exception as e:
        return RedirectResponse(url=f"/?error=임포트 중 오류: {e!s}", status_code=303)


@app.get("/api/history", response_model=None)
async def get_history(
    category: str | None = None, limit: int = 100
) -> dict[str, Any] | JSONResponse:
    """
    Input 히스토리 조회

    Query Parameters:
    - category: 카테고리 필터 (선택)
    - limit: 최대 조회 개수 (기본값: 100)

    Returns:
        JSON: Input 히스토리 리스트
    """
    if not INPUT_STORAGE_AVAILABLE:
        return JSONResponse(status_code=503, content={"error": "PostgreSQL storage not available"})

    try:
        history = get_input_history(category=category, limit=limit)
        return {"status": "success", "count": len(history), "history": history}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# Main entry point
if __name__ == "__main__":
    import uvicorn

    # Phase 2-4: settings 사용
    try:
        from AFO..config.settings import import get_settings

        settings = get_settings()
        port = settings.INPUT_SERVER_PORT
        host = settings.INPUT_SERVER_HOST
    except ImportError:
        port = int(os.getenv("INPUT_SERVER_PORT", "4200"))
        host = os.getenv("INPUT_SERVER_HOST", "127.0.0.1")

    print("=" * 60)
    print("🍽️  AFO Input Server - 胃 (Stomach)")
    print("=" * 60)
    print(f"Port: {port}")
    print(f"Host: {host}")
    print(f"API Wallet URL: {API_WALLET_URL}")
    print("=" * 60)
    print()

    uvicorn.run(app, host=host, port=port, log_level="info")
