from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Context7Meta:
    path: str
    category: str = "Uncategorized"
    description: str = ""
    tags: tuple[str, ...] = ()
    type: str = "document"  # default; may be overridden or inferred


def _iter_meta_objects(obj: Any) -> Iterable[dict[str, Any]]:
    """
    Accepts flexible JSON shapes:
    - list of {path,...}
    - dict containing nested lists/dicts with {path,...}
    - dict mapping path -> meta
    """
    if isinstance(obj, list):
        for x in obj:
            yield from _iter_meta_objects(x)
        return

    if isinstance(obj, dict):
        # case: {"some/path.md": {...}}
        if "path" not in obj and all(
            isinstance(k, str) and isinstance(v, dict) for k, v in obj.items()
        ):
            for k, v in obj.items():
                if "path" not in v:
                    v = {**v, "path": k}
                yield from _iter_meta_objects(v)
            return

        if "path" in obj and isinstance(obj["path"], str):
            yield obj
            return

        for v in obj.values():
            yield from _iter_meta_objects(v)
        return


def _infer_type(path: str) -> str:
    p = Path(path)
    suf = p.suffix.lower()
    if suf in {".py"}:
        return "code/python"
    if suf in {".ts", ".tsx"}:
        return "code/typescript"
    if suf in {".js", ".jsx"}:
        return "code/javascript"
    if suf in {".json"}:
        return "document"  # keep safest; content will include meta header
    if suf in {".md", ".markdown", ".txt", ""}:
        return "document"
    return "document"


def load_context7_metadata(repo_root: Path) -> dict[str, Context7Meta]:
    meta_path = repo_root / "docs" / "context7_integration_metadata.json"
    if not meta_path.exists():
        # Fallback: try finding it relative to current file if repo_root is ambiguous
        fallback_path = (
            Path(__file__).resolve().parent.parent.parent.parent.parent
            / "docs"
            / "context7_integration_metadata.json"
        )
        if fallback_path.exists():
            meta_path = fallback_path
        else:
            return {}

    import json

    try:
        raw = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return {}

    out: dict[str, Context7Meta] = {}
    for m in _iter_meta_objects(raw):
        # Handle dict format where key is the name/ID, not just path
        if "file" in m:
            m["path"] = m["file"]

        rel = str(m.get("path", "")).strip()
        if not rel:
            continue

        category = str(m.get("category", "Uncategorized")).strip() or "Uncategorized"
        description = str(m.get("description", "")).strip()
        tags_raw = m.get("tags", [])
        tags: tuple[str, ...]
        if isinstance(tags_raw, list):
            tags = tuple(str(t).strip() for t in tags_raw if str(t).strip())
        else:
            tags = tuple(x for x in (str(tags_raw).strip(),) if x)

        typ = str(m.get("type", "")).strip() or _infer_type(rel)

        out[rel] = Context7Meta(
            path=rel,
            category=category,
            description=description,
            tags=tags,
            type=typ,
        )

    return out


def inject_meta_header(meta: Context7Meta, content: str) -> str:
    header = [
        "---",
        f"category: {meta.category}",
        f"description: {meta.description}",
        f"tags: {', '.join(meta.tags)}",
        f"source: {meta.path}",
        f"type: {meta.type}",
        "---",
        "",
    ]
    return "\n".join(header) + content
