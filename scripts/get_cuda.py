import hashlib, json, pathlib, urllib.request, zipfile
base = 'https://developer.download.nvidia.com/compute/cuda/redist/'
manifest = json.load(urllib.request.urlopen(base + 'redistrib_13.5.0.json'))
dest = pathlib.Path('work/cuda135')
dest.mkdir(parents=True, exist_ok=True)
for name in ('cccl', 'cuda_crt', 'cuda_cudart', 'cuda_nvcc'):
    item = manifest[name]['windows-arm64']
    path = pathlib.Path('work') / pathlib.Path(item['relative_path']).name
    print(name, item['size'], flush=True)
    if not path.exists(): urllib.request.urlretrieve(base + item['relative_path'], path)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            parts = pathlib.PurePosixPath(info.filename).parts
            if len(parts) < 2 or info.is_dir(): continue
            target = dest.joinpath(*parts[1:])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(z.read(info))
print('CUDA archives verified and extracted', flush=True)
