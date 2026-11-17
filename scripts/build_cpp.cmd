@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" arm64
if errorlevel 1 exit /b %errorlevel%
set "PATH=%CD%\work\buildenv\Scripts;%CD%\work\cuda135\bin;%PATH%"
cmake --build work\cpp-build --target install --parallel 8
