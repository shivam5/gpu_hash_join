#include "random"
#include "stdio.h"
#include <cassert>
#include "helper.h"
#define DEBUG false
std::vector<KeyValue> create_table(std::mt19937& rnd, uint32_t numkvs)
{
    std::uniform_int_distribution<uint32_t> dis(0, maxCapacity - 1);
    std::vector<KeyValue> kvs;
    kvs.reserve(numkvs);

    for (uint32_t i = 0; i < numkvs; i++)
    {
        uint32_t val = dis(rnd);
        kvs.push_back(KeyValue{i, val});
    }
    return kvs;
}

int main() {
    std::random_device rd;
    uint32_t seed = rd();
    std::mt19937 rnd(seed);  // mersenne_twister_engine
    printf("Random number generator seed = %u\n", seed);

    // generate query table
    std::vector<KeyValue> t1_kvs = create_table(rnd, t1Size);
    KeyValue* t1_hash = create_hashtable();
    const uint32_t num_insert_batches = 16;
    uint32_t num_inserts_per_batch = (uint32_t)t1_kvs.size() / num_insert_batches;
    for (uint32_t i = 0; i < num_insert_batches; i++)
    {
        insert_hashtable(t1_hash, t1_kvs.data() + i * num_inserts_per_batch, num_inserts_per_batch);
    }
    // create key value pairs for table 2
    std::vector<KeyValue> t2_kvs = create_table(rnd, t2Size);
    if (DEBUG) {
        printf("Printing Table 1\n");
        printf("Printing KV pairs on CPU\n");
        for (int i = 0; i < t1Size; i++) {
            printf("%u %u\n", t1_kvs[i].key, t1_kvs[i].value);
        }
        printf("Printing KV pairs on GPU\n");
        print_arr_gpu(t1_hash, t1_kvs.data(), t1Size);
        printf("Printing table 2\n");
        for (int i = 0; i < t2Size; i++) {
            printf("%u %u\n", t2_kvs[i].key, t2_kvs[i].value);
        }
    }
    Match* result = (Match*)malloc(sizeof(Match) * std::min(t1Size, t2Size));
    int rpos = findMatches(result, t1_hash, t2_kvs.data(), t1Size, t2Size);
    assert(rpos == std::min(t1Size, t2Size) && "Number of matches are incorrect");
    return 0;
}