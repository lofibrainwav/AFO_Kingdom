import argparse
import json
import os
import subprocess
import sys
import time


CUTLINE_BYTES = 20_000_000_000  # 20GB in bytes


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def parse_maxrss_bytes(time_stderr: str):
    for line in time_stderr.splitlines():
        if "maximum resident set size" in line:
            try:
                # Extract the number (could be with or without "kbytes")
                value_str = line.split(":")[-1].strip()
                value = int("".join(filter(str.isdigit, value_str)))
                # If "kbytes" is in the line, convert to bytes
                if "kbytes" in line.lower():
                    return value * 1024
                return value
            except Exception:
                return None
    return None


def run_with_time(cmd):
    p = subprocess.run(
        ["/usr/bin/time", "-l", *cmd],
        check=False,
        text=True,
        capture_output=True,
    )
    maxrss = parse_maxrss_bytes(p.stderr)
    return p.returncode, p.stdout, p.stderr, maxrss


def append_jsonl(path: str, rec: dict):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def cmd_vlm_smoke(model: str, image: str, max_tokens: int, temperature: float, prompt: str):
    return [
        sys.executable,
        "-m",
        "mlx_vlm",
        "generate",
        "--model",
        model,
        "--image",
        image,
        "--prompt",
        prompt,
        "--max-tokens",
        str(max_tokens),
        "--temperature",
        str(temperature),
    ]


def cmd_coload(vlm_model: str, llm_model: str):
    code = r"""
import resource
from mlx_vlm import load as vlm_load
from mlx_lm import load as lm_load
def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print("rss0_bytes", rss())
m1, p1 = vlm_load(__import__("os").environ["VLM_MODEL"])
print("rss_after_vlm_bytes", rss())
m2, t2 = lm_load(__import__("os").environ["LLM_MODEL"])
print("rss_after_llm_bytes", rss())
"""
    return [sys.executable, "-c", code]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="artifacts/ticket016_mlx_monitor_ssot.jsonl")
    sub = ap.add_subparsers(dest="mode", required=True)

    s1 = sub.add_parser("vlm_smoke")
    s1.add_argument("--model", required=True)
    s1.add_argument("--image", required=True)
    s1.add_argument("--max-tokens", type=int, default=140)
    s1.add_argument("--temperature", type=float, default=0.0)
    s1.add_argument(
        "--prompt", default="이 이미지에서 UI/에러 징후를 찾아서 한글로 5줄 이내로 요약해 주세요."
    )

    s2 = sub.add_parser("coload")
    s2.add_argument("--vlm-model", required=True)
    s2.add_argument("--llm-model", required=True)

    s3 = sub.add_parser("chain_run")
    s3.add_argument("--vlm-model", required=True)
    s3.add_argument("--llm-model", required=True)
    s3.add_argument("--image", required=True)
    s3.add_argument("--max-tokens", type=int, default=220)
    s3.add_argument("--temperature", type=float, default=0.7)

    args = ap.parse_args()

    t0 = time.time()
    rec = {
        "schema_version": 2,
        "ts": now_iso(),
        "mode": args.mode,
        "ok": False,
        "secs": None,
        "max_rss_bytes": None,
        "cutline_bytes": CUTLINE_BYTES,
        "status_badge": "UNKNOWN",
        "health_score": 0.0,
        "lazy_cache_hit_rate": None,
        "reload_overhead_ms": None,
        "image_pixels": None,
        "compression_ratio": None,
        "token_budget": None,
        "kv_cache_size": None,
        "model_fallback": None,
        "measured": False,
        "measurement_tool": "time",
        "confidence_level": "medium",
        "qwen_accuracy_before": None,
        "qwen_accuracy_after": None,
        "llama_quality_before": None,
        "llama_quality_after": None,
        "chain_accuracy_before": None,
        "chain_accuracy_after": None,
        "quality_metrics": None,
        "improvement_percentage": None,
        "notes": "",
    }

    if args.mode == "vlm_smoke":
        rec.update({
            "model_vlm": args.model,
            "image": args.image,
            "max_tokens": args.max_tokens,
            "temperature": args.temperature,
        })
        rc, so, se, maxrss = run_with_time(
            cmd_vlm_smoke(args.model, args.image, args.max_tokens, args.temperature, args.prompt)
        )
        rec["ok"] = rc == 0
        rec["max_rss_bytes"] = maxrss
        rec["secs"] = round(time.time() - t0, 3)
        if maxrss is not None and maxrss > CUTLINE_BYTES:
            rec["notes"] = "OVER_CUTLINE"
        append_jsonl(args.out, rec)
        print(so[:1200])
        if rc != 0:
            print(se[-2000:], file=sys.stderr)
            sys.exit(rc)

    if args.mode == "coload":
        rec.update({
            "model_vlm": args.vlm_model,
            "model_llm": args.llm_model,
            "rss_bytes_after_vlm": None,
            "rss_bytes_after_llm": None,
        })
        env = os.environ.copy()
        env["VLM_MODEL"] = args.vlm_model
        env["LLM_MODEL"] = args.llm_model
        p = subprocess.run(
            ["/usr/bin/time", "-l", *cmd_coload(args.vlm_model, args.llm_model)],
            check=False,
            text=True,
            capture_output=True,
            env=env,
        )
        rec["ok"] = p.returncode == 0
        rec["max_rss_bytes"] = parse_maxrss_bytes(p.stderr)
        rec["secs"] = round(time.time() - t0, 3)

        # stdout parsing (rss_after_* lines)
        for line in p.stdout.splitlines():
            if line.startswith("rss_after_vlm_bytes"):
                rec["rss_bytes_after_vlm"] = int(line.split()[-1])
            if line.startswith("rss_after_llm_bytes"):
                rec["rss_bytes_after_llm"] = int(line.split()[-1])

        if rec["max_rss_bytes"] is not None and rec["max_rss_bytes"] > CUTLINE_BYTES:
            rec["notes"] = "OVER_CUTLINE"

        append_jsonl(args.out, rec)
        print(p.stdout.strip()[:1200])
        if p.returncode != 0:
            print(p.stderr[-2000:], file=sys.stderr)
            sys.exit(p.returncode)

    if args.mode == "chain_run":
        rec.update({
            "model_vlm": args.vlm_model,
            "model_llm": args.llm_model,
            "image": args.image,
            "max_tokens": args.max_tokens,
            "temperature": args.temperature,
        })

        # 체인 실행: Qwen3-VL 이미지 분석 → Llama 요약 생성
        chain_code = rf"""
import os
from mlx_vlm import load as vlm_load, generate as vlm_generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config
from mlx_lm import load as lm_load, generate as llm_generate

# 모델 로드
vlm_model, vlm_proc = vlm_load("{args.vlm_model}")
cfg = load_config("{args.vlm_model}")

# 이미지 분석
image = "{args.image}"
prompt_vlm = "이 이미지에서 UI/에러 징후를 찾아서 3줄로 요약해 주세요."
formatted_prompt = apply_chat_template(vlm_proc, cfg, prompt_vlm, num_images=1)
vl_feedback = vlm_generate(vlm_model, vlm_proc, formatted_prompt, [image], max_tokens=120, verbose=False)

# Llama 요약
llm_model, llm_tok = lm_load("{args.llm_model}")
prompt_llm = f"시각 요약: {{vl_feedback}}\n해결책을 5줄로 요약해 주세요."
llm_output = llm_generate(llm_model, llm_tok, prompt=prompt_llm, max_tokens={args.max_tokens}, temperature={args.temperature}, verbose=False)

print("VL 결과:", vl_feedback[:200] + "..." if len(vl_feedback) > 200 else vl_feedback)
print("Llama 요약:", llm_output[:200] + "..." if len(llm_output) > 200 else llm_output)
"""

        cmd_chain = [sys.executable, "-c", chain_code]
        rc, so, se, maxrss = run_with_time(cmd_chain)
        rec["ok"] = rc == 0
        rec["max_rss_bytes"] = maxrss
        rec["secs"] = round(time.time() - t0, 3)

        if maxrss is not None and maxrss > CUTLINE_BYTES:
            rec["notes"] = "OVER_CUTLINE"

        append_jsonl(args.out, rec)
        print(so[:1200])
        if rc != 0:
            print(se[-2000:], file=sys.stderr)
            sys.exit(rc)


if __name__ == "__main__":
    main()
