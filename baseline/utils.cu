#include "stdio.h"
#include "stdint.h"
#include <cassert>
#include "helper.h"

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

    // Create events for GPU timing
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);

    int threadblocksize = std::min(1024, (int)num_kvs);
    int gridsize = (num_kvs + threadblocksize - 1) / threadblocksize;
    assert(gridsize * threadblocksize && "Number of threads are less");
    gpu_hashtable_insert<<<gridsize, threadblocksize>>>(pHashTable, device_kvs, num_kvs);
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        printf("Kernel launch failed: %s\n", cudaGetErrorString(err));
    }
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);
    float seconds = milliseconds / 1000.0f;
    printf("GPU inserted %d items in %f ms (%f million keys/second)\n", num_kvs, milliseconds, num_kvs / (double)seconds / 1000000.0f);

    cudaFree(device_kvs);
}

__global__ void gpu_hashtable_print(KeyValue* deviceArr, const KeyValue* kvs, uint32_t tsize) {
    unsigned int threadid = blockIdx.x*blockDim.x + threadIdx.x;
    if (threadid < tsize)
    {
        uint32_t key = kvs[threadid].key;
        uint32_t value = kvs[threadid].value;
        uint32_t slot = hash(key);
        while (true)
        {
            if (deviceArr[slot].key != kEmpty) {
                if (key != deviceArr[slot].key) {
                    printf("Mismatch found: KV key: %d Hash key: %d\n", key, deviceArr[slot].key); 
                    return;
                }
                else if (value != deviceArr[slot].value) {
                    printf("Mismatch found: KV value: %u Hash value: %u\n", value, deviceArr[slot].value); 
                    return;
                }
                else {
                    printf("Match found: key: %d value: %u\n", deviceArr[slot].key, deviceArr[slot].value);
                    return;
                }
            }
            slot = (slot + 1) & (maxCapacity-1);
        }
    }
}

void print_arr_gpu(KeyValue* deviceArr, const KeyValue* kvs, uint32_t tsize) {
     // Copy the keyvalues to the GPU
    KeyValue* device_kvs;
    cudaMalloc(&device_kvs, sizeof(KeyValue) * tsize);
    cudaMemcpy(device_kvs, kvs, sizeof(KeyValue) * tsize, cudaMemcpyHostToDevice);

    // Have CUDA calculate the thread block size
    int threadblocksize = std::min(1024, (int)tsize);
    int gridsize = (tsize + threadblocksize - 1) / threadblocksize;

    // Create events for GPU timing
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);
    gpu_hashtable_print<<<gridsize, threadblocksize>>>(deviceArr, device_kvs, tsize);
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        printf("Kernel launch failed: %s\n", cudaGetErrorString(err));
    }
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);
    float seconds = milliseconds / 1000.0f;
    printf("Printed GPU %d items in %f ms (%f million keys/second)\n", tsize, milliseconds, tsize / (double)seconds / 1000000.0f);

    cudaFree(device_kvs);
}

__global__ void gpu_lookup(Match* rgpu, int* rid, KeyValue* t1, KeyValue* t2dev_kvs, uint32_t s1, uint32_t s2) {
    unsigned int threadid = blockDim.x * blockIdx.x + threadIdx.x;
    if (threadid < s2)
    {
        uint32_t k = t2dev_kvs[threadid].key;
        uint32_t v = t2dev_kvs[threadid].value;
        uint32_t slot = hash(k);
        while (true) {
            if (t1[slot].key == k) {
                uint32_t pos =  atomicAdd(rid, 1);
                rgpu[pos].key = k;
                rgpu[pos].value1 = t1[slot].value;
                rgpu[pos].value2 = v;
                return;
            }
            else if (t1[slot].key == kEmpty) {
                return;
            }
            slot = (slot + 1) & (maxCapacity-1);
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

    int threadblocksize = std::min(1024, (int)s2);
    int gridsize = (maxCapacity + threadblocksize - 1) / threadblocksize;

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);

    gpu_lookup<<<gridsize, threadblocksize>>>(rgpu, rid, t1_hash, t2dev_kvs, s1, s2);
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        printf("Kernel launch failed: %s\n", cudaGetErrorString(err));
    }

    int rpos;
    cudaMemcpy(&rpos, rid, sizeof(int), cudaMemcpyDeviceToHost);
    cudaMemcpy(result, rgpu, sizeof(Match) * rpos, cudaMemcpyDeviceToHost);

    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);
    float seconds = milliseconds / 1000.0f;
    printf("Found %d matches in %f ms (%f million keys/second)\n", rpos, milliseconds, rpos / (double)seconds / 1000000.0f);
    
    return rpos;
}