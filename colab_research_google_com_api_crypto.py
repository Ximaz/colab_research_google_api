import ctypes
import math
import json
import typing
import pathlib
import string

googcrypto = ctypes.CDLL("./libgoogcrypto.so")

def _hashFunction(chunk_: typing.List[int], w_: typing.List[int], hash_: typing.List[int]) -> typing.List[int]:
    hash_ = hash_.copy()
    chunk_arg_type = ctypes.c_ubyte * 64
    w_arg_type = ctypes.c_uint * 64
    hash_arg_type = ctypes.c_uint * 8

    googcrypto.hashFunction.argtypes = [chunk_arg_type, w_arg_type, hash_arg_type]

    chunk_ = chunk_arg_type(*chunk_)
    w_ = w_arg_type(*w_)
    hash_ = hash_arg_type(*hash_)
    googcrypto.hashFunction(chunk_, w_, hash_)
    return list(hash_)


PIA = [128] + [0] * 63
NIA = [
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
NUM_HASH_BLOCKS = 8
INIT_HASH_BLOCKS = [
    1779033703,
    3144134277,
    1013904242,
    2773480762,
    1359893119,
    2600822924,
    528734635,
    1541459225,
]
MINI_ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits
ALPHABETS = [
    MINI_ALPHABET + "+/=",
    MINI_ALPHABET + "+/",
    MINI_ALPHABET + "-_=",
    MINI_ALPHABET + "-_.",
    MINI_ALPHABET + "-_",
]

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
        self.hash_ = self.initHashBlocks_

    def hashFunction(self):
        chunk_, w_, hash_ = self.chunk_, self.w_, self.hash_
        hash_ = _hashFunction(chunk_=chunk_, w_=w_, hash_=hash_)
        self.hash_ = hash_

    def update(self, buffer: list | str, _length: int = None):
        l = _length or len(buffer)
        inChunk = self.inChunk_
        c = 0
        if isinstance(buffer, str):
            buffer = list(map(ord,buffer))
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
            self.update(PIA, 56 - self.inChunk_)
        else:
            self.update(PIA, self.blockSize - (self.inChunk_ - 56))
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
                if b == len(a):
                    a.append(0)
                a[b] = (self.hash_[c] >> d) & 255
                b += 1
                d -= 8
            c += 1
        return a

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
    b = ALPHABETS[length]
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
    delta = len(buffer) - e

    if (delta >= 2):
        m = buffer[e + 1]
        l = b[(m & 15) << 2] or d
    if (delta >= 1):
        buffer = buffer[e]
        if f == len(c):
            c.append('')
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


def get_assign_nbh_token(user_email: str, notebook_id: str):
    file = notebook2customFile(
            user_email,
            { "notebookId": notebook_id }
        )
    customHash = CustomHash(
        num_hash_blocks=NUM_HASH_BLOCKS, init_hash_blocks=INIT_HASH_BLOCKS
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
