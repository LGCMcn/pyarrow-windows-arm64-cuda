# PyArrow for Windows ARM64 with CUDA

Unofficial community build of Apache Arrow/PyArrow **26.0.1** for CPython **3.14** (standard GIL build), Windows ARM64, built against NVIDIA CUDA Toolkit **13.5.0**. It is not an Apache Arrow or NVIDIA release.

Download the wheel from [Releases](../../releases), then install it with an ARM64 Python 3.14:

```powershell
python -m pip install .\pyarrow-26.0.1-cp314-cp314-win_arm64.whl
python -c "import pyarrow as pa; import pyarrow.cuda; print(pa.__version__)"
```

SHA-256: `5444de556cb7d8cd8c79b41939998b3ca639296cb883cbb5d2a43ef30dd5cd6b`.

Tested on Windows ARM64, Python 3.14.10, NVIDIA RTX Spark N1X, driver 617.69. Verified import, Parquet Zstandard round trip, CUDA device allocation and copying bytes from host to device and back. This is not a comprehensive test suite, and other hardware and drivers have not been tested. A CUDA-capable NVIDIA GPU and compatible Windows ARM64 driver are needed for CUDA operations. NVIDIA documents CUDA 13.x minor-version compatibility with driver 580 or newer, subject to platform and feature restrictions; CUDA 13.5 new features require an R620 or newer driver. Consult [NVIDIA release notes](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/).

`pyarrow.cuda` provides Arrow CUDA buffers and interoperability; it does not automatically run ordinary Arrow compute or Parquet operations on the GPU. The wheel includes Arrow C++ libraries; it does not include the NVIDIA driver. Enabled features include compute, CSV, JSON, dataset, filesystem, Acero, Parquet, CUDA, Brotli, LZ4, Snappy, Zstandard and zlib. S3, GCS, Azure, Flight, RE2, UTF8PROC and Parquet encryption were not enabled. It has the same version as upstream; pin the wheel hash if this particular build is required.

## Build record

Source: Apache Arrow tag `apache-arrow-26.0.1`, commit `9e5d6978e9acf372cc989aaaf94e863fe8582c90`. The `scripts` directory records the commands used. It assumes the repository is a sibling of a `work` directory under the current directory; build paths may be adjusted for your system. Visual Studio 2022 Build Tools with native ARM64 C++ and Windows SDK, Python 3.14 ARM64, internet access and adequate disk space are required.

1. Clone Arrow to `work/arrow` at the commit above; create `work/buildenv` using `python -m venv work/buildenv`. Install `numpy cython scikit-build-core cmake ninja build wheel libcst setuptools_scm` into it.
2. Run `python scripts/get_cuda.py` and `python scripts/download_boost.py` from the working root. NVIDIA CUDA archives and Boost are verified against SHA-256 manifests. Set `work/configure.cmd`, `work/build_cpp.cmd`, and `work/build_wheel.cmd` by copying the corresponding scripts.
3. Run `work/configure.cmd`. In `work/cpp-build/_deps/thrift-src/lib/cpp/src/thrift/transport/TSocketPool.cpp`, replace both `#if __cplusplus >= 201703L` checks with `#if __cplusplus >= 201703L || (defined(_MSVC_LANG) && _MSVC_LANG >= 201703L)`. This selects the C++17 shuffle path on MSVC. `CXX_LINKER_SUPPORTS_VERSION_SCRIPT=OFF` avoids a false-positive GNU linker flag probe on MSVC.
4. Run `work/build_cpp.cmd` and `work/build_wheel.cmd`. Run `work/buildenv/Scripts/python.exe scripts/add_licenses.py` to add third-party license texts and repack the wheel. Repacking changes its hash. Test in a fresh virtual environment with `scripts/smoke_test.py`.

Arrow is distributed under Apache License 2.0. The wheel contains upstream LICENSE and NOTICE plus third-party license files in its `.dist-info/licenses` directory. NVIDIA CUDA Toolkit is obtained separately under NVIDIA's terms; no CUDA Toolkit runtime DLL is bundled in this wheel.
