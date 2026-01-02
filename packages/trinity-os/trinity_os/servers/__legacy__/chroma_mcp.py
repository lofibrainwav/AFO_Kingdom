#!/usr/bin/env python3
"""
Chroma Vector Database MCP Server
AFO 왕국 - Chroma 벡터 데이터베이스 통합

이 스크립트는 Chroma 벡터 데이터베이스를 MCP 프로토콜로 래핑합니다.
임베딩 생성, 벡터 검색, 컬렉션 관리를 제공합니다.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any

import chromadb

# 프로젝트 경로 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "afo_soul_engine"))


class ChromaMCP:
    """Chroma MCP 서버 클래스"""

    def __init__(self):
        self.client = chromadb.EphemeralClient()
        self._initialize_client()

    def _initialize_client(self):
        """Chroma 클라이언트 초기화"""
        try:
            # 환경 변수에서 패스 가져오거나 기본 PersistentClient 사용
            persist_directory = os.getenv("CHROMA_DB_PATH", None)

            if persist_directory:
                self.client = chromadb.PersistentClient(path=persist_directory)
            else:
                # 기본적으로 EphemeralClient 사용 (인메모리, 세션 내에서만 유지)
                pass
        except Exception:
            # 이미 EphemeralClient가 설정되어 있음
            pass

    def create_collection(self, name: str) -> str:
        """새 컬렉션 생성"""
        try:
            self.client.create_collection(name=name)
            return json.dumps(
                {
                    "success": True,
                    "collection_name": name,
                    "message": f"컬렉션 '{name}'이(가) 성공적으로 생성되었습니다.",
                }
            )
        except Exception as e:
            return json.dumps({"success": False, "error": f"컬렉션 생성 실패: {e!s}"})

    def get_or_create_collection(self, name: str) -> str:
        """컬렉션 가져오기 또는 생성"""
        try:
            self.client.get_or_create_collection(name=name)
            return json.dumps(
                {
                    "success": True,
                    "collection_name": name,
                    "message": f"컬렉션 '{name}'이(가) 준비되었습니다.",
                }
            )
        except Exception as e:
            return json.dumps(
                {"success": False, "error": f"컬렉션 가져오기 실패: {e!s}"}
            )

    def add_documents(
        self,
        collection_name: str,
        documents: list[str],
        metadatas: list[dict[str, Any]] | None = None,
        ids: list[str] | None = None,
    ) -> str:
        """문서 추가"""
        try:
            collection = self.client.get_collection(name=collection_name)

            # 자동 ID 생성
            if ids is None:
                import uuid

                ids = [str(uuid.uuid4()) for _ in documents]

            # 메타데이터 타입 처리
            if metadatas is not None:
                # Chroma expects List[Dict[str, Union[str, int, float, bool, None]]]
                processed_metadatas = []
                for meta in metadatas:
                    processed_meta = {}
                    for k, v in meta.items():
                        if isinstance(v, (str, int, float, bool)) or v is None:
                            processed_meta[k] = v
                        else:
                            processed_meta[k] = str(v)  # Convert other types to string
                    processed_metadatas.append(processed_meta)
            else:
                processed_metadatas = None

            collection.add(documents=documents, metadatas=processed_metadatas, ids=ids)

            return json.dumps(
                {
                    "success": True,
                    "collection_name": collection_name,
                    "added_count": len(documents),
                    "ids": ids,
                    "message": f"{len(documents)}개 문서가 컬렉션 '{collection_name}'에 추가되었습니다.",
                }
            )
        except Exception as e:
            return json.dumps({"success": False, "error": f"문서 추가 실패: {e!s}"})

    def query_collection(
        self,
        collection_name: str,
        query_texts: list[str],
        n_results: int = 5,
        where: dict | None = None,
        where_document: dict | None = None,
    ) -> str:
        """컬렉션 쿼리"""
        try:
            collection = self.client.get_collection(name=collection_name)

            results = collection.query(
                query_texts=query_texts,
                n_results=n_results,
                where=where,
                where_document=where_document,
            )

            # 안전하게 결과 길이 계산
            documents = results.get("documents", [])
            if isinstance(documents, list) and documents:
                result_count = (
                    len(documents)
                    if isinstance(documents[0], list)
                    else len([d for d in documents if d])
                )
            else:
                result_count = 0

            return json.dumps(
                {
                    "success": True,
                    "collection_name": collection_name,
                    "query_texts": query_texts,
                    "results": results,
                    "message": f"컬렉션 '{collection_name}'에서 {result_count}개 결과 발견",
                }
            )
        except Exception as e:
            return json.dumps({"success": False, "error": f"쿼리 실패: {e!s}"})

    def get_document(self, collection_name: str, doc_id: str) -> str:
        """특정 문서 가져오기"""
        try:
            collection = self.client.get_collection(name=collection_name)
            result = collection.get(ids=[doc_id])

            if result["documents"]:
                return json.dumps(
                    {
                        "success": True,
                        "collection_name": collection_name,
                        "document": result["documents"][0],
                        "metadata": (
                            result["metadatas"][0] if result["metadatas"] else {}
                        ),
                        "id": doc_id,
                    }
                )
            return json.dumps(
                {
                    "success": False,
                    "error": f"문서 ID '{doc_id}'를 찾을 수 없습니다.",
                }
            )
        except Exception as e:
            return json.dumps({"success": False, "error": f"문서 조회 실패: {e!s}"})

    def delete_collection(self, name: str) -> str:
        """컬렉션 삭제"""
        try:
            self.client.delete_collection(name=name)
            return json.dumps(
                {
                    "success": True,
                    "collection_name": name,
                    "message": f"컬렉션 '{name}'이(가) 삭제되었습니다.",
                }
            )
        except Exception as e:
            return json.dumps({"success": False, "error": f"컬렉션 삭제 실패: {e!s}"})

    def list_collections(self) -> str:
        """모든 컬렉션 목록"""
        try:
            collections = self.client.list_collections()
            collection_names = [col.name for col in collections]

            return json.dumps(
                {
                    "success": True,
                    "collections": collection_names,
                    "count": len(collection_names),
                    "message": f"{len(collection_names)}개 컬렉션을 발견했습니다.",
                }
            )
        except Exception as e:
            return json.dumps(
                {"success": False, "error": f"컬렉션 목록 조회 실패: {e!s}"}
            )


def main():
    """MCP 서버 메인 함수"""
    chroma_mcp = ChromaMCP()

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

                        response_text = ""
                        if tool_name == "create_collection":
                            name = arguments.get("name", "")
                            response_text = chroma_mcp.create_collection(name)

                        elif tool_name == "get_or_create_collection":
                            name = arguments.get("name", "")
                            response_text = chroma_mcp.get_or_create_collection(name)

                        elif tool_name == "add_documents":
                            collection_name = arguments.get("collection_name", "")
                            documents = arguments.get("documents", [])
                            metadatas = arguments.get("metadatas")
                            ids = arguments.get("ids")
                            response_text = chroma_mcp.add_documents(
                                collection_name, documents, metadatas, ids
                            )

                        elif tool_name == "query_collection":
                            collection_name = arguments.get("collection_name", "")
                            query_texts = arguments.get("query_texts", [])
                            n_results = arguments.get("n_results", 5)
                            where = arguments.get("where")
                            where_document = arguments.get("where_document")
                            response_text = chroma_mcp.query_collection(
                                collection_name,
                                query_texts,
                                n_results,
                                where,
                                where_document,
                            )

                        elif tool_name == "get_document":
                            collection_name = arguments.get("collection_name", "")
                            doc_id = arguments.get("id", "")
                            response_text = chroma_mcp.get_document(
                                collection_name, doc_id
                            )

                        elif tool_name == "delete_collection":
                            name = arguments.get("name", "")
                            response_text = chroma_mcp.delete_collection(name)

                        elif tool_name == "list_collections":
                            response_text = chroma_mcp.list_collections()

                        result = {
                            "jsonrpc": "2.0",
                            "id": request.get("id"),
                            "result": {
                                "content": [{"type": "text", "text": response_text}]
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
                                    "name": "chroma-mcp",
                                    "version": "1.0.0",
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
        # 일반 모드
        print("Chroma MCP Server")
        print("Usage:")
        print("  python chroma_mcp.py mcp  # MCP 서버 모드")
        print()
        print("Available tools:")
        print("  - create_collection")
        print("  - get_or_create_collection")
        print("  - add_documents")
        print("  - query_collection")
        print("  - get_document")
        print("  - delete_collection")
        print("  - list_collections")


if __name__ == "__main__":
    main()
