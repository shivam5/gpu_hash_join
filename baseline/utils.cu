#include "stdio.h"
#include "stdint.h"
#include "helper.h"
#include "vector"

// 32 bit Murmur3 hash
__device__ uint32_t hash(uint32_t k)
{
    k ^= k >> 16;
    k *= 0x85ebca6b;
    k ^= k >> 13;
    k *= 0xc2b2ae35;
    k ^= k >> 16;
    return k & (maxCapacity-1);
}

// Create a hash table. For linear probing, this is just an array of KeyValues
KeyValue* create_hashtable() 
{
    // Allocate memory
    KeyValue* hashtable;
    cudaMalloc(&hashtable, sizeof(KeyValue) * maxCapacity);

    // Initialize hash table to empty
    static_assert(kEmpty == 0xffffffff, "memset expected kEmpty=0xffffffff");
    cudaMemset(hashtable, 0xff, sizeof(KeyValue) * maxCapacity);

    return hashtable;
}

// Insert the key/values in kvs into the hashtable
__global__ void gpu_hashtable_insert(KeyValue* hashtable, const KeyValue* kvs, unsigned int numkvs)
{
    unsigned int threadid = blockIdx.x*blockDim.x + threadIdx.x;
    if (threadid < numkvs)
    {
        uint32_t key = kvs[threadid].key;
        uint32_t value = kvs[threadid].value;
        uint32_t slot = hash(key);
        printf("Inserting pos: %u key: %d val: %d\n", slot, key, value);
        while (true)
        {
            uint32_t prev = atomicCAS(&hashtable[slot].key, kEmpty, key);
            if (prev == kEmpty || prev == key)
            {
                hashtable[slot].value = value;
                return;
            }

            slot = (slot + 1) & (maxCapacity-1);
        }
    }
}
 
void insert_hashtable(KeyValue* pHashTable, const KeyValue* kvs, uint32_t num_kvs)
{
    // Copy the keyvalues to the GPU
    KeyValue* device_kvs;
    cudaMalloc(&device_kvs, sizeof(KeyValue) * num_kvs);
    cudaMemcpy(device_kvs, kvs, sizeof(KeyValue) * num_kvs, cudaMemcpyHostToDevice);

    // Have CUDA calculate the thread block size
    int mingridsize;
    int threadblocksize;
    cudaOccupancyMaxPotentialBlockSize(&mingridsize, &threadblocksize, gpu_hashtable_insert, 0, 0);

    // Create events for GPU timing
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    cudaEventRecord(start);

    // Insert all the keys into the hash table
    int gridsize = ((uint32_t)num_kvs + threadblocksize - 1) / threadblocksize;
    gpu_hashtable_insert<<<gridsize, threadblocksize>>>(pHashTable, device_kvs, (uint32_t)num_kvs);

    cudaEventRecord(stop);

    cudaEventSynchronize(stop);

    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);
    float seconds = milliseconds / 1000.0f;
    // printf("GPU inserted %d items in %f ms (%f million keys/second)\n", num_kvs, milliseconds, num_kvs / (double)seconds / 1000000.0f);

    cudaFree(device_kvs);
}

void transfer_data(KeyValue* hostArr, KeyValue* deviceArr, uint32_t tsize) {
    cudaMemcpy(hostArr, deviceArr, sizeof(KeyValue) * tsize, cudaMemcpyDeviceToHost);
}

__global__ void gpu_lookup(Match* rgpu, int* rid, KeyValue* t1, KeyValue* t2dev_kvs, uint32_t s1, uint32_t s2) {
    unsigned int threadid = blockDim.x * blockIdx.x + threadIdx.x;
    if (threadid < s2)
    {
        uint32_t k = t2dev_kvs[threadid].key;
        uint32_t v = t2dev_kvs[threadid].value;
        uint32_t hval = hash(k);
        if (t1[hval].key == k) {
            uint32_t pos =  atomicAdd(rid, 1);
            rgpu[pos].key = k;
            rgpu[pos].value1 = t1[hval].value;
            rgpu[pos].value2 = v;
        }
    }
}

int findMatches(Match* result, KeyValue* t1_hash, const KeyValue* t2_kvs, uint32_t s1, uint32_t s2) {
    Match* rgpu;
    cudaMalloc(&rgpu, sizeof(Match) * s2);
    int* rid;
    cudaMalloc(&rid, sizeof(int));
    cudaMemset(rid, 0, sizeof(int));

    KeyValue* t2dev_kvs;
    cudaMalloc(&t2dev_kvs, sizeof(KeyValue) * s2);
    cudaMemcpy(t2dev_kvs, t2_kvs, sizeof(KeyValue) * s2, cudaMemcpyHostToDevice);

    int mingridsize;
    int threadblocksize;
    cudaOccupancyMaxPotentialBlockSize(&mingridsize, &threadblocksize, gpu_lookup, 0, 0);
    
    int gridsize = (maxCapacity + threadblocksize - 1) / threadblocksize;
    gpu_lookup<<<gridsize, threadblocksize>>>(rgpu, rid, t1_hash, t2dev_kvs, s1, s2);
    cudaDeviceSynchronize();

    int rpos;
    cudaMemcpy(&rpos, rid, sizeof(int), cudaMemcpyDeviceToHost);
    cudaMemcpy(result, rgpu, sizeof(Match) * rpos, cudaMemcpyDeviceToHost);
    return rpos;
}