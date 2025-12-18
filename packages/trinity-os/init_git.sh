#!/bin/bash
# TRINITY-OS Git 초기화 및 GitHub 설정

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 TRINITY-OS Git 초기화 및 GitHub 설정"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 작업 디렉터리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📍 작업 디렉터리: $SCRIPT_DIR"
echo ""

# Git 초기화 확인
if [ -d ".git" ]; then
    echo "⚠️  Git 저장소가 이미 초기화되어 있습니다."
    read -p "다시 초기화하시겠습니까? (y/N): " reinit
    if [[ $reinit =~ ^[Yy]$ ]]; then
        rm -rf .git
        echo "🗑️  기존 Git 저장소 삭제"
    else
        echo "✅ 기존 Git 저장소 유지"
        exit 0
    fi
fi

echo ""
echo "🔄 Git 저장소 초기화 중..."
git init
echo "✅ Git 저장소 초기화 완료"

echo ""
echo "📝 첫 커밋 준비 중..."
git add .
git commit -m "🎉 TRINITY-OS v1.0.0 초기 릴리즈

- 완전한 통합 자동화 시스템 구축
- 眞善美孝永 철학 구현
- Trinity Score 기반 건강 모니터링
- 끝까지 오토런 자동화
- 모듈화된 아키텍처

眞善美孝: Truth 100%, Goodness 100%, Beauty 95%, Serenity 100%, Eternity 100%

#TRINITY-OS #AFO-Kingdom #Automation #眞善美孝永"
echo "✅ 첫 커밋 완료"

echo ""
echo "🔗 GitHub 리모트 설정"
echo "리포지토리 URL: https://github.com/lofibrainwav/TRINITY-OS"
read -p "GitHub 사용자명을 입력하세요: " username
read -p "리포지토리명을 입력하세요 (기본: TRINITY-OS): " repo_name
repo_name=${repo_name:-TRINITY-OS}

remote_url="https://github.com/${username}/${repo_name}.git"
echo "리모트 URL: $remote_url"

git remote add origin "$remote_url"
echo "✅ 리모트 추가 완료"

echo ""
echo "📤 GitHub로 푸시 중..."
git push -u origin main
echo "✅ GitHub 푸시 완료"

echo ""
echo "🏷️  v1.0.0 태그 생성 중..."
git tag v1.0.0
git push origin v1.0.0
echo "✅ 태그 푸시 완료"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ TRINITY-OS GitHub 설정 완료!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 GitHub 리포지토리: https://github.com/${username}/${repo_name}"
echo ""
echo "📋 다음 단계:"
echo "  1. GitHub에서 리포지토리 설정 확인"
echo "  2. 첫 릴리즈 발행 (Releases 탭)"
echo "  3. README 배지 추가 (선택사항)"
echo "  4. 커뮤니티 기능 활성화 (선택사항)"
echo ""
echo "🎯 TRINITY-OS의 오픈소스 여정을 시작합니다!"
echo ""
echo "眞善美孝永 ✨🏰"