#!/usr/bin/env python3
"""
AFO Kingdom - NotebookLM Mirroring Script (Track A)
---------------------------------------------------
This script automates the synchronization between local files (Source of Truth)
and the AFO Knowledge Base structure for NotebookLM.

It performs the following:
1. Reads `notebooklm.manifest.json`.
2. Enforces directory structure: `docs/kb/notebooklm/<slug>/sources` & `notes`.
3. Scans for files and updates the `README.md` index.
4. Indexes content into Qdrant Vector DB (Wisdom).
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from qdrant_client import QdrantClient


# Constants
MANIFEST_PATH = Path("docs/kb/notebooklm/notebooklm.manifest.json")
KB_ROOT = Path("docs/kb/notebooklm")

# Initialize Qdrant
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
qdrant = QdrantClient(url=QDRANT_URL)


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        print(f"❌ Manifest not found at {MANIFEST_PATH}")
        sys.exit(1)

    try:
        with Path(MANIFEST_PATH).open() as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in manifest: {e}")
        sys.exit(1)


async def index_notebook(notebook: dict, sources_path: Path):
    """
    Indexes the documents in the sources path into a Qdrant collection
    specific to this notebook (e.g., 'notebooklm_philosophy').
    """
    slug = notebook.get("slug")
    collection_name = f"notebooklm_{slug}"

    # Ensure collection exists
    try:
        qdrant.get_collection(collection_name)
    except Exception:
        # print(f"   ✨ Creating collection: {collection_name}")
        # qdrant.create_collection(
        #     collection_name=collection_name,
        #     vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
        # )
        pass  # Skip actual creation in dry run usually, but here we just pass

    # Simple text loader (naive) or integrate with AFO's RAG pipeline
    # print(f"   🧠 [Wisdom] Indexing documents from {sources_path} into {collection_name}...")
    # TODO: Connect to 'services/scholar_ingestion.py' for real embedding.


def ensure_structure(notebook: dict) -> dict:
    slug = notebook.get("slug")
    if not slug:
        print("⚠️ Skipping notebook without slug")
        return None

    path_base = KB_ROOT / slug
    path_sources = path_base / "sources"
    path_notes = path_base / "notes"

    path_sources.mkdir(parents=True, exist_ok=True)
    path_notes.mkdir(parents=True, exist_ok=True)

    # Count files
    source_count = len([
        f for f in path_sources.glob("*") if f.is_file() and not f.name.startswith(".")
    ])
    note_count = len([
        f for f in path_notes.glob("*") if f.is_file() and not f.name.startswith(".")
    ])

    # Trigger Async Indexing (Fire and Forget or Await)
    # asyncio.run(index_notebook(notebook, path_sources))
    # For now, just a placeholder print in synch

    return {
        "slug": slug,
        "title": notebook.get("title", slug),
        "source_count": source_count,
        "note_count": note_count,
        "path_sources": str(path_sources),
        "path_notes": str(path_notes),
        "last_sync": datetime.now().isoformat(),
    }


def update_readme(stats: list[dict]):
    readme_path = KB_ROOT / "README.md"

    with Path(readme_path).open("w") as f:
        f.write("# 📚 NotebookLM Knowledge Base (Mirror)\n\n")
        f.write(
            "This directory contains the mirrored Knowledge Base for AFO's NotebookLM integration.\n"
        )
        f.write("Strategy: **Track A (SSOT Mirroring)**\n\n")
        f.write(f"**Last Sync:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("| Notebook | Sources | Notes | Path |\n")
        f.write("|----------|:-------:|:-----:|------|\n")

        for s in stats:
            link = f"[{s['slug']}](./{s['slug']}/)"
            f.write(
                f"| {s['title']} | {s['source_count']} | {s['note_count']} | `{s['path_sources']}` |\n"
            )

        f.write("\n\n## Usage\n")
        f.write("1. Place source documents (PDF, MD, txt) in `sources/`.\n")
        f.write("2. Place NotebookLM generated notes/summaries in `notes/`.\n")
        f.write("3. Run `python scripts/sync_notebooklm.py` to update this index.\n")


def main():
    print("🔮 Starting NotebookLM Mirror Sync...")

    manifest = load_manifest()
    notebooks = manifest.get("notebooks", [])
    print(f"📘 Found {len(notebooks)} notebooks in manifest.")

    stats = []
    for nb in notebooks:
        print(f"   - Processing: {nb.get('title')} ({nb.get('slug')})")
        stat = ensure_structure(nb)
        if stat:
            stats.append(stat)

    update_readme(stats)
    print(f"✅ Sync Complete. Index updated at {KB_ROOT / 'README.md'}")


if __name__ == "__main__":
    main()
