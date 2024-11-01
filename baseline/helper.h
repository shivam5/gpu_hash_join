#pragma once

struct KeyValue
{
    uint32_t key = 0xffffffff;
    uint32_t value = 0xffffffff;
};

struct Match
{
    uint32_t key;
    uint32_t value1;
    uint32_t value2;
};

const uint32_t maxCapacity = 16777216;
const uint32_t t1Size = 1048576;
const uint32_t t2Size = 4194304;

const uint32_t kEmpty = 0xffffffff;

KeyValue* create_hashtable();

void insert_hashtable(KeyValue* hashtable, const KeyValue* kvs, uint32_t num_kvs);

int findMatches(Match* result, KeyValue* t1_hash, const KeyValue* t2_kvs, uint32_t s1, uint32_t s2);