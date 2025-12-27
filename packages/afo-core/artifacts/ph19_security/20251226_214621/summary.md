# PH19 Security Sweep Summary (20251226_214621)

- pip-audit: vulnerabilities=0 rc=0
- gitleaks: findings=50 rc=1
- bandit: findings=0 rc=0

## Gate rule
- PASS = all rc == 0
- FAIL = any rc != 0 (including missing tools)