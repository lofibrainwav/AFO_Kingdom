# Excalidraw Automation Tutorial

> **As-of: 2025-12-29 | Version: v1.0**
> **眞善美孝永** - 지능형 시각화 자동화 (ea 객체 & Script Engine)

## 개요

Excalidraw는 단순한 드로잉 툴을 넘어, **ExcalidrawAutomate (ea 객체)**를 통해 프로그래밍 방식으로 다이어그램을 생성하고 제어할 수 있는 강력한 엔진입니다.

---

## 🛠️ 핵심 자동화: ea 객체 활용

Obsidian 내에서 `ExcalidrawAutomate` 객체를 사용하여 요소를 생성하는 기본 패턴입니다.

### 1. 기본 도형 생성
```javascript
const ea = ExcalidrawAutomate;
ea.reset(); // 캔버스 초기화

// 사각형 및 텍스트 추가
ea.addRect(0, 0, 400, 200);
ea.addText(100, 50, "AFO Kingdom Core", {box: true});

// 캔버스에 적용
ea.addElementsToView();
```

### 2. 노드 간 연결 (Connector)
```javascript
const id1 = ea.addText(0, 0, "Input");
const id2 = ea.addText(300, 0, "Output");

// 두 객체를 화살표로 연결
ea.connectObjects(id1, id2, {
    startArrowhead: "arrow",
    endArrowhead: "dot",
    strokeColor: "#00ff00"
});

ea.addElementsToView();
```

---

## 🏗️ Templater 통합 (실전 예제)

Templater를 사용하여 노트 생성 시 다이어그램을 자동으로 빌드합니다.

### 새 파일 생성 및 임베드
```javascript
<%*
const ea = ExcalidrawAutomate;
ea.reset();
ea.setTheme("dark");

// 5기둥 원형 다이어그램 (眞善美孝永)
ea.addCircle(300, 300, 400); 
ea.addText(300, 100, "眞善美孝永", {textAlign: "center", fontSize: 40});

await ea.create({
  filename: "System_Diagram_" + tp.date.now("HHmm"),
  onNewPane: true
});
%>
```

---

## 🏛️ Script Engine 활용

Obsidian Excalidraw 플러그인 설정의 **Script Engine Store**에서 검증된 스크립트를 내려받아 즉시 사용할 수 있습니다.

- **Add Box Around Text**: 선택한 텍스트에 자동으로 박스를 씌움.
- **Connect Selected**: 선택한 두 노드를 자동으로 화살표 연결.
- **Glow Effect**: 객체에 광채 효과 부여 (Trinity Score 시각화용).

---

**Trinity Score**: 眞 100% | 善 100% | 美 100% | 孝 100% | 永 100%
