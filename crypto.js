const pIa = [
        128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ],
    nIa = [
        1116352408, 1899447441, 3049323471, 3921009573, 961987163, 1508970993,
        2453635748, 2870763221, 3624381080, 310598401, 607225278, 1426881987,
        1925078388, 2162078206, 2614888103, 3248222580, 3835390401, 4022224774,
        264347078, 604807628, 770255983, 1249150122, 1555081692, 1996064986,
        2554220882, 2821834349, 2952996808, 3210313671, 3336571891, 3584528711,
        113926993, 338241895, 666307205, 773529912, 1294757372, 1396182291,
        1695183700, 1986661051, 2177026350, 2456956037, 2730485921, 2820302411,
        3259730800, 3345764771, 3516065817, 3600352804, 4094571909, 275423344,
        430227734, 506948616, 659060556, 883997877, 958139571, 1322822218,
        1537002063, 1747873779, 1955562222, 2024104815, 2227730452, 2361852424,
        2428436474, 2756734187, 3204031479, 3329325298,
    ]
const MG = window.Int32Array ? new Int32Array(nIa) : nIa

class CustomFile {
    constructor(fileObj) {
        const perSessionIsolation = fileObj.perSessionIsolation || false,
            perUserIsolation = fileObj.perUserIsolation || false,
            userId = fileObj.userId || ''

        this.fileId = fileObj.fileId
        if (perSessionIsolation) {
            let suffix = window.sessionStorage.getItem('kernelSuffix')
            if (suffix) {
                suffix = Math.random().toString(36).slice(2)
                window.sessionStorage.setItem('kernelSuffix', suffix)
            }
            this.setSuffix(suffix)
        }
        if (perUserIsolation && userId) this.setUsername(userId)
    }

    setUsername(username) {
        this.username = username
    }

    setSuffix(suffix) {
        this.suffix = suffix
    }

    getFileId() {
        return this.fileId
    }

    getUsername() {
        return this.username
    }

    getSuffix() {
        return this.suffix
    }

    equals(_rzb) {
        return (
            _rzb.getFileId() === this.getFileId() &&
            _rzb.getSuffix() === this.getSuffix() &&
            _rzb.getUsername() === this.getUsername()
        )
    }
}

function file2array(file) {
    var props = ['fileId'],
        values = [file.getFileId()]
    if (file.getSuffix()) {
        props.push('kernelSuffix')
        values.push(file.getSuffix())
    }
    if (file.getUsername()) {
        props.push('username')
        values.push(file.getUsername())
    }
    return [props, values]
}

function isArray(object) {
    return (
        (object && Array.isArray(object)) ||
        ('object' == typeof object && 'number' == typeof object.length)
    )
}

class CustomHash {
    constructor(
        numHashBlocks = 8,
        initHashBlocks = [
            1779033703, 3144134277, 1013904242, 2773480762, 1359893119,
            2600822924, 528734635, 1541459225,
        ]
    ) {
        this.blockSize = 64
        this.chunk_ = window.Uint8Array
            ? new Uint8Array(this.blockSize)
            : Array(this.blockSize)
        this.total_ = this.inChunk_ = 0
        this.hash_ = []
        this.numHashBlocks_ = numHashBlocks
        this.initHashBlocks_ = initHashBlocks
        this.w_ = window.Int32Array ? new Int32Array(64) : Array(64)
        this.reset()
    }

    reset() {
        this.total_ = this.inChunk_ = 0
        this.hash_ = window.Int32Array
            ? new Int32Array(this.initHashBlocks_)
            : Fb(this.initHashBlocks_)
    }

    hashFunction() {
        var { chunk_, w_, hash_ } = this
        for (var b = chunk_, c = w_, d = 0, e = 0; e < b.length; )
            (c[d++] =
                (b[e] << 24) | (b[e + 1] << 16) | (b[e + 2] << 8) | b[e + 3]),
                (e = 4 * d)
        for (b = 16; 64 > b; b++) {
            e = c[b - 15] | 0
            d = c[b - 2] | 0
            var f =
                    ((c[b - 16] | 0) +
                        (((e >>> 7) | (e << 25)) ^
                            ((e >>> 18) | (e << 14)) ^
                            (e >>> 3))) |
                    0,
                h =
                    ((c[b - 7] | 0) +
                        (((d >>> 17) | (d << 15)) ^
                            ((d >>> 19) | (d << 13)) ^
                            (d >>> 10))) |
                    0
            c[b] = (f + h) | 0
        }
        d = hash_[0] | 0
        e = hash_[1] | 0
        var k = hash_[2] | 0,
            l = hash_[3] | 0,
            m = hash_[4] | 0,
            n = hash_[5] | 0,
            p = hash_[6] | 0
        f = hash_[7] | 0
        for (b = 0; 64 > b; b++) {
            var q =
                ((((d >>> 2) | (d << 30)) ^
                    ((d >>> 13) | (d << 19)) ^
                    ((d >>> 22) | (d << 10))) +
                    ((d & e) ^ (d & k) ^ (e & k))) |
                0
            h = (m & n) ^ (~m & p)
            f =
                (f +
                    (((m >>> 6) | (m << 26)) ^
                        ((m >>> 11) | (m << 21)) ^
                        ((m >>> 25) | (m << 7)))) |
                0
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
        }
        this.hash_[0] = (hash_[0] + d) | 0
        this.hash_[1] = (hash_[1] + e) | 0
        this.hash_[2] = (hash_[2] + k) | 0
        this.hash_[3] = (hash_[3] + l) | 0
        this.hash_[4] = (hash_[4] + m) | 0
        this.hash_[5] = (hash_[5] + n) | 0
        this.hash_[6] = (hash_[6] + p) | 0
        this.hash_[7] = (hash_[7] + f) | 0
        console.log(this.hash_)
    }

    update(bufferOrString, _length) {
        const length = _length || bufferOrString.length
        var inChunk = this.inChunk_
        if ('string' === typeof bufferOrString)
            for (var c = 0; c < length; ) {
                this.chunk_[inChunk++] = bufferOrString.charCodeAt(c++)
                if (inChunk == this.blockSize) {
                    this.hashFunction()
                    inChunk = 0
                }
            }
        else if (isArray(bufferOrString))
            for (var c = 0; c < length; ) {
                var e = bufferOrString[c++]
                if (
                    !(
                        'number' == typeof e &&
                        0 <= e &&
                        255 >= e &&
                        e == (e | 0)
                    )
                )
                    throw Error('message must be a byte array')
                this.chunk_[inChunk++] = e
                if (inChunk == this.blockSize) {
                    this.hashFunction()
                    inChunk = 0
                }
            }
        else throw Error('message must be string or array')
        this.inChunk_ = inChunk
        this.total_ += length
    }
    digest() {
        var a = [],
            b = 8 * this.total_
        56 > this.inChunk_
            ? this.update(pIa, 56 - this.inChunk_)
            : this.update(pIa, this.blockSize - (this.inChunk_ - 56))
        for (var c = 63; 56 <= c; c--) {
            this.chunk_[c] = Math.floor(b) & 255
            b /= 256
        }
        this.hashFunction()
        for (c = b = 0; c < this.numHashBlocks_; c++)
            for (var d = 24; 0 <= d; d -= 8) a[b++] = (this.hash_[c] >> d) & 255
        return a
    }
}

let hea = {
        0: [
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'I',
            'J',
            'K',
            'L',
            'M',
            'N',
            'O',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'U',
            'V',
            'W',
            'X',
            'Y',
            'Z',
            'a',
            'b',
            'c',
            'd',
            'e',
            'f',
            'g',
            'h',
            'i',
            'j',
            'k',
            'l',
            'm',
            'n',
            'o',
            'p',
            'q',
            'r',
            's',
            't',
            'u',
            'v',
            'w',
            'x',
            'y',
            'z',
            '0',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '+',
            '/',
            '=',
        ],
        1: [
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'I',
            'J',
            'K',
            'L',
            'M',
            'N',
            'O',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'U',
            'V',
            'W',
            'X',
            'Y',
            'Z',
            'a',
            'b',
            'c',
            'd',
            'e',
            'f',
            'g',
            'h',
            'i',
            'j',
            'k',
            'l',
            'm',
            'n',
            'o',
            'p',
            'q',
            'r',
            's',
            't',
            'u',
            'v',
            'w',
            'x',
            'y',
            'z',
            '0',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '+',
            '/',
        ],
        2: [
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'I',
            'J',
            'K',
            'L',
            'M',
            'N',
            'O',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'U',
            'V',
            'W',
            'X',
            'Y',
            'Z',
            'a',
            'b',
            'c',
            'd',
            'e',
            'f',
            'g',
            'h',
            'i',
            'j',
            'k',
            'l',
            'm',
            'n',
            'o',
            'p',
            'q',
            'r',
            's',
            't',
            'u',
            'v',
            'w',
            'x',
            'y',
            'z',
            '0',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '-',
            '_',
            '=',
        ],
        3: [
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'I',
            'J',
            'K',
            'L',
            'M',
            'N',
            'O',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'U',
            'V',
            'W',
            'X',
            'Y',
            'Z',
            'a',
            'b',
            'c',
            'd',
            'e',
            'f',
            'g',
            'h',
            'i',
            'j',
            'k',
            'l',
            'm',
            'n',
            'o',
            'p',
            'q',
            'r',
            's',
            't',
            'u',
            'v',
            'w',
            'x',
            'y',
            'z',
            '0',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '-',
            '_',
            '.',
        ],
        4: [
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'I',
            'J',
            'K',
            'L',
            'M',
            'N',
            'O',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'U',
            'V',
            'W',
            'X',
            'Y',
            'Z',
            'a',
            'b',
            'c',
            'd',
            'e',
            'f',
            'g',
            'h',
            'i',
            'j',
            'k',
            'l',
            'm',
            'n',
            'o',
            'p',
            'q',
            'r',
            's',
            't',
            'u',
            'v',
            'w',
            'x',
            'y',
            'z',
            '0',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '-',
            '_',
        ],
    },
    we = {
        0: 52,
        1: 53,
        2: 54,
        3: 55,
        4: 56,
        5: 57,
        6: 58,
        7: 59,
        8: 60,
        9: 61,
        A: 0,
        B: 1,
        C: 2,
        D: 3,
        E: 4,
        F: 5,
        G: 6,
        H: 7,
        I: 8,
        J: 9,
        K: 10,
        L: 11,
        M: 12,
        N: 13,
        O: 14,
        P: 15,
        Q: 16,
        R: 17,
        S: 18,
        T: 19,
        U: 20,
        V: 21,
        W: 22,
        X: 23,
        Y: 24,
        Z: 25,
        a: 26,
        b: 27,
        c: 28,
        d: 29,
        e: 30,
        f: 31,
        g: 32,
        h: 33,
        i: 34,
        j: 35,
        k: 36,
        l: 37,
        m: 38,
        n: 39,
        o: 40,
        p: 41,
        q: 42,
        r: 43,
        s: 44,
        t: 45,
        u: 46,
        v: 47,
        w: 48,
        x: 49,
        y: 50,
        z: 51,
        '+': 62,
        '/': 63,
        '=': 64,
        '-': 62,
        _: 63,
        '.': 64,
    }

function xe(buffer, length) {
    b = hea[length || 0]
    for (
        var c = Array(Math.floor(buffer.length / 3)),
            d = b[64] || '',
            e = 0,
            f = 0;
        e < buffer.length - 2;
        e += 3
    ) {
        var h = buffer[e],
            k = buffer[e + 1],
            l = buffer[e + 2],
            m = b[h >> 2]
        h = b[((h & 3) << 4) | (k >> 4)]
        k = b[((k & 15) << 2) | (l >> 6)]
        l = b[l & 63]
        c[f++] = '' + m + h + k + l
    }
    m = 0
    l = d
    switch (buffer.length - e) {
        case 2:
            ;(m = buffer[e + 1]), (l = b[(m & 15) << 2] || d)
        case 1:
            ;(buffer = buffer[e]),
                (c[f] =
                    '' +
                    b[buffer >> 2] +
                    b[((buffer & 3) << 4) | (m >> 4)] +
                    l +
                    d)
    }
    return c.join('')
}

const kDb = {
    StorageKey: {
        ACCESS_HISTORY: 'external_access_history',
        KERNEL: 'datalab_kernelAlloc',
        LOCAL_STORE: 'colab_localstore',
        PREFS: 'datalab_prefs',
    },
    getUsername: function () {
        return window.colabUserEmail || ''
    },
    init: function () {},
    reauthenticate: function () {},
}

function hashFile(file) {
    var customHash = new CustomHash(
        8,
        [
            1779033703, 3144134277, 1013904242, 2773480762, 1359893119,
            2600822924, 528734635, 1541459225,
        ]
    )
    customHash.update(JSON.stringify(file2array(file)))
    return xe(customHash.digest(), 3)
}

function notebook2customFile(notebook) {
    var perUserIsolation = false,
        userId = '',
        runtime = notebook.runtime
    if (runtime && 'gce_unmanaged' === runtime.kind) {
        perUserIsolation = true
        userId = kDb.getUsername() || ''
    }
    return new CustomFile({
        fileId: notebook.notebookId,
        perSessionIsolation:
            !!notebook.notebookModel.getTraits().params.sandboxMode,
        perUserIsolation: perUserIsolation,
        userId: userId,
    })
}

console.log(
    hashFile(
        notebook2customFile({
            userId: 'm.durand@straton-dcim.com',
            notebookId: '14mNurj5d0LDES8u4SI8NWOIKrZY1rZP3',
            notebookModel: {
                getTraits() {
                    return { params: { sandboxMode: false } }
                },
            },
        })
    )
)
