#!/bin/bash
# 환경 설정 표준화 스크립트

echo "🔧 환경 설정 표준화 시작..."

# WORKSPACE_ROOT 설정
export WORKSPACE_ROOT="/Users/brnestrm/AFO_Kingdom"
echo "export WORKSPACE_ROOT=\"$WORKSPACE_ROOT\"" >> ~/.zshrc

# PYTHONPATH 정리 및 표준화
export PYTHONPATH="$WORKSPACE_ROOT/packages/afo-core:$WORKSPACE_ROOT/packages/trinity-os"
echo "export PYTHONPATH=\"$PYTHONPATH\"" >> ~/.zshrc

# .env 파일 생성
cat > .env << ENV_EOF
WORKSPACE_ROOT=$WORKSPACE_ROOT
PYTHONPATH=$PYTHONPATH
AFO_ENV=dev
ENV_EOF

echo "✅ 환경 설정 완료"
echo "   WORKSPACE_ROOT: $WORKSPACE_ROOT"
echo "   PYTHONPATH: $PYTHONPATH"
EOF && chmod +x fix_environment.sh && echo "" && echo "🚀 IMMEDIATE FIX #2: Claude 권한 정리" && cat > fix_claude_permissions.sh << 'EOF'
#!/bin/bash
# Claude 권한 정리 스크립트

echo "🔧 Claude 권한 정리 시작..."

# 현재 권한 수 확인
current_count=$(grep -c '"Bash(' .claude/settings.local.json)
echo "현재 권한 수: $current_count"

# 핵심 권한만 남기고 정리
cat > .claude/settings.local.json << CLAUDE_EOF
{
  "permissions": {
    "allow": [
      "Bash(cd /Users/brnestrm/AFO_Kingdom && *)",
      "Bash(export PYTHONPATH=/Users/brnestrm/AFO_Kingdom/packages/afo-core:/Users/brnestrm/AFO_Kingdom/packages/trinity-os && python3 *)",
      "Bash(git status)",
      "Bash(git diff)",
      "Bash(mypy packages/afo-core --show-error-codes)",
      "Bash(ruff check packages/afo-core)",
      "Bash(docker ps)",
      "Bash(redis-cli ping)",
      "Bash(find . -name \"*.py\" | head -10)",
      "Bash(ps aux | grep python)"
    ]
  },
  "enabledMcpjsonServers": [
    "afo-ultimate-mcp",
    "afo-skills-mcp",
    "trinity-score-mcp"
  ]
}
CLAUDE_EOF

new_count=$(grep -c '"Bash(' .claude/settings.local.json)
echo "정리 후 권한 수: $new_count (감소: $((current_count - new_count)))"

echo "✅ Claude 권한 정리 완료"
EOF && chmod +x fix_claude_permissions.sh