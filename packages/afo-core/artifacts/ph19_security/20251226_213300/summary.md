# PH19 Security Sweep Summary (20251226_213300)

- pip-audit: vulnerabilities=0 rc=0
- gitleaks: findings=n/a rc=127
- bandit: findings=80 rc=1

## Gate rule
- PASS = all rc == 0
- FAIL = any rc != 0 (including missing tools)