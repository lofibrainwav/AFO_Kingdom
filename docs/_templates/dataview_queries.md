---
created: {{date:YYYY-MM-DD}}
tags: [dataview, queries, templates]
---

# Dataview 쿼리 템플릿 모음

> [!abstract] Dataview 개요
> 이 문서는 옵시디언 Dataview 플러그인을 활용한 다양한 쿼리 패턴을 제공합니다.
> 프로젝트 상태 추적, 태스크 관리, 메트릭 계산 등에 활용할 수 있습니다.

---

## 📊 프로젝트 상태 대시보드

### 진행 중인 프로젝트 목록

```dataview
TABLE
	file.mtime as "수정일",
	priority as "우선순위",
	status as "상태",
	tags as "태그"
FROM "docs"
WHERE type = "project" AND status != "completed"
SORT priority DESC, file.mtime DESC
```

### 프로젝트별 태스크 수량 통계

```dataview
TABLE
	length(rows.file.link) as "총 태스크",
	length(rows.file.link.where(meta(status) = "completed")) as "완료",
	length(rows.file.link.where(meta(status) = "in-progress")) as "진행중",
	length(rows.file.link.where(meta(status) = "pending")) as "대기중"
FROM "docs"
WHERE type = "project"
FLATTEN file.tasks as tasks
GROUP BY file.link as project
```

### 우선순위별 프로젝트 분포

```dataview
TABLE rows.file.link as "프로젝트"
FROM "docs"
WHERE type = "project"
FLATTEN priority as priority
GROUP BY priority
SORT length(rows) DESC
```

---

## 🎯 태스크 관리 대시보드

### 오늘 마감 태스크

```dataview
TASK
FROM "docs"
WHERE due = date(today)
SORT priority DESC
```

### 진행 중인 고우선순위 태스크

```dataview
TASK
FROM "docs"
WHERE status = "in-progress" AND priority = "high"
SORT file.mtime DESC
```

### 담당자별 태스크 분배

```dataview
TABLE
	length(rows.file.link) as "태스크 수",
	rows.priority as "우선순위 분포"
FROM "docs"
WHERE type = "task"
FLATTEN assignee as assignee
GROUP BY assignee
SORT length(rows) DESC
```

### 태스크 상태별 통계

```dataview
TABLE WITHOUT ID
	choice(meta(status) = "pending", 1, 0) as "대기",
	choice(meta(status) = "in-progress", 1, 0) as "진행중",
	choice(meta(status) = "completed", 1, 0) as "완료",
	choice(meta(status) = "cancelled", 1, 0) as "취소"
FROM "docs"
WHERE type = "task"
GROUP BY true
```

---

## 🔧 시스템 컴포넌트 모니터링

### 컴포넌트 상태 개요

```dataview
TABLE
	status as "상태",
	version as "버전",
	file.mtime as "최종 수정"
FROM "docs"
WHERE type = "component"
SORT status DESC, file.mtime DESC
```

### API 엔드포인트 상태

```dataview
TABLE
	method as "메서드",
	endpoint_path as "경로",
	status as "상태"
FROM "docs"
WHERE type = "api-endpoint"
SORT method ASC, endpoint_path ASC
```

### 에러 발생 컴포넌트

```dataview
LIST
FROM "docs"
WHERE type = "component" AND status = "error"
SORT file.mtime DESC
```

---

## 📈 메트릭 및 통계

### Trinity Score 평균 계산

```dataview
TABLE WITHOUT ID
	sum(rows.trinity_score) / length(rows) as "평균 Trinity Score",
	max(rows.trinity_score) as "최고 점수",
	min(rows.trinity_score) as "최저 점수"
FROM "docs"
WHERE trinity_score
GROUP BY true
```

### 문서 생성 통계

```dataview
TABLE WITHOUT ID
	count(rows) as "총 문서 수",
	sum(rows.file.size) as "총 파일 크기",
	avg(rows.file.mtime) as "평균 수정일"
FROM "docs"
WHERE file
GROUP BY true
```

### 태그 사용 빈도 분석

```dataview
TABLE length(rows) as "사용 빈도"
FROM "docs"
FLATTEN tags as tag
GROUP BY tag
SORT length(rows) DESC
LIMIT 20
```

---

## 🔍 검색 및 필터링

### 최근 수정된 중요 문서

```dataview
LIST
FROM "docs"
WHERE file.mtime >= date(today) - dur(7 days) AND priority = "high"
SORT file.mtime DESC
```

### 특정 태그가 있는 문서

```dataview
LIST
FROM "docs"
WHERE contains(tags, "#urgent") OR contains(tags, "#critical")
SORT priority DESC
```

### 담당자가 할당되지 않은 태스크

```dataview
TASK
FROM "docs"
WHERE !assignee AND type = "task"
SORT priority DESC
```

---

## 📋 검증 보고서 자동화

### 검증 상태 개요

```dataview
TABLE
	status as "상태",
	count as "문서 수"
FROM "docs"
WHERE contains(file.name, "verification") OR contains(file.name, "report")
FLATTEN status as status
GROUP BY status
```

### 실패한 검증 항목

```dataview
LIST
FROM "docs"
WHERE status = "failed" AND (type = "verification" OR type = "test")
SORT file.mtime DESC
```

### 성공률 계산

```dataview
TABLE WITHOUT ID
	round((length(rows.where(meta(status) = "passed")) / length(rows)) * 100, 2) + "%" as "검증 성공률",
	length(rows.where(meta(status) = "failed")) as "실패 항목 수",
	length(rows.where(meta(status) = "pending")) as "대기 항목 수"
FROM "docs"
WHERE type = "verification"
GROUP BY true
```

---

## 🔄 자동화된 워크플로우

### 매일 점검 항목

```dataview
TASK
FROM "docs"
WHERE contains(tags, "#daily-check") AND status != "completed"
SORT priority DESC
```

### 주간 리뷰 대상

```dataview
LIST
FROM "docs"
WHERE file.mtime <= date(today) - dur(7 days) AND status = "needs-review"
SORT file.mtime DESC
```

### 만료 예정 항목

```dataview
LIST
FROM "docs"
WHERE expiry_date AND expiry_date <= date(today) + dur(30 days)
SORT expiry_date ASC
```

---

## 🎨 시각화 템플릿

### 상태별 분포 차트 (Mermaid)

```dataviewjs
const pages = dv.pages('"docs"').where(p => p.status);
const statusCounts = {};

pages.forEach(page => {
    const status = page.status;
    statusCounts[status] = (statusCounts[status] || 0) + 1;
});

const chartData = Object.entries(statusCounts)
    .map(([status, count]) => `    ${status}: ${count}`)
    .join('\n');

dv.paragraph(`
\`\`\`mermaid
pie title 문서 상태 분포
${chartData}
\`\`\`
`);
```

### 우선순위 트렌드 (Chart.js)

```dataviewjs
const tasks = dv.pages('"docs"').where(p => p.type === "task" && p.priority);
const priorityData = {};

tasks.forEach(task => {
    const priority = task.priority;
    priorityData[priority] = (priorityData[priority] || 0) + 1;
});

const labels = Object.keys(priorityData);
const data = Object.values(priorityData);

dv.paragraph(`
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<canvas id="priorityChart" width="400" height="200"></canvas>
<script>
const ctx = document.getElementById('priorityChart');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ${JSON.stringify(labels)},
        datasets: [{
            label: '태스크 수',
            data: ${JSON.stringify(data)},
            backgroundColor: ['#ff6b6b', '#ffd93d', '#6bcf7f']
        }]
    }
});
</script>
`);
```

---

## ⚙️ 고급 Dataview 패턴

### 관련 문서 네트워크

```dataview
LIST
FROM "docs"
WHERE file.name = "AFO_KINGDOM_MAIN"
FLATTEN file.outlinks as outlink
WHERE contains(outlink.path, "docs/")
SORT outlink ASC
```

### 파일 크기 분석

```dataview
TABLE
	file.size as "크기",
	round(file.size / 1024, 2) + " KB" as "크기(KB)",
	file.mtime as "수정일"
FROM "docs"
SORT file.size DESC
LIMIT 10
```

### 템플릿 사용 통계

```dataview
TABLE length(rows) as "사용 수"
FROM "docs/_templates"
FLATTEN file.inlinks as inlink
GROUP BY file.name
SORT length(rows) DESC
```

---

## 🔧 유지보수 쿼리

### 오래된 문서 식별

```dataview
LIST
FROM "docs"
WHERE file.mtime <= date(today) - dur(90 days)
SORT file.mtime ASC
```

### 링크 깨짐 검사

```dataview
LIST
FROM "docs"
WHERE file.outlinks.length > 0
FLATTEN file.outlinks as outlink
WHERE !outlink.exists
SORT file.name ASC
```

### 중복 태그 정리

```dataview
LIST
FROM "docs"
FLATTEN tags as tag
GROUP BY tag
WHERE length(rows) > 1
SORT length(rows) DESC
LIMIT 10
```

---

> [!tip] Dataview 활용 팁
>
> 1. **정기적 실행**: Dataview 쿼리는 파일이 변경될 때마다 자동으로 업데이트됩니다
> 2. **성능 최적화**: WHERE 절을 사용하여 검색 범위를 제한하세요
> 3. **데이터 타입**: `meta(field)`를 사용하여 YAML frontmatter 데이터를 참조하세요
> 4. **JavaScript 통합**: DataviewJS를 사용하여 복잡한 계산과 시각화를 구현하세요
> 5. **템플릿화**: 자주 사용하는 쿼리를 템플릿으로 만들어 재사용하세요

---

> [!info] Dataview 설정
> **옵시디언 설정 → 커뮤니티 플러그인 → Dataview 설치**
>
> 주요 설정:
> - **Enable JavaScript Queries**: DataviewJS 활성화
> - **Enable Inline Queries**: 인라인 쿼리 활성화
> - **Refresh Interval**: 자동 새로고침 간격 설정

---

**생성일**: {{date:YYYY-MM-DD}}
**버전**: 1.0.0
**카테고리**: Dataview 템플릿
