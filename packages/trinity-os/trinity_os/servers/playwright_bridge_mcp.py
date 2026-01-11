from typing import Any, Mapping, cast

# mypy: ignore-errors
from playwright.sync_api import \
    sync_playwright  # pyright: ignore[reportMissingImports]


def _as_mapping(x: object) -> Mapping[str, Any]:
    return cast(Mapping[str, Any], x)


def _as_list(x: object) -> list[Any]:
    return cast(list[Any], x)


def _as_any(x: object) -> Any:
    return cast(Any, x)


class PlaywrightBridgeMCP:
    """Frontend Bridge Node (Playwright MCP)
    Enables the AFO Kingdom to control web browsers, reducing manual friction (Serenity).
    """

    _playwright = None
    _browser = None
    _page = None

    @classmethod
    def _ensure_browser(cls):
        """Singleton browser initialization."""
        if cast(Any, cls)._page is None:
            cls._playwright = sync_playwright().start()
            # Launch headless by default, or headful if debugging (can be configured)
            # Using headless=True for MCP to avoid popping up windows on User's face unexpectedly
            # unless User explicitly requests it.
            # But "Bridge Node" implies we might want to attach to existing sessions.
            # For now, we launch a new context.
            cls._browser = cls._playwright.chromium.launch(headless=True)
            cls._page = cls._browser.new_page()

    @classmethod
    def navigate(cls, url: str) -> dict:
        """Navigate to a URL."""
        try:
            cls._ensure_browser()
            cast(Any, cls)._page.goto(url)
            title: Any = cast(Any, cls)._page.title()
            return {
                "success": True,
                "url": url,
                "title": title,
                "message": f"Navigated to {title}",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    def screenshot(cls, path: str = "screenshot.png") -> dict:
        """Capture the current view."""
        try:
            cls._ensure_browser()
            # Ensure path is just a filename in a temp dir or specific artifacts dir
            # For safety, we force writing to /tmp or current dir if safe
            # Here we just use the provided path but valid absolute path should be enforced by caller
            cast(Any, cls)._page.screenshot(path=path)
            return {
                "success": True,
                "path": path,
                "message": f"Screenshot saved to {path}",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    def click(cls, selector: str) -> dict:
        """Click an element."""
        try:
            cls._ensure_browser()
            cast(Any, cls)._page.click(selector)
            return {"success": True, "message": f"Clicked {selector}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    def type_text(cls, selector: str, text: str) -> dict:
        """Type text into an element."""
        try:
            cls._ensure_browser()
            _as_any(cls)._page.fill(selector, text)
            return {"success": True, "message": f"Typed text into {selector}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    def scrape(cls, selector: str) -> dict:
        """Scrape text content from a selector."""
        try:
            cls._ensure_browser()
            if selector == "body" or selector == "content":
                content = cast(Any, cls)._page.content()  # Full HTML
                text: Any = cast(Any, cls)._page.inner_text("body")
                return {
                    "success": True,
                    "text_length": len(text),
                    "preview": text[:500],
                    "message": "Scraped body content",
                }

            content: Any = cast(Any, cls)._page.inner_text(selector)
            return {
                "success": True,
                "content": content,
                "message": f"Scraped content from {selector}",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    def close(cls):
        """Close the browser resource."""
        if cast(Any, cls)._browser:
            cast(Any, cls)._browser.close()
        if cast(Any, cls)._playwright:
            cast(Any, cls)._playwright.stop()
        cls._page = None
        cls._browser = None
        cls._playwright = None
