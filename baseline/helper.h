#pragma once

struct KeyValue
{
    uint32_t key;
    uint32_t value;
};

struct Match
{
    uint32_t key;
    uint32_t value1;
    uint32_t value2;
};

const uint32_t maxCapacity = 16384;
const uint32_t t1Size = 64;
const uint32_t t2Size = 128;

const uint32_t kEmpty = 0xffffffff;

KeyValue* create_hashtable();

void insert_hashtable(KeyValue* hashtable, const KeyValue* kvs, uint32_t num_kvs);

void transfer_data(KeyValue* hostArr, KeyValue* deviceArr, uint32_t tsize);

int findMatches(Match* result, KeyValue* t1_hash, const KeyValue* t2_kvs, uint32_t s1, uint32_t s2);