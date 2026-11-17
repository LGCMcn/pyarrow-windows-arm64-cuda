@echo off
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" arm64
if errorlevel 1 exit /b %errorlevel%
set "PATH=%CD%\work\buildenv\Scripts;%CD%\work\cuda135\bin;%CD%\work\arrow-install\bin;%PATH%"
set "CMAKE_PREFIX_PATH=%CD%\work\arrow-install"
set "CUDAToolkit_ROOT=%CD%\work\cuda135"
set "PYARROW_BUNDLE_ARROW_CPP=ON"
set "PYARROW_WITH_CUDA=ON"
set "CMAKE_BUILD_PARALLEL_LEVEL=8"
work\buildenv\Scripts\python.exe -m build --wheel --no-isolation --outdir "%CD%\outputs" work\arrow\python
