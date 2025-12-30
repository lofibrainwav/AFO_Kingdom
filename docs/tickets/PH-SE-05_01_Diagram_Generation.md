# [TICKET] PH-SE-05.01: AI-Driven Diagram Generation

> **Status: OPEN | Priority: HIGH**
> **Owner: Chancellor (Chancellor V2)**

## 🎯 Goal
사령관님의 텍스트 명령을 Excalidraw JSON 포맷으로 직접 변환하는 AI 파이프라인(GenUI for Diagrams)을 구축한다.

---

## 📋 핵심 과업 (Tasks)
- **Prompt Engineering**: 텍스트 설명을 Excalidraw 요소(elements) 배열로 변환하는 정교한 프롬프트 설계.
- **Node Injection**: `GraphState`에서 추출된 데이터를 다이어그램 내 특정 노드에 동적으로 삽입하는 로직 개발.
- **Style Unification**: 제국의 네오 브루탈리즘 스타일(굵은 선, 특정 색상 코드)을 기본 스타일로 고정.

---

## ⚖️ CI Gate Condition
- `verify_visual_sync.py` PASS 필수.
- 생성된 `.excalidraw` 파일이 유효한 JSON 스키마를 준수해야 함.
