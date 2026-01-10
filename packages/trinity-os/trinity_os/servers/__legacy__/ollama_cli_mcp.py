#!/usr/bin/env python3
"""Ollama CLI MCP Server Wrapper
AFO 왕국 - 자룡, 영덕 통합 (4단계 트리아지 2단계)

이 스크립트는 Ollama CLI를 MCP 프로토콜로 래핑합니다.
"""

import json
import os
import sys

import requests


def invoke_ollama(prompt: str, model: str | None = None) -> str:
    """Ollama CLI를 통한 LLM 호출 (4단계 트리아지 2단계: 로컬 정예병)

    Args:
        prompt: 사용자 프롬프트
        model: 사용할 모델 (기본: 환경 변수 또는 llama3.2:1b)

    Returns:
        Ollama의 응답

    """
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = model or os.getenv("OLLAMA_MODEL", "llama3.2:1b")

    try:
        response = requests.post(
            f"{base_url}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=300,
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
    except requests.exceptions.ConnectionError:
        return json.dumps(
            {
                "error": f"Ollama 서버에 연결할 수 없습니다. '{base_url}'에서 서버가 실행 중인지 확인하세요."
            }
        )
    except requests.exceptions.Timeout:
        return json.dumps({"error": "Ollama API 호출 시간 초과"})
    except Exception as e:
        return json.dumps({"error": f"Ollama API 오류: {e!s}"})


def main():
    """MCP 서버 메인 함수"""
    if len(sys.argv) > 1 and sys.argv[1] == "mcp":
        # MCP 모드: stdio를 통한 JSON-RPC 통신
        try:
            for line in sys.stdin:
                if not line.strip():
                    continue

                try:
                    request = json.loads(line)
                    method = request.get("method", "")
                    params = request.get("params", {})

                    if method == "tools/call":
                        tool_name = params.get("name", "")
                        arguments = params.get("arguments", {})

                        if tool_name == "ollama_chat":
                            prompt = arguments.get("prompt", "")
                            model = arguments.get("model", None)
                            response = invoke_ollama(prompt, model)

                            result = {
                                "jsonrpc": "2.0",
                                "id": request.get("id"),
                                "result": {
                                    "content": [{"type": "text", "text": response}]
                                },
                            }
                            print(json.dumps(result))
                            sys.stdout.flush()
                    elif method == "initialize":
                        result = {
                            "jsonrpc": "2.0",
                            "id": request.get("id"),
                            "result": {
                                "protocolVersion": "2024-11-05",
                                "capabilities": {"tools": {}},
                                "serverInfo": {
                                    "name": "ollama-cli-mcp",
                                    "version": "1.0.0",
                                    "description": "4단계 트리아지 2단계: 로컬 정예병",
                                },
                            },
                        }
                        print(json.dumps(result))
                        sys.stdout.flush()
                except json.JSONDecodeError:
                    continue
        except KeyboardInterrupt:
            pass
    else:
        # 일반 모드: 직접 프롬프트 실행
        if len(sys.argv) < 2:
            print("Usage: ollama_cli_mcp.py <prompt> [model]")
            print("   or: ollama_cli_mcp.py mcp  # MCP 서버 모드")
            sys.exit(1)

        prompt = " ".join(
            sys.argv[1:-1]
            if len(sys.argv) > 2 and sys.argv[-1].startswith("llama")
            else sys.argv[1:]
        )
        model = (
            sys.argv[-1]
            if len(sys.argv) > 2 and sys.argv[-1].startswith("llama")
            else None
        )
        response = invoke_ollama(prompt, model)
        print(response)


if __name__ == "__main__":
    main()
