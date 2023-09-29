#include "googcrypto.h"

DLL_EXPORT unsigned char *hash_json_file_object(unsigned char const *json_data)
{
    unsigned char *buffer = 0;
    unsigned char *hash = 0;
    hasher_t *hasher = init_hasher();

    if (NULL == hasher)
        return NULL;
    update_hasher(hasher, json_data, -1);
    buffer = digest_hasher(hasher);
    if (NULL == buffer) {
        destroy_hasher(hasher);
        return NULL;
    }
    hash = xe(buffer, 3);
    free(buffer);
    if (NULL == hash) {
        destroy_hasher(hasher);
        return NULL;
    }
    destroy_hasher(hasher);
    return hash;
}

DLL_EXPORT void free_hash(unsigned char *hash)
{
    if (NULL != hash)
        free(hash);
}
