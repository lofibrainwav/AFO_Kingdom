import json, time
from pathlib import Path

def main():
    out = Path("artifacts/mipro_runs") / f"mipro_light_{int(time.time())}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    # TODO: 여기에 형님 왕국의 unoptimized_rag / trinity_metric / trainset 연결
    # 지금은 러너 뼈대만 SSOT로 봉인합니다.
    record = {"ts": time.time(), "status": "runner_created", "auto": "light", "num_trials": 20}
    out.write_text(json.dumps(record) + "\n", encoding="utf-8")
    print(str(out))

if __name__ == "__main__":
    main()
