#pragma once

struct KeyValue
{
    uint32_t key = 0xffffffff;
    const char* value = "";
};

struct Match
{
    uint32_t key;
    const char* value1;
    const char* value2;
};

const uint32_t maxCapacity = 1073741824;
const uint32_t t1Size = 1048576;
const uint32_t t2Size = 4194304;

const uint32_t kEmpty = 0xffffffff;

KeyValue* create_hashtable();

void insert_hashtable(KeyValue* hashtable, const KeyValue* kvs, uint32_t num_kvs);

// void print_arr_gpu(KeyValue* deviceArr, const KeyValue* kvs, uint32_t tsize);

int findMatches(Match* result, KeyValue* t1_hash, const KeyValue* t2_kvs, uint32_t s2);