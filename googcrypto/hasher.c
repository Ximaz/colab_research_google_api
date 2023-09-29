#include "googcrypto.h"


hasher_t *init_hasher(void)
{
    int i = 0;
    hasher_t *self = (hasher_t *)malloc(sizeof(hasher_t));

    if (NULL == self)
        return NULL;
    self->block_size = 64;
    self->total = 0;
    self->in_chunk = 0;
    self->num_hash_blocks = NUM_HASH_BLOCKS;
    for (; self->num_hash_blocks > i; ++i)
        self->hash[i] = INIT_HASH_BLOCKS[i];
    return self;
}

void destroy_hasher(hasher_t *self)
{
    if (NULL != self)
        free(self);
}

void hash_hasher(hasher_t *self)
{
    unsigned int d = 0,
                 e = 0,
                 f = 0,
                 h = 0,
                 k = 0,
                 l = 0,
                 m = 0,
                 n = 0,
                 p = 0,
                 q = 0;
    unsigned char *b = self->chunk;
    unsigned int *c = self->w;

    for (; 64 >= e; e = 4 * d)
        c[d++] = (b[e] << 24) | (b[e + 1] << 16) | (b[e + 2] << 8) | b[e + 3];
    for (int b = 16; 64 > b; ++b) {
        e = c[b - 15] | 0;
        d = c[b - 2] | 0;
        f = ((c[b - 16] | 0) + (((e >> 7) | (e << 25)) ^ ((e >> 18) | (e << 14)) ^ (e >> 3))) | 0;
        h = ((c[b - 7] | 0) + (((d >> 17) | (d << 15)) ^ ((d >> 19) | (d << 13)) ^ (d >> 10))) | 0;
        c[b] = (f + h) | 0;
    }
    d = self->hash[0] | 0;
    e = self->hash[1] | 0;
    k = self->hash[2] | 0;
    l = self->hash[3] | 0;
    m = self->hash[4] | 0;
    n = self->hash[5] | 0;
    p = self->hash[6] | 0;
    f = self->hash[7] | 0;
    for (int b = 0; 64 > b; ++b) {
        q = ((((d >> 2) | (d << 30)) ^ ((d >> 13) | (d << 19)) ^ ((d >> 22) | (d << 10))) + ((d & e) ^ (d & k) ^ (e & k))) | 0;
        h = (m & n) ^ (~m & p);
        f = (f + (((m >> 6) | (m << 26)) ^ ((m >> 11) | (m << 21)) ^ ((m >> 25) | (m << 7)))) | 0;
        h = (h + (NIA[b] | 0)) | 0;
        h = (f + ((h + (c[b] | 0)) | 0)) | 0;
        f = p;
        p = n;
        n = m;
        m = (l + h) | 0;
        l = k;
        k = e;
        e = d;
        d = (h + q) | 0;
    }
    self->hash[0] = (self->hash[0] + d) | 0;
    self->hash[1] = (self->hash[1] + e) | 0;
    self->hash[2] = (self->hash[2] + k) | 0;
    self->hash[3] = (self->hash[3] + l) | 0;
    self->hash[4] = (self->hash[4] + m) | 0;
    self->hash[5] = (self->hash[5] + n) | 0;
    self->hash[6] = (self->hash[6] + p) | 0;
    self->hash[7] = (self->hash[7] + f) | 0;
}

void update_hasher(hasher_t *self, unsigned char const *buffer, ssize_t length)
{
    ssize_t l = 0;
    int in_chunk = 0;
    int i = 0;
    char c = 0;

    if (NULL == self || NULL == buffer)
        return;
    l = length < 0 ? (ssize_t)strlen((char const *)buffer) : length;
    if (0 == l)
        return;
    in_chunk = self->in_chunk;
    for (; i < l; ++i) {
        c = buffer[i];
        self->chunk[in_chunk++] = c;
        if (in_chunk == self->block_size) {
            in_chunk = 0;
            hash_hasher(self);
        }
    }
    self->in_chunk = in_chunk;
    self->total += l;
}

unsigned char *digest_hasher(hasher_t *self)
{
    unsigned char *a = 0;
    int b = 0;
    int c = 0;
    int d = 0;

    if (NULL == self)
        return NULL;
    a = (unsigned char *)calloc(1024, sizeof(unsigned char));
    if (NULL == a)
        return NULL;
    b = NUM_HASH_BLOCKS * self->total;
    if (56 > self->in_chunk)
        update_hasher(self, (unsigned char const *)PIA, (size_t)(56 - self->in_chunk));
    else
        update_hasher(self, (unsigned char const *)PIA, (size_t)(self->block_size - (self->in_chunk - 56)));
    c = 63;
    while (56 <= c) {
        self->chunk[c--] = b & 0xFF;
        b /= 0x100;
    }
    hash_hasher(self);
    c = 0;
    b = 0;
    while (self->num_hash_blocks > c) {
        d = 24;
        while (0 <= d) {
            a[b++] = (self->hash[c] >> d) & 0xFF;
            d -= 8;
        }
        c++;
    }
    return a;
}


unsigned char *xe(unsigned char const *buffer, unsigned int n)
{
    char const *alphabet = ALPHABETS[n];
    size_t alphabet_len = strlen(alphabet);
    unsigned char *output = 0;
    unsigned char **chunks = 0;
    unsigned char chunk[5] = {0};
    unsigned char d = alphabet[64],
                  h = 0,
                  k = 0,
                  l = 0,
                  m = 0;
    int e = 0,
        f = 0,
        i = 0;
    size_t chunks_len = 0,
           output_len = 0,
           tmp = 0;
    ssize_t buff_len = 0,
            delta = 0;

    if (NULL == buffer)
        return NULL;
    buff_len = strlen((char const *)buffer);
    chunks_len = buff_len / 3;
    chunks = (unsigned char **)malloc(sizeof(unsigned char *) * (chunks_len + 1));
    if (NULL == chunks)
        return NULL;
    chunks[chunks_len] = 0;
    for (; (buff_len - 2) > e; e += 3) {
        h = buffer[e];
        k = buffer[e + 1];
        l = buffer[e + 2];
        m = alphabet[h >> 2];
        h = alphabet[((h & 3) << 4) | (k >> 4)];
        k = alphabet[((k & 15) << 2) | (l >> 6)];
        l = alphabet[l & 63];
        chunk[0] = m;
        chunk[1] = h;
        chunk[2] = k;
        chunk[3] = l;
        chunks[f] = (unsigned char *)calloc(4, sizeof(unsigned char));
        if (NULL != chunks[f])
            memcpy(chunks[f], chunk, 4);
        f++;
        output_len += 4;
    }
    m = 0;
    l = d;
    delta = buff_len - e;
    if (2 <= delta) {
        m = buffer[e + 1];
        tmp = (m & 15) << 2;
        l = tmp < alphabet_len ? alphabet[tmp] : d;
    }
    if (1 <= delta) {
        chunk[0] = alphabet[buffer[e] >> 2];
        chunk[1] = alphabet[((buffer[e] & 3) << 4) | (m >> 4)];
        chunk[2] = l;
        chunk[3] = d;
        chunks[f] = (unsigned char *)calloc(5, sizeof(unsigned char));
        if (chunks[f])
            memcpy(chunks[f], chunk, 4);
        output_len += 4;
        f++;
    }
    output = (unsigned char *)calloc((output_len + 1), sizeof(unsigned char));
    if (NULL == output)
        return NULL;
    for (; i < f; ++i) {
        memcpy(&output[i * 4], chunks[i], 4);
        free(chunks[i]);
    }
    free(chunks);
    return output;
}
