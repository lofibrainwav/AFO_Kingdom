# Trinity Score: 90.0 (Established by Chancellor)
"""
Git Status API
Git 저장소 상태 조회 엔드포인트
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/git", tags=["Git Status"])

logger = logging.getLogger(__name__)

# 프로젝트 루트 경로 (Docker vs Host)
if Path("/workspace").exists():
    WORKSPACE_ROOT = Path("/workspace")
    # Docker에서 .git 소유권 문제 해결을 위해 safe directory 설정 필요할 수 있음
    # 하지만 여기서는 git command 실행 시 설정 추가가 더 안전함
else:
    WORKSPACE_ROOT = Path("/Users/brnestrm/AFO_Kingdom")


def _run_git_command(cmd_str: str) -> str:
    """Git 명령어 실행"""
    try:
        # T27: Docker Volume Mount 시 safe.directory 이슈 방지
        # cmd_str은 space로 분리된 문자열이라고 가정 (legacy support)
        args = ["git", "-c", "safe.directory=*"] + cmd_str.replace("git ", "", 1).split()
        
        result = subprocess.run(
            args,
            cwd=WORKSPACE_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return ""
    except Exception as e:
        logger.warning(f"Git command failed: {cmd_str}, error: {e}")
        return ""


@router.get("/status")
async def get_git_status() -> dict[str, Any]:
    """
    Git 저장소 상태 조회

    Returns:
        - total_commits: 전체 커밋 수
        - today_commits: 오늘 커밋 수
        - head: 현재 HEAD SHA
        - branch: 현재 브랜치
        - synced: 동기화 상태 (uncommitted changes 여부)
        - status: git status 출력
        - recent_commits: 최근 커밋 목록
    """
    try:
        # 기본 Git 정보
        total_commits = _run_git_command("git rev-list --count HEAD")
        head_sha = _run_git_command("git rev-parse --short HEAD")
        branch = _run_git_command("git branch --show-current")
        status_output = _run_git_command("git status --porcelain")

        # 오늘 커밋 수
        today_commits_cmd = ["git", "log", "--oneline", "--since=midnight"]
        try:
            result = subprocess.run(
                today_commits_cmd,
                cwd=WORKSPACE_ROOT,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                # Python에서 라인 수 계산
                count = len(result.stdout.strip().splitlines()) if result.stdout.strip() else 0
                today_commits = str(count)
            else:
                today_commits = "0"
        except Exception:
            today_commits = "0"

        # 최근 커밋 목록
        recent_commits_output = _run_git_command("git log --oneline -10")
        recent_commits = []
        if recent_commits_output:
            for line in recent_commits_output.split("\n"):
                if line.strip():
                    parts = line.split(" ", 1)
                    if len(parts) == 2:
                        recent_commits.append(
                            {"hash": parts[0], "message": parts[1][:50]}
                        )

        # 동기화 상태
        synced = not bool(status_output)

        # 추적 중인 파일 수
        tracked_files = _run_git_command("git ls-tree -r HEAD --name-only | wc -l")

        return {
            "status": "success",
            "total_commits": int(total_commits) if total_commits.isdigit() else 0,
            "today_commits": (
                int(today_commits.strip()) if today_commits.strip().isdigit() else 0
            ),
            "head": head_sha,
            "branch": branch or "unknown",
            "synced": synced,
            "has_changes": not synced,
            "status_output": status_output,
            "tracked_files": (
                int(tracked_files.strip()) if tracked_files.strip().isdigit() else 0
            ),
            "recent_commits": recent_commits,
        }
    except Exception as e:
        logger.error(f"Git status check failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get git status: {e}"
        ) from e


@router.get("/info")
async def get_git_info() -> dict[str, Any]:
    """
    Git 저장소 상세 정보 조회

    Returns:
        - remote: 원격 저장소 정보
        - config: Git 설정 정보
        - tags: 태그 목록
    """
    try:
        # 원격 저장소 정보
        remote_url = _run_git_command("git config --get remote.origin.url")

        # 태그 목록
        tags_output = _run_git_command("git tag -l | tail -10")
        tags = (
            [tag.strip() for tag in tags_output.split("\n") if tag.strip()]
            if tags_output
            else []
        )

        # 사용자 정보
        user_name = _run_git_command("git config user.name")
        user_email = _run_git_command("git config user.email")

        return {
            "status": "success",
            "remote": {
                "url": remote_url,
            },
            "user": {
                "name": user_name,
                "email": user_email,
            },
            "tags": tags,
        }
    except Exception as e:
        logger.error(f"Git info check failed: {e}")
@router.get("/history")
async def get_git_history(limit: int = 100) -> dict[str, Any]:
    """
    Git 커밋 히스토리 조회 (T27 Phase 2)
    
    Args:
        limit: 조회할 커밋 수 (기본 100)
    
    Returns:
        - history: 커밋 목록 (hash, parent, author, date, message)
    """
    try:
        # 형식: 해시|부모해시|작성자|날짜|메시지
        cmd = [
            "git",
            "-c", "safe.directory=*",
            "log",
            f"-n {limit}",
            "--pretty=format:%H|%p|%an|%ad|%s",
            "--date=iso"
        ]
        
        result = subprocess.run(
            cmd,
            cwd=WORKSPACE_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        
        history = []
        if result.returncode == 0:
            for line in result.stdout.strip().splitlines():
                if not line:
                    continue
                try:
                    parts = line.split("|", 4)
                    if len(parts) >= 5:
                        history.append({
                            "hash": parts[0],
                            "parent": parts[1],
                            "author": parts[2],
                            "date": parts[3],
                            "message": parts[4]
                        })
                except Exception:
                    continue
                    
        return {
            "status": "success",
            "count": len(history),
            "history": history
        }
            
    except Exception as e:
        logger.error(f"Git history check failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get git history: {e}"
        ) from e

