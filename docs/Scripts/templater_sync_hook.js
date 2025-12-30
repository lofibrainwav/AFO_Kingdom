/**
 * Scripts/templater_sync_hook.js
 * 템플릿 실행 후 Dataview 및 메타데이터 동기화를 위한 Hook 스크립트
 */
module.exports = async function templater_sync_hook(tp) {
    tp.hooks.on_all_templates_executed(async () => {
        try {
            // 1. 메타데이터 캐시 강제 갱신 시도
            const file = tp.file.find_tfile(tp.file.path(true));
            if (file) {
                // 인덱싱 대기를 위해 약간의 지연 추가 (Obsidian Forum 권고)
                await new Promise(r => setTimeout(r, 500));
                await app.metadataCache.resolve(file);
            }
            
            // 2. Dataview API 리프레시 (사용자 가이드 반영)
            const dvPlugin = app.plugins.plugins.dataview;
            if (dvPlugin && dvPlugin.api) {
                await dvPlugin.api.refresh();
                new Notice("Kingdom Sync: Dataview & Metadata Refreshed! 🚀");
            } else {
                // Dataview가 없거나 API 접근 불가 시 조용히 넘어가되 Notice는 표시
                console.log("Dataview API not available for instant refresh.");
            }
        } catch (error) {
            console.error("Templater Hook Error:", error);
            // 孝(Serenity)를 위해 과한 에러 팝업 대신 로그 기록
        }
    });
}
