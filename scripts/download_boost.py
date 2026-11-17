import concurrent.futures, hashlib, pathlib, urllib.request
url = 'https://github.com/boostorg/boost/releases/download/boost-1.92.0/boost-1.92.0-cmake.tar.gz'
size = 142762026
chunk = 8 * 1024 * 1024
out = pathlib.Path('work/boost-parts'); out.mkdir(exist_ok=True)
def fetch(i):
    start=i*chunk; end=min(start+chunk,size)-1
    path=out / str(i)
    if path.exists() and path.stat().st_size == end-start+1: return
    req=urllib.request.Request(url, headers={'Range':f'bytes={start}-{end}'})
    with urllib.request.urlopen(req,timeout=120) as src:
        assert src.status == 206, src.status
        path.write_bytes(src.read())
    assert path.stat().st_size == end-start+1
    print(i, flush=True)
n=(size+chunk-1)//chunk
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: list(pool.map(fetch, range(n)))
with open('work/boost-complete.tar.gz','wb') as dst:
    for i in range(n): dst.write((out/str(i)).read_bytes())
assert hashlib.sha256(pathlib.Path('work/boost-complete.tar.gz').read_bytes()).hexdigest() == 'f51707c27359a0df0cac1beada86de31bb5eed5e8285592dadec384df99c2984'
print('verified',flush=True)
