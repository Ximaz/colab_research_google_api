#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>

#define NUM_HASH_BLOCKS 8

#if defined(_WIN32)
#   define DLL_EXPORT __declspec(dllexport)
#else
#   define DLL_EXPORT
#endif


static const unsigned int INIT_HASH_BLOCKS[NUM_HASH_BLOCKS] = {1779033703, 3144134277, 1013904242, 2773480762, 1359893119, 2600822924, 528734635, 1541459225};
static const unsigned int PIA[64] = {128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static const unsigned int NIA[64] = {1116352408, 1899447441, 3049323471, 3921009573, 961987163, 1508970993, 2453635748, 2870763221, 3624381080, 310598401, 607225278, 1426881987, 1925078388, 2162078206, 2614888103, 3248222580, 3835390401, 4022224774, 264347078, 604807628, 770255983, 1249150122, 1555081692, 1996064986, 2554220882, 2821834349, 2952996808, 3210313671, 3336571891, 3584528711, 113926993, 338241895, 666307205, 773529912, 1294757372, 1396182291, 1695183700, 1986661051, 2177026350, 2456956037, 2730485921, 2820302411, 3259730800, 3345764771, 3516065817, 3600352804, 4094571909, 275423344, 430227734, 506948616, 659060556, 883997877, 958139571, 1322822218, 1537002063, 1747873779, 1955562222, 2024104815, 2227730452, 2361852424, 2428436474, 2756734187, 3204031479, 3329325298};
static const char *ALPHABETS[5] = {"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/-", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_=", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"};

typedef struct s_hasher
{
    int block_size;
    int total;
    int in_chunk;
    int num_hash_blocks;
    unsigned char chunk[64];
    unsigned int hash[NUM_HASH_BLOCKS];
    unsigned int init_hash_blocks[NUM_HASH_BLOCKS];
    unsigned int w[64];
} hasher_t;

hasher_t *init_hasher(void);
void destroy_hasher(hasher_t *self);
void hash_hasher(hasher_t *self);
void update_hasher(hasher_t *self, unsigned char const *buffer, ssize_t length);
unsigned char *digest_hasher(hasher_t *self);

unsigned char *xe(unsigned char const *buffer, unsigned int n);

DLL_EXPORT unsigned char *hash_json_file_object(unsigned char const *json_data);
DLL_EXPORT void free_hash(unsigned char *hash);
