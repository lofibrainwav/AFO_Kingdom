
import sys
import os
import asyncio

# Setup path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/afo-core")))

from services.sejong_researcher import sejong

async def verify_sejong_system():
    print("🔭 [Sejong Institute] Verification Start")
    
    # 1. Research
    topic = "Python 3.13 NO_GIL"
    print(f"\n1. Researching: {topic}...")
    findings = sejong.research_topic(topic)
    print(f"   -> Found: {findings['summary']}")
    
    # 2. Validate (Sisi-Bibi)
    print(f"\n2. Validating (Sisi-Bibi)...")
    score = sejong.sisi_bibi_validation(findings)
    print(f"   -> Trinity Score: {score}")
    
    if score >= 90.0:
        print("   ✅ Passed Validation (> 90)")
    else:
        print("   ❌ Failed Validation")
        return

    # 3. Adopt
    print(f"\n3. Adopting Knowledge...")
    success = sejong.adopt_knowledge(findings, score)
    
    if success:
        print("   ✅ Knowledge saved to Archives (knowledge_base.jsonl)")
    else:
        print("   ❌ Failed to save knowledge")
        
    print("\n[Verification Complete] Sejong Research System Operational.")

if __name__ == "__main__":
    asyncio.run(verify_sejong_system())
