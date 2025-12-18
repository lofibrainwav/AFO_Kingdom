@echo off
REM TRINITY-OS Windows 배치 파일

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM 명령어 인수 처리
if "%1"=="init" goto init
if "%1"=="test" goto test
if "%1"=="run" goto run
if "%1"=="verify" goto verify
if "%1"=="detect" goto detect
if "%1"=="health" goto health
if "%1"=="spirit" goto spirit
if "%1"=="unified" goto unified
if "%1"=="infinite" goto infinite
if "%1"=="help" goto help
if "%1"=="-h" goto help
if "%1"=="--help" goto help

:run
bash run_trinity_os.sh
goto end

:init
bash init_trinity_os.sh
goto end

:test
bash test_trinity_os.sh
goto end

:verify
bash scripts/verify_all_scripts.sh
goto end

:detect
python scripts/kingdom_problem_detector.py
goto end

:health
python scripts/kingdom_health_report.py
goto end

:spirit
python scripts/kingdom_spirit_integration.py
goto end

:unified
bash scripts/kingdom_unified_autorun.sh
goto end

:infinite
bash scripts/kingdom_infinite_autorun.sh
goto end

:help
echo TRINITY-OS 명령어 도움말
echo.
echo 사용법: TRINITY-OS.bat [command]
echo.
echo 명령어:
echo   init     - 시스템 초기화
echo   test     - 시스템 테스트
echo   run      - 인터랙티브 실행
echo   verify   - 검증 실행
echo   detect   - 문제 감지
echo   health   - 건강 리포트
echo   spirit   - 정신 통합
echo   unified  - 통합 자동화
echo   infinite - 끝까지 오토런
echo   help     - 이 도움말
echo.
goto end

:end