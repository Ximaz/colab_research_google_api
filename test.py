import ctypes

chunk_arg_type = ctypes.c_ubyte * 64
w_arg_type = ctypes.c_uint * 64
hash_arg_type = ctypes.c_uint * 8

lib = ctypes.CDLL("./libgoogcrypto.so")
lib.hashFunction.argtypes = [chunk_arg_type, w_arg_type, hash_arg_type]

chunk_ = [
    91,
    91,
    34,
    102,
    105,
    108,
    101,
    73,
    100,
    34,
    93,
    44,
    91,
    34,
    49,
    52,
    109,
    78,
    117,
    114,
    106,
    53,
    100,
    48,
    76,
    68,
    69,
    83,
    56,
    117,
    52,
    83,
    73,
    56,
    78,
    87,
    79,
    73,
    75,
    114,
    90,
    89,
    49,
    114,
    90,
    80,
    51,
    34,
    93,
    93,
    128,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    144,
]
w_ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
hash_ = [
    1779033703,
    3144134277,
    1013904242,
    2773480762,
    1359893119,
    2600822924,
    528734635,
    1541459225,
]
chunk_ = chunk_arg_type(*chunk_)
w_ = w_arg_type(*w_)
hash_ = hash_arg_type(*hash_)
lib.hashFunction(chunk_, w_, hash_)
print(list(hash_))