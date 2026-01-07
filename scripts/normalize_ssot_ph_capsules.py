import re
import sys
from pathlib import Path

HDR_RE = re.compile(r"^##\s+\[(SSOT/PH-[^\]]+)\](.*)$", re.M)
END_RE = re.compile(r"(?=^##\s+\[|\Z)", re.M)

def parse_lines(block: str):
    status = None
    scope = None
    evidence = []
    gaps = None

    for line in block.splitlines():
        s = line.strip()

        m = re.match(r"^(Status|상태)\s*:\s*(.+)$", s, re.I)
        if m and status is None:
            status = m.group(2).strip()
            continue

        m = re.match(r"^(Scope|범위)\s*:\s*(.+)$", s, re.I)
        if m and scope is None:
            scope = m.group(2).strip()
            continue

        if re.match(r"^(Evidence|증거)\s*:", s, re.I):
            continue
        if re.match(r"^(Gaps|갭|미해결)\s*:", s, re.I):
            gaps = "none"
            continue

        if s.startswith("- "):
            if gaps == "none":
                gaps = s[2:].strip()
            else:
                evidence.append(s[2:].strip())

    if status is None:
        if re.search(r"\bSEALED\b", block, re.I):
            status = "SEALED"
        elif re.search(r"\bPARTIAL\b", block, re.I):
            status = "PARTIAL"
        elif re.search(r"\bPENDING\b", block, re.I):
            status = "PENDING"
        else:
            status = "SEALED"

    if scope is None:
        scope = "SSOT update"

    ev = [e for e in evidence if e]
    if len(ev) > 3:
        extra = len(ev) - 3
        ev = ev[:3]
        ev.append(f"+{extra} more")

    if not ev:
        ev = ["(no evidence lines detected)"]

    if gaps is None:
        gaps = "none"
    elif isinstance(gaps, str) and gaps != "none":
        gaps = gaps
    else:
        gaps = "none"

    return status, scope, ev, gaps

def to_capsule(tag: str, tail: str, status: str, scope: str, ev: list[str], gaps: str):
    ev_str = "; ".join(ev)
    return "\n".join([
        f"## [{tag}]{tail}".rstrip(),
        f"- Status: {status}",
        f"- Scope: {scope}",
        f"- Evidence: {ev_str}",
        f"- Gaps: {gaps}",
        ""
    ])

def normalize_text(text: str) -> str:
    out = []
    i = 0
    while True:
        m = HDR_RE.search(text, i)
        if not m:
            out.append(text[i:])
            break
        out.append(text[i:m.start()])
        tag = m.group(1)
        tail = m.group(2) or ""
        end = END_RE.search(text, m.start())
        block = text[m.start(): end.start() if end else len(text)]
        status, scope, ev, gaps = parse_lines(block)
        out.append(to_capsule(tag, tail, status, scope, ev, gaps))
        i = end.start() if end else len(text)
    return "".join(out)

def main():
    if len(sys.argv) < 2:
        print("usage: normalize_ssot_ph_capsules.py <file.md> [--write]", file=sys.stderr)
        sys.exit(2)
    p = Path(sys.argv[1])
    write = "--write" in sys.argv[2:]
    text = p.read_text(encoding="utf-8")
    new = normalize_text(text)
    if not write:
        sys.stdout.write(new)
        return
    bak = p.with_suffix(p.suffix + ".bak")
    bak.write_text(text, encoding="utf-8")
    p.write_text(new, encoding="utf-8")

if __name__ == "__main__":
    main()