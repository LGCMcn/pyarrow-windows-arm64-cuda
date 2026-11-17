import io, platform, sys
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.cuda as cuda
print('Python:', sys.version)
print('Architecture:', platform.machine())
print('PyArrow:', pa.__version__)
table = pa.table({'id': [1, 2, 3], 'text': ['a', 'b', 'c']})
sink = pa.BufferOutputStream()
pq.write_table(table, sink, compression='zstd')
assert pq.read_table(pa.BufferReader(sink.getvalue())).equals(table)
print('Parquet Zstandard roundtrip: PASS')
context = cuda.Context(0)
src = b'Arrow on Windows ARM64 CUDA 13.5'
device_buffer = context.new_buffer(len(src))
device_buffer.copy_from_host(src)
assert device_buffer.copy_to_host().to_pybytes() == src
print('CUDA allocation and host/device roundtrip: PASS')
