import math
from time import time
import ctypes
import mmap

buf_s = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
ftype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
fpointer_s = ctypes.c_void_p.from_buffer(buf_s)
f_s = ftype(ctypes.addressof(fpointer_s))

buf_s.write(
    b'\x8b\xc7'  # mov eax, edi
    b'\x83\xc0\x01'  # add eax, 1
    b'\x0f\x1f\x84\xbe\x00\x00\x01\x01' # nop
    b'\xc3' #ret
)

buf_e = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
ftype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
fpointer_e = ctypes.c_void_p.from_buffer(buf_e)
f_e = ftype(ctypes.addressof(fpointer_e))

buf_e.write(
    b'\x8b\xc7'  # mov eax, edi
    b'\x83\xc0\x01'  # add eax, 1
    b'\x0f\x1f\x84\xed\x00\x00\x01\x01' # nop
    b'\xc3' #ret
)

def float_operations(n):
    start = time()
    for i in range(0, n):
        sin_i = math.sin(i)
        cos_i = math.cos(i)
        sqrt_i = math.sqrt(i)
    latency = time() - start
    return latency


def main(event):
    f_s(0)
    latencies = {}
    timestamps = {}
    timestamps["starting_time"] = time()
    n = int(event['n'])
    metadata = event['metadata']
    latency = float_operations(n)
    latencies["function_execution"] = latency
    timestamps["finishing_time"] = time()
    f_e(0)
    return {"latencies": latencies, "timestamps": timestamps, "metadata": metadata}
