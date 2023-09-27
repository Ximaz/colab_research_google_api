MG = [
    1116352408,
    1899447441,
    3049323471,
    3921009573,
    961987163,
    1508970993,
    2453635748,
    2870763221,
    3624381080,
    310598401,
    607225278,
    1426881987,
    1925078388,
    2162078206,
    2614888103,
    3248222580,
    3835390401,
    4022224774,
    264347078,
    604807628,
    770255983,
    1249150122,
    1555081692,
    1996064986,
    2554220882,
    2821834349,
    2952996808,
    3210313671,
    3336571891,
    3584528711,
    113926993,
    338241895,
    666307205,
    773529912,
    1294757372,
    1396182291,
    1695183700,
    1986661051,
    2177026350,
    2456956037,
    2730485921,
    2820302411,
    3259730800,
    3345764771,
    3516065817,
    3600352804,
    4094571909,
    275423344,
    430227734,
    506948616,
    659060556,
    883997877,
    958139571,
    1322822218,
    1537002063,
    1747873779,
    1955562222,
    2024104815,
    2227730452,
    2361852424,
    2428436474,
    2756734187,
    3204031479,
    3329325298,
]


def urs(num, shift):
    if num >= 0:
        return i32(num >> shift).value
    else:
        # If num is negative, simulate zero-fill right shift
        return i32((num >> shift) + (2 ** (32 - shift))).value


from ctypes import c_int32 as i32


def hashFunction(data):
    chunk_ = data["chunk_"]
    w_ = data["w_"]
    hash_ = data["hash_"]

    d, e = 0, 0
    c = w_

    for b in chunk_:
        c[d] = (b[3] << 24) | (b[2] << 16) | (b[1] << 8) | b[0]
        d += 1

    for b in range(16, 64):
        e = c[b - 15] | 0
        d = c[b - 2] | 0
        f = (c[b - 16] | 0) + i32(
            (urs(e, 7) | (e << 25)) ^ (urs(e, 18) | (e << 14)) ^ urs(e, 3)
        ).value
        h = (
            c[b - 7]
            | 0
            + i32(
                (urs(d, 17) | (d << 15)) ^ (urs(d, 19) | (d << 13)) ^ urs(d, 10)
            ).value
            | 0
        )
        c[b] = f + h

    d = hash_[0] | 0
    e = hash_[1] | 0
    k = hash_[2] | 0
    l = hash_[3] | 0
    m = hash_[4] | 0
    n = hash_[5] | 0
    p = hash_[6] | 0
    f = hash_[7] | 0

    qs = []

    for b in range(64):
        q = i32(
            (
                (urs(d, 2) | (d << 30))
                ^ (urs(d, 13) | (d << 19))
                ^ (urs(d, 22) | (d << 10))
            )
            + ((d & e) ^ (d & k) ^ (e & k))
        ).value
        h = (m & n) ^ (~m & p)
        f = i32(
            f
            + (
                (urs(m, 6) | (m << 26))
                ^ (urs(m, 11) | (m << 21))
                ^ (urs(m, 25) | (m << 7))
            )
        ).value
        h = h + (MG[b] | 0)
        h = ((f + ((h + (c[b] | 0))) | 0)) | 0
        f = p
        p = n
        n = m
        m = (l + h) | 0
        l = k
        k = e
        e = d
        d = (h + q) | 0

    hash_[0] = (hash_[0] + d) | 0
    hash_[1] = (hash_[1] + e) | 0
    hash_[2] = (hash_[2] + k) | 0
    hash_[3] = (hash_[3] + l) | 0
    hash_[4] = (hash_[4] + m) | 0
    hash_[5] = (hash_[5] + n) | 0
    hash_[6] = (hash_[6] + p) | 0
    hash_[7] = (hash_[7] + f) | 0

    return hash_


# Example input
input_data = {
    "chunk_": [
        [
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
        ],
    ],
    "w_": [0] * 64,  # You can populate w_ as needed
    "hash_": [
        1779033703,
        3144134277,
        1013904242,
        2773480762,
        1359893119,
        2600822924,
        528734635,
        1541459225,
    ],
}

# Call the function
result = hashFunction(input_data)

# Print the result
print(result)
