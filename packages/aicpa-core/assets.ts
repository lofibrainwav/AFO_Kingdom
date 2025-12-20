import { Template } from './types';

export const ASSET_TEMPLATES: Template[] = [
    {
        id: 'big4-ma',
        category: 'Advisory',
        name: 'M&A Due Diligence (Big 4 Style)',
        badge: 'Big 4 Method',
        description: 'Tech Startup 인수합병 시 재무 실사 및 위험 평가.',
        variables: [
            { key: 'target_company', label: '대상 기업', value: 'Core AI Startup', type: 'text' },
            { key: 'deal_size', label: '인수 금액', value: '50,000,000', type: 'currency' },
            { key: 'risk_area', label: '중점 리스크', value: 'ASC 606 (Revenue)', type: 'text' }
        ],
        data: {
            role: 'Big 4 Deal Advisory Partner. M&A 전문가.',
            context: '우리는 {{target_company}} (Deal Size: ${{deal_size}})에 대한 인수 실사(Due Diligence)를 수행 중입니다. 주요 검토 사항은 {{risk_area}} 입니다. 현재 대상 회사는 초기 단계라 내부 통제가 미비합니다.',
            audience: 'PE(Private Equity) 투자 위원회 및 전략적 투자자(SI).',
            task: '재무 제표의 질적 분석(QofE)을 수행하고, Valuation에 영향을 미칠 수 있는 Deal Breaker 요인을 식별하십시오. 특히 EBITDA 조정 항목을 보수적으로 산출하십시오.',
            execution: 'Key Findings -> Financial Analysis -> Risk Assessment -> Recommendation 순으로 보고서를 구성하십시오.'
        }
    },
    {
        id: 'la-tax-realestate',
        category: 'Tax',
        name: 'LA Real Estate 1031 Exchange',
        badge: 'LA Specialist',
        description: 'LA 지역 상업용 부동산 매각 및 1031 교환 세무 자문.',
        variables: [
            { key: 'sale_price', label: '매각 금액', value: '2,500,000', type: 'currency' },
            { key: 'capital_gain', label: '양도 차익', value: '800,000', type: 'currency' },
            { key: 'replacement_deadline', label: '대체 취득 기한', value: '45일 이내', type: 'date' }
        ],
        data: {
            role: 'LA Based Real Estate Tax Expert. 1031 Exchange Specialist.',
            context: '고객이 LA K-Town 소재 상가 건물을 ${{sale_price}}에 매각하고, ${{capital_gain}}의 양도 차익에 대한 과세 이연을 원합니다. 대체 부동산 지정 기한은 {{replacement_deadline}} 입니다.',
            audience: '고객 (High Net Worth Individual) 및 부동산 에이전트.',
            task: 'Section 1031 요건 충족 여부를 검토하고, Boot(현금 수령분) 발생 시 예상 세액을 시뮬레이션 하십시오. 캘리포니아 주세(FTB)와의 차이점도 명시하십시오.',
            execution: 'Step-by-step Tax Planning Strategy. Timeline 시각화 포함.'
        }
    },
    {
        id: 'la-sba-audit',
        category: 'Audit',
        name: 'SBA Loan Audit Response',
        badge: 'Forensic',
        description: 'SBA EIDL/PPP 대출 사용 내역 감사 대응.',
        variables: [
            { key: 'loan_amount', label: '대출 금액', value: '150,000', type: 'currency' },
            { key: 'audit_period', label: '감사 대상 기간', value: '2020-2021', type: 'text' },
            { key: 'issue', label: '주요 이슈', value: '개인적 용도 자금 유용', type: 'text' }
        ],
        data: {
            role: 'Forensic Accountant specialized in SBA Loans.',
            context: '클라이언트가 ${{loan_amount}}의 EIDL 대출을 받았으며, {{audit_period}} 기간 동안의 자금 집행 내역에 대해 감사를 받고 있습니다. 이슈는 {{issue}} 입니다.',
            audience: 'SBA Auditor 및 은행 규정 준수 부서.',
            task: '자금 흐름을 추적하여 적격 비용(Qualified Expenses)으로 사용되었음을 입증하는 소명 자료를 작성하십시오. 자금의 혼재(Commingling) 이슈를 방어하십시오.',
            execution: 'Transaction Mapping 및 Evidence Table 작성.'
        }
    },
    {
        id: 'cross-border-estate',
        category: 'Specialty',
        name: 'Korea-US Estate Tax (상속세)',
        badge: 'Cross-Border',
        description: '한-미 간 자산 상속 시 이중 과세 방지 및 절세 전략.',
        variables: [
            { key: 'korea_asset', label: '한국 자산', value: '3,000,000,000', type: 'currency' },
            { key: 'us_asset', label: '미국 자산', value: '5,000,000', type: 'currency' },
            { key: 'beneficiary', label: '상속인 신분', value: 'US Citizen', type: 'text' }
        ],
        data: {
            role: 'International Tax Attorney & CPA (Korea-US Expert).',
            context: '피상속인이 한국 거주자이며 KRW {{korea_asset}}의 한국 부동산과 ${{us_asset}}의 미국 주식을 보유 중입니다. 상속인은 {{beneficiary}} 입니다.',
            audience: '상속인 가족 및 양국 세무 당국.',
            task: '한-미 상속세 조약(Treaty) 및 외국 납부 세액 공제(Foreign Tax Credit)를 활용하여 전체 실효 세율을 최소화하는 시뮬레이션을 수행하십시오.',
            execution: '국가별 납부 예상액 비교 및 신고 절차(Form 706 vs 한국 상속세 신고) 안내.'
        }
    }
];