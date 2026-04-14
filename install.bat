@echo off
set "SCRIPT_PATH=%~dp0constract.py"
echo @echo off > "%~dp0constract.bat"
echo python "%SCRIPT_PATH%" %%* >> "%~dp0constract.bat"
echo "constract.bat has been created in %~dp0"
pause
