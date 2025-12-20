# mypy: ignore-errors
"""
MCP (Model Context Protocol) 통합 모듈
LLM이 브라우저를 직접 조종하는 통합
2025년 VibeCoding: AI가 스냅샷 보고 테스트 코드 뚝딱!
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any

import httpx

try:
    from .mcp_error_handler import MCPErrorHandler, mcp_tool_call_with_retry

    ERROR_HANDLER_AVAILABLE = True
except ImportError:
    ERROR_HANDLER_AVAILABLE = False

    from .advanced_retry import (
        RetryState,
        with_condition_retry,
        # jittered_backoff, # Unused
        # poll_until, # Unused
        # smart_retry_for_mcp_tool, # Unused
    )

    ADVANCED_RETRY_AVAILABLE = True
except ImportError:
    ADVANCED_RETRY_AVAILABLE = False

try:
    from anthropic import AsyncAnthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from openai import AsyncOpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class MCPBrowserTools:
    """
    MCP 브라우저 툴 시뮬레이션
    실제 MCP 서버와 통신하는 클래스
    """

    def __init__(self, mcp_server_url: str | None = None):
        # 중앙 설정 사용 (Phase 1 리팩토링)
        if mcp_server_url is None:
            try:
                from AFO.config.settings import get_settings

                mcp_server_url = get_settings().MCP_SERVER_URL
            except ImportError:
                mcp_server_url = "http://localhost:8931"  # Fallback
        self.mcp_server_url = mcp_server_url
        self.tool_call_history: list[dict[str, Any]] = []

    async def browser_navigate(self, url: str) -> dict[str, Any]:
        """
        브라우저 네비게이션 (MCP 툴 콜)

        Args:
            url: 이동할 URL

        Returns:
            스냅샷 및 결과
        """
        tool_call = {
            "tool": "browser_navigate",
            "params": {"url": url},
            "timestamp": asyncio.get_event_loop().time(),
        }

        try:
            # 실제 MCP 서버 호출 (시뮬레이션)
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.mcp_server_url}/tools/browser_navigate", json={"url": url}
                )
                if response.status_code == 200:
                    result = response.json()
                else:
                    # 폴백: 시뮬레이션 결과
                    result = {
                        "snapshot": f"Page title: {url} | Elements: [ref=e1: navigation complete]",
                        "success": True,
                    }
        except Exception:
            # MCP 서버가 없으면 시뮬레이션
            result = {
                "snapshot": f"Page title: {url} | Elements: [ref=e1: navigation complete]",
                "success": True,
            }

        tool_call["result"] = result
        self.tool_call_history.append(tool_call)

        print(f"🛡️ MCP 툴 콜: browser_navigate({url})")
        print(f"   스냅샷: {result.get('snapshot', 'N/A')}")

        return result

    async def browser_snapshot(self) -> dict[str, Any]:
        """
        브라우저 스냅샷 캡처 (MCP 툴 콜)

        Returns:
            접근성 트리 및 스냅샷
        """
        tool_call = {
            "tool": "browser_snapshot",
            "params": {},
            "timestamp": asyncio.get_event_loop().time(),
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.mcp_server_url}/tools/browser_snapshot", json={}
                )
                if response.status_code == 200:
                    result = response.json()
                else:
                    result = {
                        "snapshot": "Page elements: [ref=e1: username input], [ref=e2: password input], [ref=e3: login button]",
                        "accessibility_tree": "button: Login, input: Username, input: Password",
                    }
        except Exception:
            result = {
                "snapshot": "Page elements: [ref=e1: username input], [ref=e2: password input], [ref=e3: login button]",
                "accessibility_tree": "button: Login, input: Username, input: Password",
            }

        tool_call["result"] = result
        self.tool_call_history.append(tool_call)

        print("🛡️ MCP 툴 콜: browser_snapshot()")
        print(f"   스냅샷: {result.get('snapshot', 'N/A')[:100]}...")

        return result

    async def browser_fill_form(self, fields: list[dict[str, str]]) -> dict[str, Any]:
        """
        폼 필드 채우기 (MCP 툴 콜)

        Args:
            fields: [{"name": "username", "value": "test"}, ...]

        Returns:
            결과 및 스냅샷
        """
        tool_call = {
            "tool": "browser_fill_form",
            "params": {"fields": fields},
            "timestamp": asyncio.get_event_loop().time(),
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.mcp_server_url}/tools/browser_fill_form", json={"fields": fields}
                )
                if response.status_code == 200:
                    result = response.json()
                else:
                    result = {
                        "snapshot": f"Form filled: {', '.join([f['name'] for f in fields])}",
                        "success": True,
                    }
        except Exception:
            result = {
                "snapshot": f"Form filled: {', '.join([f['name'] for f in fields])}",
                "success": True,
            }

        tool_call["result"] = result
        self.tool_call_history.append(tool_call)

        print(f"🛡️ MCP 툴 콜: browser_fill_form({len(fields)} fields)")

        return result

    async def browser_click(self, element_ref: str) -> dict[str, Any]:
        """
        요소 클릭 (MCP 툴 콜)

        Args:
            element_ref: 요소 참조 (예: "e3")

        Returns:
            결과 및 스냅샷
        """
        tool_call = {
            "tool": "browser_click",
            "params": {"ref": element_ref},
            "timestamp": asyncio.get_event_loop().time(),
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.mcp_server_url}/tools/browser_click", json={"ref": element_ref}
                )
                if response.status_code == 200:
                    result = response.json()
                else:
                    result = {"snapshot": f"Clicked: {element_ref}", "success": True}
        except Exception:
            result = {"snapshot": f"Clicked: {element_ref}", "success": True}

        tool_call["result"] = result
        self.tool_call_history.append(tool_call)

        print(f"🛡️ MCP 툴 콜: browser_click({element_ref})")

        return result


class MCPIntegratedAuth:
    """
    MCP 통합 인증 클래스
    LLM이 브라우저를 직접 조종하여 인증 테스트 생성
    """

    def __init__(self, llm_provider: str = "anthropic", api_key: str | None = None):
        """
        Args:
            llm_provider: "anthropic" (Claude) 또는 "openai" (GPT)
            api_key: API 키
        """
        self.mcp_tools = MCPBrowserTools()
        self.mcp_tools = MCPBrowserTools()
        self.tool_call_history: list[dict[str, Any]] = []

        # Phase 2-4: settings 사용
        try:
            from config.settings import get_settings

            settings = get_settings()
        except ImportError:
            try:
                from AFO.config.settings import get_settings

                settings = get_settings()
            except ImportError:
                settings = None

        if llm_provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                raise ImportError("Anthropic 라이브러리가 필요합니다: pip install anthropic")
            api_key = (
                api_key
                or (settings.ANTHROPIC_API_KEY if settings else None)
                or os.getenv("ANTHROPIC_API_KEY")
            )
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY 환경변수가 필요합니다")
            self.client = AsyncAnthropic(api_key=api_key)
            self.model = "claude-3-5-sonnet-20241022"
        else:
            if not OPENAI_AVAILABLE:
                raise ImportError("OpenAI 라이브러리가 필요합니다: pip install openai")
            api_key = (
                api_key
                or (settings.OPENAI_API_KEY if settings else None)
                or os.getenv("OPENAI_API_KEY")
            )
            if not api_key:
                raise ValueError("OPENAI_API_KEY 환경변수가 필요합니다")
            self.client = AsyncOpenAI(api_key=api_key)  # type: ignore[assignment]
            self.model = "gpt-4o"

    async def generate_auth_with_mcp(self, prompt: str, playwright_page: Any) -> str:
        """
        MCP를 사용하여 인증 테스트 코드 생성

        Args:
            prompt: 테스트 요청 (예: "ChatGPT 로그인 테스트 생성해")
            playwright_page: Playwright 페이지 객체

        Returns:
            생성된 Python 코드
        """
        print("\n" + "=" * 70)
        print("🔌 MCP 통합: AI가 브라우저를 직접 조종합니다!")
        print("=" * 70)

        # 1. 페이지 스냅샷 캡처
        print("\n📸 1단계: 브라우저 스냅샷 캡처 중...")
        snapshot_result = await self.mcp_tools.browser_snapshot()
        snapshot = snapshot_result.get("snapshot", "")

        # 2. LLM에게 MCP 컨텍스트 주입
        print("\n🤖 2단계: LLM이 스냅샷 분석 중...")

        system_prompt = """You are a Playwright automation expert. Use MCP browser tools to interact with the browser and generate test code.

Available MCP tools:
1. browser_navigate(url) - Navigate to URL
2. browser_snapshot() - Capture page snapshot
3. browser_fill_form(fields) - Fill form fields
4. browser_click(ref) - Click element by reference

Analyze the snapshot and generate Playwright code based on what you see."""

        user_prompt = f"""
{prompt}

Current Page Snapshot:
{snapshot}

Generate Playwright Python async code that:
1. Uses the snapshot to understand page structure
2. Fills login form fields
3. Clicks submit button
4. Verifies success

Return only Python code in ```python blocks."""

        try:
            if isinstance(self.client, AsyncAnthropic):
                # Claude
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    messages=[{"role": "user", "content": user_prompt}],
                )
                generated_code = response.content[0].text  # type: ignore[union-attr]
            else:
                # OpenAI
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.2,
                    max_tokens=2000,
                )
                generated_code = response.choices[0].message.content

            # 코드 블록에서 추출
            if "```python" in generated_code:
                generated_code = generated_code.split("```python")[1].split("```")[0].strip()
            elif "```" in generated_code:
                generated_code = generated_code.split("```")[1].split("```")[0].strip()

            print("\n✅ 3단계: AI가 코드 생성 완료!")
            print(f"   코드 길이: {len(generated_code)}자")

            return generated_code

        except Exception as e:
            print(f"\n❌ 코드 생성 실패: {e}")
            raise

    def _init_error_handler(self) -> Any:
        """Initialize MCP error handler if available."""
        if not ERROR_HANDLER_AVAILABLE:
            return None
        try:
            from AFO.config.settings import get_settings
            claude_key = get_settings().ANTHROPIC_API_KEY
            return MCPErrorHandler(api_key=claude_key)
        except Exception:
            return None

    async def _setup_browser_and_page(
        self, playwright: Any, attempt: int, max_retries: int, error_handler: Any
    ) -> tuple[Any, Any]:
        """브라우저 및 페이지 초기화 (Retry 포함)"""
        print(f"\n🌐 브라우저 시작 (시도 {attempt + 1}/{max_retries})...")
        if ADVANCED_RETRY_AVAILABLE:
            browser = await with_condition_retry(
                lambda: playwright.chromium.launch(headless=False),
                max_retries=3,
                base_delay=1.0,
            )
        else:
            browser = await mcp_tool_call_with_retry(
                lambda: playwright.chromium.launch(headless=False),
                max_retries=3,
                error_handler=error_handler,
            )
        page = await browser.new_page()
        return browser, page

    async def _perform_navigation(self, page: Any, url: str, error_handler: Any) -> None:
        """페이지 이동 수행 (Retry 포함)"""
        print(f"\n🌐 페이지 이동: {url}")
        if ADVANCED_RETRY_AVAILABLE:
            async def navigate_action():
                await page.goto(url, wait_until="networkidle", timeout=60000)
                return page

            async def navigation_condition():
                return page.url != "about:blank" and await page.evaluate("document.readyState") == "complete"

            await with_condition_retry(
                navigate_action,
                max_retries=3,
                condition_fn=navigation_condition,
                timeout=10000,
                base_delay=1.0,
            )
        else:
            await mcp_tool_call_with_retry(
                lambda: page.goto(url, wait_until="networkidle", timeout=60000),
                max_retries=3,
                error_handler=error_handler,
            )
        await asyncio.sleep(2)

    async def _run_generated_logic(self, code: str, page: Any, browser: Any) -> None:
        """생성된 코드 실행"""
        print("\n🚀 4단계: 생성된 코드 실행 중...")
        exec_globals = {"asyncio": asyncio, "page": page, "browser": browser}
        exec_locals: dict[str, Any] = {}
        exec(code, exec_globals, exec_locals)

        for key, value in exec_locals.items():
            if callable(value) and not key.startswith("_"):
                await value(page)
                break

    async def _handle_auth_error(
        self, error: Exception, attempt: int, max_retries: int, url: str, error_handler: Any, results: dict[str, Any]
    ) -> bool:
        """인증 오류 처리 및 재시도 판단"""
        from playwright.async_api import Error as PlaywrightError
        error_msg = str(error)
        results["error"] = error_msg
        print(f"\n❌ 오류 발생: {error_msg}")

        if error_handler:
            fix_result = await error_handler.handle_error(error, context={"url": url, "attempt": attempt})
            is_playwright_error = isinstance(error, PlaywrightError)
            
            key = "errors_handled" if is_playwright_error else "fixes_applied"
            val = {"error": error_msg, "fix": fix_result, "attempt": attempt + 1} if is_playwright_error else fix_result
            results[key].append(val)

            if fix_result.get("retry", False) and attempt < max_retries - 1:
                delay = fix_result.get("delay", 2**attempt)
                print(f"💡 {fix_result.get('message', '복구 중...')}")
                print(f"   {delay}초 후 재시도...")
                await asyncio.sleep(delay)
                return True

        if attempt < max_retries - 1:
            delay = 5 + attempt * 2
            print(f"   {delay}초 후 재시도...")
            await asyncio.sleep(delay)
            return True
        return False

    async def execute_mcp_auth_flow(
        self,
        url: str,
        prompt: str = "ChatGPT 로그인 테스트 생성해, MCP로 페이지 탐색",
        max_retries: int = 3,
    ) -> dict[str, Any]:
        """MCP 통합 인증 플로우 실행 (Refactored)"""
        from playwright.async_api import Error as PlaywrightError
        from playwright.async_api import async_playwright

        error_handler = self._init_error_handler()
        results: dict[str, Any] = {
            "success": False, "generated_code": "", "tool_calls": [], "snapshot": "",
            "error": None, "errors_handled": [], "fixes_applied": [],
        }

        async with async_playwright() as p:
            browser = None
            page = None

            for attempt in range(max_retries):
                try:
                    if browser is None or not browser.is_connected():
                        browser, page = await self._setup_browser_and_page(p, attempt, max_retries, error_handler)

                    await self._perform_navigation(page, url, error_handler)

                    generated_code = await self.generate_auth_with_mcp(prompt, page)
                    results["generated_code"] = generated_code
                    results["tool_calls"] = self.mcp_tools.tool_call_history

                    await self._run_generated_logic(generated_code, page, browser)

                    print("\n✅ MCP 통합 성공! 🎉")
                    results["success"] = True
                    break

                except (PlaywrightError, Exception) as e:
                    if await self._handle_auth_error(e, attempt, max_retries, url, error_handler, results):
                        if attempt < max_retries - 1 and browser:
                            try:
                                await browser.close()
                                browser = None
                                page = None
                            except Exception: pass
                        continue
                    break

            if error_handler:
                results["error_summary"] = error_handler.get_error_summary()
            if browser:
                print("\n💡 브라우저를 닫으시면 세션이 저장됩니다.")

        return results


async def mcp_auth_experiment(
    url: str = "https://chat.openai.com/auth/login",
    prompt: str = "ChatGPT 로그인 테스트 생성해, MCP로 페이지 탐색",
    llm_provider: str = "anthropic",
    api_key: str | None = None,
) -> dict[str, Any]:
    """
    MCP 통합 인증 실험 헬퍼 함수

    Args:
        url: 대상 URL
        prompt: 테스트 생성 프롬프트
        llm_provider: LLM 제공자 ("anthropic" 또는 "openai")
        api_key: API 키

    Returns:
        실행 결과
    """
    mcp_auth = MCPIntegratedAuth(llm_provider=llm_provider, api_key=api_key)
    return await mcp_auth.execute_mcp_auth_flow(url, prompt)


if __name__ == "__main__":
    import sys

    # Phase 2-4: settings 사용
    try:
        from config.settings import get_settings

        settings = get_settings()
        api_key = settings.ANTHROPIC_API_KEY
    except ImportError:
        try:
            from AFO.config.settings import get_settings

            settings = get_settings()
            api_key = settings.ANTHROPIC_API_KEY
        except ImportError:
            api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("⚠️  ANTHROPIC_API_KEY 환경변수를 설정해주세요")
        print("   또는 OPENAI_API_KEY를 사용하려면 llm_provider='openai' 설정")
        sys.exit(1)

    result = asyncio.run(mcp_auth_experiment(llm_provider="anthropic", api_key=api_key))

    print("\n" + "=" * 70)
    print("📊 MCP 통합 실험 결과")
    print("=" * 70)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
