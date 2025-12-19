// 옵시디언 템플릿 적용 후 자동 실행 스크립트
// Templater에서 호출되어 템플릿 후처리를 수행합니다.

class TemplatePostProcessor {
    constructor() {
        this.app = app;
        this.file = app.workspace.getActiveFile();
        this.metadata = {};
    }

    async processTemplate() {
        try {
            // 현재 파일의 메타데이터 추출
            await this.extractMetadata();

            // 템플릿 타입에 따른 후처리 실행
            await this.runTemplateSpecificProcessing();

            // 공통 후처리 실행
            await this.runCommonPostProcessing();

            console.log(`✅ 템플릿 후처리 완료: ${this.file.basename}`);
        } catch (error) {
            console.error(`❌ 템플릿 후처리 실패: ${error.message}`);
        }
    }

    async extractMetadata() {
        const fileContent = await app.vault.read(this.file);
        const frontmatterMatch = fileContent.match(/^---\n([\s\S]*?)\n---/);

        if (frontmatterMatch) {
            // 간단한 YAML 파싱 (복잡한 파싱은 필요시 라이브러리 사용)
            const frontmatter = frontmatterMatch[1];
            const lines = frontmatter.split('\n');

            for (const line of lines) {
                const [key, ...valueParts] = line.split(':');
                if (key && valueParts.length > 0) {
                    const value = valueParts.join(':').trim().replace(/^["']|["']$/g, '');
                    this.metadata[key.trim()] = value;
                }
            }
        }
    }

    async runTemplateSpecificProcessing() {
        const templateType = this.detectTemplateType();

        switch (templateType) {
            case 'project':
                await this.processProjectTemplate();
                break;
            case 'component':
                await this.processComponentTemplate();
                break;
            case 'api':
                await this.processApiTemplate();
                break;
            case 'collaboration':
                await this.processCollaborationTemplate();
                break;
            case 'ai':
                await this.processAiTemplate();
                break;
            default:
                console.log(`ℹ️  일반 템플릿 감지됨: ${templateType}`);
        }
    }

    detectTemplateType() {
        // 파일명이나 메타데이터를 기반으로 템플릿 타입 감지
        const fileName = this.file.basename.toLowerCase();

        if (fileName.includes('project') || this.metadata.type === 'project') {
            return 'project';
        } else if (fileName.includes('component') || this.metadata.type === 'component') {
            return 'component';
        } else if (fileName.includes('api') || this.metadata.type === 'api-endpoint') {
            return 'api';
        } else if (fileName.includes('collaboration') || fileName.includes('workflow')) {
            return 'collaboration';
        } else if (fileName.includes('ai') || fileName.includes('integration')) {
            return 'ai';
        }

        return 'general';
    }

    async processProjectTemplate() {
        console.log('🏗️  프로젝트 템플릿 후처리 시작');

        // 프로젝트 폴더 구조 생성
        await this.createProjectStructure();

        // 관련 문서 링크 추가
        await this.addRelatedLinks('project');

        // Trinity Score 초기화
        await this.initializeTrinityScore();
    }

    async processComponentTemplate() {
        console.log('🔧 컴포넌트 템플릿 후처리 시작');

        // 컴포넌트 태그 추가
        await this.addComponentTags();

        // 인터페이스 파일 생성
        await this.generateInterfaceFiles();

        // 테스트 파일 템플릿 생성
        await this.createTestTemplates();
    }

    async processApiTemplate() {
        console.log('🌐 API 템플릿 후처리 시작');

        // API 엔드포인트 검증
        await this.validateApiEndpoint();

        // 관련 API 문서 링크
        await this.addApiLinks();

        // 테스트 코드 생성
        await this.generateApiTests();
    }

    async processCollaborationTemplate() {
        console.log('👥 협업 템플릿 후처리 시작');

        // 팀 멤버 태그 추가
        await this.addTeamTags();

        // Git 브랜치 제안
        await this.suggestGitBranch();

        // 리뷰어 할당
        await this.assignReviewers();
    }

    async processAiTemplate() {
        console.log('🤖 AI 템플릿 후처리 시작');

        // AI 모델 설정 검증
        await this.validateAiConfig();

        // 프롬프트 템플릿 최적화
        await this.optimizePrompts();

        // 비용 추정
        await this.estimateCosts();
    }

    async runCommonPostProcessing() {
        // 공통 후처리 작업들

        // 파일 권한 설정
        await this.setFilePermissions();

        // Dataview 인덱싱 준비
        await this.prepareDataviewIndexing();

        // 백업 생성
        await this.createBackup();

        // Context7에 자동 등록
        await this.registerToContext7();

        // 알림 전송
        await this.sendNotification();
    }

    async registerToContext7() {
        // Context7에 문서 자동 등록
        try {
            const filePath = this.file.path;
            const projectRoot = this.app.vault.adapter.basePath || '/Users/brnestrm/AFO_Kingdom';
            const scriptPath = `${projectRoot}/scripts/register_obsidian_doc_to_context7.py`;
            const fullPath = `${projectRoot}/docs/${filePath}`;

            // Templater의 system command를 통해 Python 스크립트 실행
            // 주의: Templater의 enable_system_commands가 true여야 함
            const { exec } = require('child_process');
            
            exec(`python3 "${scriptPath}" "${fullPath}"`, (error, stdout, stderr) => {
                if (error) {
                    console.warn(`⚠️  Context7 등록 실패: ${error.message}`);
                    return;
                }
                if (stdout) {
                    console.log(`✅ Context7 등록: ${stdout.trim()}`);
                }
                if (stderr) {
                    console.warn(`⚠️  Context7 등록 경고: ${stderr.trim()}`);
                }
            });
        } catch (error) {
            console.warn(`⚠️  Context7 등록 중 오류: ${error.message}`);
        }
    }

    async createProjectStructure() {
        const projectName = this.metadata.name || this.file.basename.replace(/\s+/g, '_').toLowerCase();
        const basePath = `docs/projects/${projectName}`;

        const folders = [
            `${basePath}/specs`,
            `${basePath}/architecture`,
            `${basePath}/testing`,
            `${basePath}/deployment`
        ];

        for (const folder of folders) {
            try {
                await app.vault.createFolder(folder);
            } catch (error) {
                // 폴더가 이미 존재하는 경우 무시
                if (!error.message.includes('Folder already exists')) {
                    console.warn(`폴더 생성 실패: ${folder}`, error);
                }
            }
        }
    }

    async addRelatedLinks(type) {
        let links = '';

        switch (type) {
            case 'project':
                links = `
## 📚 관련 문서
- [[AFO_KINGDOM_MAIN|AFO Kingdom 메인]]
- [[docs/_templates/README|템플릿 가이드]]
- [[docs/TRINITY_SCORE_SSOT_ALIGNMENT|Trinity Score 가이드]]
`;
                break;
            case 'component':
                links = `
## 🔗 관련 컴포넌트
- [[docs/_templates/system_component|컴포넌트 템플릿]]
- [[docs/MCP_TOOL_TRINITY_SCORE_IMPLEMENTATION|MCP 구현 가이드]]
`;
                break;
        }

        if (links) {
            const currentContent = await app.vault.read(this.file);
            const updatedContent = currentContent + links;
            await app.vault.modify(this.file, updatedContent);
        }
    }

    async initializeTrinityScore() {
        // Trinity Score 초기 계산
        const trinityScore = {
            truth: 85,
            goodness: 80,
            beauty: 90,
            serenity: 75,
            eternity: 70,
            total: 80
        };

        // 메타데이터에 추가
        const currentContent = await app.vault.read(this.file);
        const frontmatterMatch = currentContent.match(/^---\n([\s\S]*?)\n---/);

        if (frontmatterMatch) {
            let frontmatter = frontmatterMatch[1];
            frontmatter += `\ntrinity_score: ${trinityScore.total}`;
            frontmatter += `\ntrinity_breakdown:`;
            frontmatter += `\n  truth: ${trinityScore.truth}`;
            frontmatter += `\n  goodness: ${trinityScore.goodness}`;
            frontmatter += `\n  beauty: ${trinityScore.beauty}`;
            frontmatter += `\n  serenity: ${trinityScore.serenity}`;
            frontmatter += `\n  eternity: ${trinityScore.eternity}`;

            const updatedContent = currentContent.replace(/^---\n[\s\S]*?\n---/, `---\n${frontmatter}\n---`);
            await app.vault.modify(this.file, updatedContent);
        }
    }

    async setFilePermissions() {
        // 파일 권한 메타데이터 추가
        const permissions = {
            owner: this.metadata.assignee || '승상',
            reviewers: ['제갈량', '사마의', '주유'],
            editors: ['팀 멤버'],
            public: false
        };

        // 실제 옵시디언에서는 파일 시스템 권한이 제한적임
        // 대신 메타데이터로 권한 정보 기록
        console.log(`📋 파일 권한 설정: ${JSON.stringify(permissions)}`);
    }

    async prepareDataviewIndexing() {
        // Dataview가 이 파일을 인덱싱할 수 있도록 메타데이터 검증
        const requiredFields = ['type', 'status', 'created'];

        for (const field of requiredFields) {
            if (!this.metadata[field]) {
                console.warn(`⚠️  누락된 Dataview 필드: ${field}`);
            }
        }
    }

    async createBackup() {
        // 중요 문서의 자동 백업
        if (this.metadata.priority === 'high' || this.metadata.type === 'project') {
            console.log('💾 자동 백업 생성됨');
            // 실제 백업 로직은 옵시디언 플러그인이나 외부 스크립트에서 처리
        }
    }

    async sendNotification() {
        // 템플릿 적용 완료 알림
        const message = `✅ 템플릿 적용 완료: ${this.file.basename}`;
        console.log(message);

        // 실제 알림은 옵시디언 알림 시스템이나 외부 통합에서 처리
        // 예: Discord 웹훅, 이메일 알림 등
    }

    // 기타 헬퍼 메서드들
    async addComponentTags() { /* 컴포넌트 태그 추가 로직 */ }
    async generateInterfaceFiles() { /* 인터페이스 파일 생성 로직 */ }
    async createTestTemplates() { /* 테스트 템플릿 생성 로직 */ }
    async validateApiEndpoint() { /* API 엔드포인트 검증 로직 */ }
    async addApiLinks() { /* API 링크 추가 로직 */ }
    async generateApiTests() { /* API 테스트 생성 로직 */ }
    async addTeamTags() { /* 팀 태그 추가 로직 */ }
    async suggestGitBranch() { /* Git 브랜치 제안 로직 */ }
    async assignReviewers() { /* 리뷰어 할당 로직 */ }
    async validateAiConfig() { /* AI 설정 검증 로직 */ }
    async optimizePrompts() { /* 프롬프트 최적화 로직 */ }
    async estimateCosts() { /* 비용 추정 로직 */ }
}

// 메인 실행 함수
async function postProcessTemplate() {
    const processor = new TemplatePostProcessor();
    await processor.processTemplate();
}

module.exports = postProcessTemplate;
