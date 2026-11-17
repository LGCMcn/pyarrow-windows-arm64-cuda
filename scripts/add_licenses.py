from pathlib import Path
import shutil, subprocess, sys
root=Path('work/cpp-build')
sources={p.name.removesuffix('-src'):p for p in (root/'_deps').glob('*-src')}
for name in ('brotli','snappy','zlib','zstd'):
    sources[name]=root/(name+'_ep-prefix')/'src'/(name+'_ep')
wheel=next(Path('outputs').glob('*.whl'))
subprocess.run([sys.executable,'-m','wheel','unpack',str(wheel),'-d','work/unpacked'],check=True)
unpacked=next(Path('work/unpacked').glob('pyarrow-*'))
dest=next(unpacked.glob('*.dist-info'))/'licenses'/'third-party'
for name, source in sources.items():
    files=[p for p in source.iterdir() if p.is_file() and (p.name.lower().startswith(('license','copying','notice')))]
    print(name, [p.name for p in files])
    for f in files:
        target=dest/name/f.name; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(f,target)
subprocess.run([sys.executable,'-m','wheel','pack',str(unpacked),'-d','outputs'],check=True)
