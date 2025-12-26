import { NextRequest, NextResponse } from 'next/server';

// AFO Skills Registry에서 스킬 정보를 가져오는 API 엔드포인트
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const category = searchParams.get('category');
  const search = searchParams.get('search');
  const minPhilosophyAvg = searchParams.get('minPhilosophyAvg');

  // 실제로는 백엔드 API를 호출해야 하지만, 현재는 목업 데이터 사용
  // TODO: 백엔드 AFO Skills Registry API와 연동

  const mockSkills = [
    {
      skill_id: "skill_001_youtube_spec_gen",
      name: "YouTube to n8n Spec Generator",
      description: "Converts YouTube tutorial transcripts to executable n8n workflow specifications",
      category: "workflow_automation",
      version: "1.0.0",
      philosophy_scores: {
        truth: 95,
        goodness: 90,
        beauty: 92,
        serenity: 88
      },
      status: "active",
      capabilities: ["youtube_transcript_extraction", "llm_spec_generation", "n8n_workflow_creation"],
      execution_mode: "async"
    },
    {
      skill_id: "skill_002_ultimate_rag",
      name: "Ultimate RAG (Hybrid CRAG + Self-RAG)",
      description: "Hybrid Corrective RAG + Self-RAG implementation with Lyapunov-proven convergence",
      category: "rag_systems",
      version: "2.0.0",
      philosophy_scores: {
        truth: 98,
        goodness: 95,
        beauty: 90,
        serenity: 92
      },
      status: "active",
      capabilities: ["corrective_rag", "self_rag", "lyapunov_convergence"],
      execution_mode: "streaming"
    },
    {
      skill_id: "skill_003_health_monitor",
      name: "11-Organ Health Monitor",
      description: "Monitors 11 critical AFO system organs (五臟六腑)",
      category: "health_monitoring",
      version: "1.5.0",
      philosophy_scores: {
        truth: 100,
        goodness: 100,
        beauty: 95,
        serenity: 100
      },
      status: "active",
      capabilities: ["redis_health_check", "postgresql_health_check", "api_server_health_check"],
      execution_mode: "sync"
    }
  ];

  try {
    // Attempt to fetch from Real Backend (Truth)
    const backendUrl = 'http://localhost:8010/api/skills';
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (search) params.append('search', search);
    if (minPhilosophyAvg) params.append('min_philosophy_avg', minPhilosophyAvg);
    
    const res = await fetch(`${backendUrl}?${params.toString()}`, {
        next: { revalidate: 10 } // Edge caching
    });

    if (res.ok) {
        const data = await res.json();
        return NextResponse.json(data);
    }
    console.warn("Backend skills fetch failed, falling back to mock data");
  } catch (e) {
    console.warn("Backend skills fetch error:", e);
  }

  // Fallback to Mock Data (Graceful Degradation)
  let filteredSkills = mockSkills;

  if (category) {
    filteredSkills = filteredSkills.filter(skill => skill.category === category);
  }

  if (search) {
    const searchLower = search.toLowerCase();
    filteredSkills = filteredSkills.filter(skill => 
      skill.name.toLowerCase().includes(searchLower) ||
      skill.description.toLowerCase().includes(searchLower)
    );
  }

  if (minPhilosophyAvg) {
    const minAvg = parseFloat(minPhilosophyAvg);
    filteredSkills = filteredSkills.filter(skill => {
      const avg = (skill.philosophy_scores.truth + skill.philosophy_scores.goodness +
                  skill.philosophy_scores.beauty + skill.philosophy_scores.serenity) / 4;
      return avg >= minAvg;
    });
  }

  return NextResponse.json({
    skills: filteredSkills,
    total: filteredSkills.length,
    categories: ["strategic_command", "rag_systems", "workflow_automation", "health_monitoring", "memory_management"],
    source: "mock_fallback"
  });
}

// 스킬 실행 API
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Attempt to execute via Real Backend (Truth)
    // Note: Trailing slash is critical for FastAPI strict_slashes
    const backendUrl = 'http://localhost:8010/api/skills/';
    
    const res = await fetch(backendUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body)
    });

    if (res.ok) {
        const data = await res.json();
        return NextResponse.json(data);
    }
    
    throw new Error(`Backend execution failed: ${res.status}`);

  } catch (error) {
    console.error('Skill execution API Error:', error);
    return NextResponse.json(
      { error: 'Failed to execute skill' },
      { status: 500 }
    );
  }
}