import ctypes
import math
import json
import typing

Int32Array = typing.List[ctypes.c_int32]


def int32array(numbers: list) -> Int32Array:
    return [ctypes.c_int32(x) for x in numbers]


def print_int32array(array: Int32Array):
    print(json.dumps([x.value for x in array]))


pIa = [
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
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]
MG = nIa = [
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
num_hash_blocks = 8
init_hash_blocks = [
    1779033703,
    3144134277,
    1013904242,
    2773480762,
    1359893119,
    2600822924,
    528734635,
    1541459225,
]
hea = {
    "0": [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "+",
        "/",
        "=",
    ],
    "1": [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "+",
        "/",
    ],
    "2": [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "-",
        "_",
        "=",
    ],
    "3": [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "-",
        "_",
        ".",
    ],
    "4": [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "-",
        "_",
    ],
}
we = {
    "0": 52,
    "1": 53,
    "2": 54,
    "3": 55,
    "4": 56,
    "5": 57,
    "6": 58,
    "7": 59,
    "8": 60,
    "9": 61,
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
    "K": 10,
    "L": 11,
    "M": 12,
    "N": 13,
    "O": 14,
    "P": 15,
    "Q": 16,
    "R": 17,
    "S": 18,
    "T": 19,
    "U": 20,
    "V": 21,
    "W": 22,
    "X": 23,
    "Y": 24,
    "Z": 25,
    "a": 26,
    "b": 27,
    "c": 28,
    "d": 29,
    "e": 30,
    "f": 31,
    "g": 32,
    "h": 33,
    "i": 34,
    "j": 35,
    "k": 36,
    "l": 37,
    "m": 38,
    "n": 39,
    "o": 40,
    "p": 41,
    "q": 42,
    "r": 43,
    "s": 44,
    "t": 45,
    "u": 46,
    "v": 47,
    "w": 48,
    "x": 49,
    "y": 50,
    "z": 51,
    "+": 62,
    "/": 63,
    "=": 64,
    "-": 62,
    "_": 63,
    ".": 64,
}
kDb = {
    "StorageKey": {
        "ACCESS_HISTORY": "external_access_history",
        "KERNEL": "datalab_kernelAlloc",
        "LOCAL_STORE": "colab_localstore",
        "PREFS": "datalab_prefs",
    },
    "getUsername": lambda: "u.email@gmail.com" or "",
    "init": lambda: None,
    "reauthenticate": lambda: None,
}


def unsigned_right_shift(num, shift):
    if num >= 0:
        return num >> shift
    else:
        # If num is negative, simulate zero-fill right shift
        return (num >> shift) + (2 ** (32 - shift))


class CustomHash:
    def __init__(self, num_hash_blocks: int, init_hash_blocks: list):
        self.blockSize = 64
        self.chunk_ = [0] * self.blockSize
        self.total_ = self.inChunk_ = 0
        self.hash_ = []
        self.numHashBlocks_ = num_hash_blocks
        self.initHashBlocks_ = init_hash_blocks
        self.w_ = [0] * 64
        self.reset()

    def reset(self):
        self.total_ = self.inChunk_ = 0
        self.hash_ = int32array(self.initHashBlocks_)

    def hashFunction(self):
        chunk_, w_, hash_ = self.chunk_, self.w_, self.hash_
        b = chunk_
        c = w_
        d = 0
        e = 0
        while e < len(b):
            c[d] = (b[e] << 24) | (b[e + 1] << 16) | (b[e + 2] << 8) | b[e + 3]
            d += 1
            e = 4 * d
        b = 16
        while 64 > b:
            e = c[b - 15] | 0
            d = c[b - 2] | 0
            f = (
                (c[b - 16] | 0)
                + (
                    (unsigned_right_shift(e, 7) | (e << 25))
                    ^ (unsigned_right_shift(e, 18) | (e << 14))
                    ^ unsigned_right_shift(e, 3)
                )
            ) | 0
            h = (
                (c[b - 7] | 0)
                + (
                    (unsigned_right_shift(d, 17) | (d << 15))
                    ^ (unsigned_right_shift(d, 19) | (d << 13))
                    ^ unsigned_right_shift(d, 10)
                )
            ) | 0
            c[b] = (f + h) | 0
            b += 1
        d = hash_[0].value | 0
        e = hash_[1].value | 0
        k = hash_[2].value | 0
        l = hash_[3].value | 0
        m = hash_[4].value | 0
        n = hash_[5].value | 0
        p = hash_[6].value | 0
        f = hash_[7].value | 0
        b = 0
        qs = []
        while 64 > b:
            q = (
                ctypes.c_int32(
                    (
                        (unsigned_right_shift(d, 2) | (d << 30))
                        ^ (unsigned_right_shift(d, 13) | (d << 19))
                        ^ (unsigned_right_shift(d, 22) | (d << 10))
                    )
                    + ((d & e) ^ (d & k) ^ (e & k))
                ).value
                | 0
            )
            qs.append(q)
            h = (m & n) ^ (~m & p)
            f = (
                ctypes.c_int32(
                    f
                    + ctypes.c_int32(
                        (unsigned_right_shift(m, 6) | (m << 26))
                        ^ (unsigned_right_shift(m, 11) | (m << 21))
                        ^ (unsigned_right_shift(m, 25) | (m << 7))
                    ).value
                ).value
                | 0
            )
            h = (h + (MG[b] | 0)) | 0
            h = (f + ((h + (c[b] | 0)) | 0)) | 0
            f = p
            p = n
            n = m
            m = (l + h) | 0
            l = k
            k = e
            e = d
            d = (h + q) | 0
            b += 1
        print(qs)
        self.hash_[0].value = (hash_[0].value + d) | 0
        self.hash_[1].value = (hash_[1].value + e) | 0
        self.hash_[2].value = (hash_[2].value + k) | 0
        self.hash_[3].value = (hash_[3].value + l) | 0
        self.hash_[4].value = (hash_[4].value + m) | 0
        self.hash_[5].value = (hash_[5].value + n) | 0
        self.hash_[6].value = (hash_[6].value + p) | 0
        self.hash_[7].value = (hash_[7].value + f) | 0
        print_int32array(self.hash_)

    def update(self, buffer: list | str, _length: int = None):
        l = _length or len(buffer)
        inChunk = self.inChunk_
        c = 0
        if isinstance(buffer, str):
            buffer = str2bytes(buffer)
        while c < l:
            char = buffer[c]
            c += 1
            if not (
                isinstance(char, int)
                and char >= 0
                and char <= 255
                and char == (char | 0)
            ):
                raise Exception("Message must be a byte array")
            self.chunk_[inChunk] = char
            inChunk += 1
            if inChunk == self.blockSize:
                inChunk = 0
                self.hashFunction()
        self.inChunk_ = inChunk
        self.total_ += l

    def digest(self):
        a = []
        b = 8 * self.total_
        if 56 > self.inChunk_:
            self.update(pIa, 56 - self.inChunk_)
        else:
            self.update(pIa, self.blockSize - (self.inChunk_ - 56))
        c = 63
        while 56 <= c:
            self.chunk_[c] = math.floor(b) & 255
            b /= 256
            c -= 1
        self.hashFunction()
        c = b = 0
        while c < self.numHashBlocks_:
            d = 24
            while 0 <= d:
                a[b] = (self.hash_[c].value >> d) & 255
                b += 1
                d -= 8
            c += 1
        return a


def str2bytes(s: str) -> list:
    return [ord(c) for c in s]


class CustomFile:
    def __init__(self, fileObj: dict):
        # Supposed to be False
        perSessionIsolation = fileObj.get("perSessionIsolation", False)
        perUserIsolation = fileObj.get("perUserIsolation", False)
        userId = fileObj.get("userId", "")

        self.fileId = fileObj.get("fileId", "")
        self.suffix = ""
        self.username = ""
        if perUserIsolation and userId:
            self.setUsername(userId)

    def setUsername(self, username):
        self.username = username

    def setSuffix(self, suffix):
        self.suffix = suffix

    def getFileId(self):
        return self.fileId

    def getUsername(self):
        return self.username

    def getSuffix(self):
        return self.suffix

    def equals(self, customFile):
        return (
            customFile.getFileId() == self.getFileId()
            and customFile.getSuffix() == self.getSuffix()
            and customFile.getUsername() == self.getUsername()
        )


def xe(buffer: list, length: int = 0):
    b = hea[length]
    c = [0] * math.floor(len(buffer) / 3)
    d = b[64] or ""
    e = 0
    f = 0
    while e < len(buffer) - 2:
        h = buffer[e]
        k = buffer[e + 1]
        l = buffer[e + 2]
        m = b[h >> 2]
        h = b[((h & 3) << 4) | (k >> 4)]
        k = b[((k & 15) << 2) | (l >> 6)]
        l = b[l & 63]
        c[f] = "" + m + h + k + l
        f += 1
        e += 3
    m = 0
    l = d
    match (len(buffer) - e):
        case 2:
            m = buffer[e + 1]
            l = b[(m & 15) << 2] or d
        case 1:
            buffer = buffer[e]
            c[f] = "" + b[buffer >> 2] + b[((buffer & 3) << 4) | (m >> 4)] + l + d
    return "".join(c)


def file2array(file):
    props = ["fileId"]
    values = [file.getFileId()]
    if file.getSuffix():
        props.push("kernelSuffix")
        values.push(file.getSuffix())
    if file.getUsername():
        props.push("username")
        values.push(file.getUsername())
    return [props, values]


def hashFile(file):
    customHash = CustomHash(
        num_hash_blocks=num_hash_blocks, init_hash_blocks=init_hash_blocks
    )
    customHash.update(json.dumps(file2array(file), separators=(",", " ")))
    return xe(customHash.digest(), 3)


def notebook2customFile(colab_user_email: str, notebook: dict):
    perUserIsolation = False
    userId = ""
    runtime = notebook.get("runtime", None)

    # XXX: MUST NOT HAPPEN
    if runtime is not None and "gce_unmanaged" == runtime.get("kind", ""):
        perUserIsolation = True
        userId = colab_user_email

    return CustomFile(
        {
            "fileId": notebook.get("notebookId", ""),
            "perSessionIsolation": False,  # is sandbox
            "perUserIsolation": perUserIsolation,
            "userId": userId,
        }
    )


print(
    hashFile(
        notebook2customFile(
            "m.durand@straton-dcim.com",
            {"notebookId": "14mNurj5d0LDES8u4SI8NWOIKrZY1rZP3"},
        )
    )
)
