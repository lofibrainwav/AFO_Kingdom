# Advanced Orchestration Template

<%*
// 1. 동적 프롬프트 실행 (Scripts/advanced_prompt.js)
const frontmatter = await tp.user.advanced_prompt(tp);
tR += frontmatter;

// 2. 동기화 Hook 등록 (Scripts/templater_sync_hook.js)
await tp.user.templater_sync_hook(tp);
%>

## 🏛️ System Context
- **Generated-at**: <% tp.date.now("YYYY-MM-DD HH:mm") %>
- **Orchestrator**: Antigravity (Chancellor V2)

## 📊 Operational Metrics (Live)
<%*
// Dataview 리프레시 후 데이터가 여기에 나타나게 됨
%>
```dataview
TABLE status, trinity-score
FROM "Metrics"
SORT file.mtime DESC
LIMIT 5
```

## 🎨 Visual SSOT (Generated)
<%*
// 3. 동적 다이어그램 생성 (Scripts/excalidraw_dynamic_gen.js)
const diagramLink = await tp.user.excalidraw_dynamic_gen(tp);
if (diagramLink) {
    tR += diagramLink;
}
%>

---
**Trinity Score**: 眞 100% | 善 100% | 美 100% | 孝 100% | 永 100%
