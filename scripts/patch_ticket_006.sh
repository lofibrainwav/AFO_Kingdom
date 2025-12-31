#!/bin/bash
set -e

mkdir -p packages/afo-core/AFO/dspy
mkdir -p scripts
mkdir -p data/dspy

cat > packages/afo-core/AFO/dspy/factcard.py <<'EOF'
import dspy

class FactCardSig(dspy.Signature):
    question: str = dspy.InputField()
    evidence: str = dspy.InputField()
    fact_card: str = dspy.OutputField()

class FactCard(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(FactCardSig)

    def forward(self, question: str, evidence: str):
        return self.predict(question=question, evidence=evidence)
EOF

cat > packages/afo-core/AFO/dspy/client_onepager.py <<'EOF'
import dspy

class ClientOnePagerSig(dspy.Signature):
    client_context: str = dspy.InputField()
    topic: str = dspy.InputField()
    evidence: str = dspy.InputField()
    one_pager: str = dspy.OutputField()

class ClientOnePager(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(ClientOnePagerSig)

    def forward(self, client_context: str, topic: str, evidence: str):
        return self.predict(client_context=client_context, topic=topic, evidence=evidence)
EOF

cat > packages/afo-core/AFO/dspy/metrics_ticket006.py <<'EOF'
from __future__ import annotations
from difflib import SequenceMatcher

def _ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return float(SequenceMatcher(None, a, b).ratio())

def _risk_penalty(text: str) -> float:
    t = (text or "").lower()
    hits = 0
    for w in ("i think", "maybe", "might be", "not sure", "guess", "probably", "hallucinat", "unverified"):
        if w in t:
            hits += 1
    return min(hits * 0.08, 0.32)

def _has_sections(text: str, required: tuple[str, ...]) -> float:
    t = (text or "").lower()
    hit = 0
    for s in required:
        if s.lower() in t:
            hit += 1
    return hit / max(len(required), 1)

def _count_sources(text: str) -> int:
    t = (text or "")
    for key in ("Sources:", "sources:", "Citations:", "citations:"):
        if key in t:
            tail = t.split(key, 1)[1]
            lines = [ln.strip() for ln in tail.splitlines() if ln.strip()]
            return min(len(lines), 10)
    return 0

def objective_factcard(example, pred, trace=None) -> float:
    expected = getattr(example, "expected", "") or ""
    got = getattr(pred, "fact_card", "") or ""

    sim = _ratio(str(expected), str(got))
    structure = _has_sections(str(got), ("As-of", "Key point", "Now do", "Sources"))
    sources = _count_sources(str(got))
    sources_score = min(sources / 2.0, 1.0)

    risk = _risk_penalty(str(got))

    score = (0.50 * sim) + (0.30 * structure) + (0.20 * sources_score)
    if sources < 2:
        score *= 0.4
    score = max(score - risk, 0.0)
    return float(score)

def objective_onepager(example, pred, trace=None) -> float:
    expected = getattr(example, "expected", "") or ""
    got = getattr(pred, "one_pager", "") or ""

    sim = _ratio(str(expected), str(got))
    structure = _has_sections(str(got), ("As-of", "Summary", "Key changes", "Risks", "Action items", "Sources"))
    sources = _count_sources(str(got))
    sources_score = min(sources / 2.0, 1.0)

    risk = _risk_penalty(str(got))

    score = (0.50 * sim) + (0.30 * structure) + (0.20 * sources_score)
    if sources < 2:
        score *= 0.4
    score = max(score - risk, 0.0)
    return float(score)
EOF

cat > scripts/dspy_compile_factcard.py <<'EOF'
import json
import os
import dspy

from AFO.dspy.factcard import FactCard
from AFO.dspy.metrics_ticket006 import objective_factcard

def load_gold(path: str):
    examples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            ex = dspy.Example(
                question=row["question"],
                evidence=row.get("evidence", ""),
                expected=row.get("expected", ""),
            ).with_inputs("question", "evidence")
            examples.append(ex)
    return examples

def main():
    lm_name = os.environ.get("AFO_DSPY_LM", "")
    if not lm_name:
        raise SystemExit("Set AFO_DSPY_LM")
    dspy.settings.configure(lm=dspy.LM(lm_name))

    trainset = load_gold(os.environ.get("AFO_DSPY_GOLD", "data/dspy/gold_factcard.jsonl"))
    program = FactCard()

    optimizer = dspy.BootstrapFewShot(metric=objective_factcard)
    compiled = optimizer.compile(program, trainset=trainset)

    with open("data/dspy/compiled_factcard.json", "w", encoding="utf-8") as f:
        json.dump(compiled.dump_state(), f, ensure_ascii=False, indent=2)

    print("OK: data/dspy/compiled_factcard.json")

if __name__ == "__main__":
    main()
EOF

cat > scripts/dspy_compile_client_onepager.py <<'EOF'
import json
import os
import dspy

from AFO.dspy.client_onepager import ClientOnePager
from AFO.dspy.metrics_ticket006 import objective_onepager

def load_gold(path: str):
    examples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            ex = dspy.Example(
                client_context=row["client_context"],
                topic=row["topic"],
                evidence=row.get("evidence", ""),
                expected=row.get("expected", ""),
            ).with_inputs("client_context", "topic", "evidence")
            examples.append(ex)
    return examples

def main():
    lm_name = os.environ.get("AFO_DSPY_LM", "")
    if not lm_name:
        raise SystemExit("Set AFO_DSPY_LM")
    dspy.settings.configure(lm=dspy.LM(lm_name))

    trainset = load_gold(os.environ.get("AFO_DSPY_GOLD", "data/dspy/gold_client_onepager.jsonl"))
    program = ClientOnePager()

    optimizer = dspy.BootstrapFewShot(metric=objective_onepager)
    compiled = optimizer.compile(program, trainset=trainset)

    with open("data/dspy/compiled_client_onepager.json", "w", encoding="utf-8") as f:
        json.dump(compiled.dump_state(), f, ensure_ascii=False, indent=2)

    print("OK: data/dspy/compiled_client_onepager.json")

if __name__ == "__main__":
    main()
EOF

cat > scripts/dspy_optimize_factcard.py <<'EOF'
import json
import os
import sys
from importlib import import_module

import dspy
from AFO.dspy.factcard import FactCard
from AFO.dspy.metrics_ticket006 import objective_factcard

def load_gold(path: str):
    examples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            ex = dspy.Example(
                question=row["question"],
                evidence=row.get("evidence", ""),
                expected=row.get("expected", ""),
            ).with_inputs("question", "evidence")
            examples.append(ex)
    return examples

def get_optimizer():
    candidates = [
        ("dspy.teleprompt", "MIPROv2"),
        ("dspy.teleprompt", "MIPRO"),
        ("dspy.teleprompt.mipro", "MIPROv2"),
        ("dspy.teleprompt.mipro", "MIPRO"),
    ]
    for mod, cls in candidates:
        try:
            m = import_module(mod)
            if hasattr(m, cls):
                return getattr(m, cls), cls
        except Exception:
            continue
    return None, None

def main():
    lm_name = os.environ.get("AFO_DSPY_LM", "")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        try:
            from AFO.api_wallet import APIWallet
            wallet = APIWallet()
            fetched_key = wallet.get("openai", decrypt=True) or wallet.get("OPENAI_API_KEY", decrypt=True)
            if fetched_key:
                os.environ["OPENAI_API_KEY"] = fetched_key
                api_key = fetched_key
        except Exception:
            pass

    lm_kwargs = {"model": lm_name if lm_name else "openai/gpt-4o-mini"}
    if api_key:
        lm_kwargs["api_key"] = api_key
    dspy.settings.configure(lm=dspy.LM(**lm_kwargs))

    gold_path = os.environ.get("AFO_DSPY_GOLD", "data/dspy/gold_factcard.jsonl")
    trainset = load_gold(gold_path)

    program = FactCard()
    Opt, opt_name = get_optimizer()
    compiled = None

    if Opt is not None:
        try:
            optimizer = Opt(metric=objective_factcard)
            compiled = optimizer.compile(program, trainset=trainset)
            print(f"OK: optimizer={opt_name}")
        except Exception as e:
            print(f"WARN: {opt_name} failed, fallback to BootstrapFewShot: {e}", file=sys.stderr)

    if compiled is None:
        optimizer = dspy.BootstrapFewShot(metric=objective_factcard)
        compiled = optimizer.compile(program, trainset=trainset)
        print("OK: optimizer=BootstrapFewShot")

    out_path = "data/dspy/compiled_factcard.v2.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(compiled.dump_state(), f, ensure_ascii=False, indent=2)
    print(f"OK: {out_path}")

if __name__ == "__main__":
    main()
EOF

cat > scripts/dspy_optimize_client_onepager.py <<'EOF'
import json
import os
import sys
from importlib import import_module

import dspy
from AFO.dspy.client_onepager import ClientOnePager
from AFO.dspy.metrics_ticket006 import objective_onepager

def load_gold(path: str):
    examples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            ex = dspy.Example(
                client_context=row["client_context"],
                topic=row["topic"],
                evidence=row.get("evidence", ""),
                expected=row.get("expected", ""),
            ).with_inputs("client_context", "topic", "evidence")
            examples.append(ex)
    return examples

def get_optimizer():
    candidates = [
        ("dspy.teleprompt", "MIPROv2"),
        ("dspy.teleprompt", "MIPRO"),
        ("dspy.teleprompt.mipro", "MIPROv2"),
        ("dspy.teleprompt.mipro", "MIPRO"),
    ]
    for mod, cls in candidates:
        try:
            m = import_module(mod)
            if hasattr(m, cls):
                return getattr(m, cls), cls
        except Exception:
            continue
    return None, None

def main():
    lm_name = os.environ.get("AFO_DSPY_LM", "")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        try:
            from AFO.api_wallet import APIWallet
            wallet = APIWallet()
            fetched_key = wallet.get("openai", decrypt=True) or wallet.get("OPENAI_API_KEY", decrypt=True)
            if fetched_key:
                os.environ["OPENAI_API_KEY"] = fetched_key
                api_key = fetched_key
        except Exception:
            pass

    lm_kwargs = {"model": lm_name if lm_name else "openai/gpt-4o-mini"}
    if api_key:
        lm_kwargs["api_key"] = api_key
    dspy.settings.configure(lm=dspy.LM(**lm_kwargs))

    gold_path = os.environ.get("AFO_DSPY_GOLD", "data/dspy/gold_client_onepager.jsonl")
    trainset = load_gold(gold_path)

    program = ClientOnePager()
    Opt, opt_name = get_optimizer()
    compiled = None

    if Opt is not None:
        try:
            optimizer = Opt(metric=objective_onepager)
            compiled = optimizer.compile(program, trainset=trainset)
            print(f"OK: optimizer={opt_name}")
        except Exception as e:
            print(f"WARN: {opt_name} failed, fallback to BootstrapFewShot: {e}", file=sys.stderr)

    if compiled is None:
        optimizer = dspy.BootstrapFewShot(metric=objective_onepager)
        compiled = optimizer.compile(program, trainset=trainset)
        print("OK: optimizer=BootstrapFewShot")

    out_path = "data/dspy/compiled_client_onepager.v2.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(compiled.dump_state(), f, ensure_ascii=False, indent=2)
    print(f"OK: {out_path}")

if __name__ == "__main__":
    main()
EOF

cat > data/dspy/gold_factcard.jsonl <<'EOF'
{"question":"Summarize the change in policy X for 2025 clients.","evidence":"(paste verified evidence snippets here)","expected":"As-of: 2025-12-30\nKey point: ...\nNow do:\n- ...\nWarnings:\n- ...\nSources:\n- source1\n- source2"}
EOF

cat > data/dspy/gold_client_onepager.jsonl <<'EOF'
{"client_context":"CPA client email blast. Audience: non-technical. Tone: clear, firm, friendly.","topic":"2025 personal income tax changes overview","evidence":"(paste verified evidence snippets here)","expected":"As-of: 2025-12-30\nSummary: ...\nKey changes:\n- ...\nRisks:\n- ...\nAction items:\n- ...\nSources:\n- source1\n- source2"}
EOF
