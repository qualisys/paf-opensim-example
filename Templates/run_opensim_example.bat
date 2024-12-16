
@echo off

cd /d "%~dp0"
call conda activate opensim_example
python "%~dp0qtm2opensim.py" --c3d_dir "%~1"
exit /b 0

