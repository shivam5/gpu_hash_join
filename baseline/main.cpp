#include "random"
#include "stdio.h"
#include "helper.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstring>
#include <cassert>
#define DEBUG false

int compareMatches(const void* a, const void* b) {
    const Match* matchA = (const Match*)a;
    const Match* matchB = (const Match*)b;

    if (matchA->key < matchB->key) return -1;
    if (matchA->key > matchB->key) return 1;

    if (matchA->value1 < matchB->value1) return -1;
    if (matchA->value1 > matchB->value1) return 1;

    // If keys are equal, compare by value2
    if (matchA->value2 < matchB->value2) return -1;
    if (matchA->value2 > matchB->value2) return 1;

    return 0;
}

std::vector<KeyValue> read_table(std::string file_path, int key_id, int val_id, int& numPairs) {
    std::ifstream file(file_path);
    std::string line;

    if (!file) {
        std::cerr << "Error opening file." << std::endl;
        return {};
    }

    std::vector<KeyValue> kv_pairs;
    int line_count = 0;
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        if (line_count == 0) {
            line_count += 1;
            continue;
        }
        std::string token;
        KeyValue temp;
        int count = 0;
        while (std::getline(ss, token, ',')) {  // Parsing based on '|' delimiter
            if (count == key_id) {
                temp.key = std::stoi(token);
            }
            else if (count == val_id) {
                temp.value = std::stoi(token);
            }
            count += 1;
        } 
        if (temp.key != 0xffffffff) {
            kv_pairs.push_back(temp);
        }
    }
    numPairs = kv_pairs.size();
    int rem = ceil(log2(numPairs));
    int newSize = 1 << rem;
    std::vector<KeyValue> kv_new(newSize);
    std::copy(kv_pairs.begin(), kv_pairs.end(), kv_new.begin());
    return kv_new;
}

void write_to_csv(const std::string& filename, Match* data, int rpos) {

    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Failed to open file: " << filename << std::endl;
        return;
    }
    // Optional: Write header
    file << "id,v2,v1\n";
    // Write each Match struct as a row in CSV format
    for (int i = 0; i < rpos; i++) {
        file << data[i].key << ',' << data[i].value1 << ',' << data[i].value2 << '\n';
    }
    file.close();
}

int main() {
    // generate query table
    std::string i1_file = "10k";
    std::string i2_file = "1k";
    std::string out_file = "../data/benchmark/pred_" + i1_file + "_" + i2_file + ".csv";
    std::string ref_file = "../data/benchmark/table" + i1_file + ".csv";
    int ref_key = 1;
    int ref_val = 2;
    int nRefs = 0;
    std::vector<KeyValue> ref = read_table(ref_file, ref_key, ref_val, nRefs);
    std::cout << "Size of ref data: " << ref.size() << " num pairs: " << nRefs << std::endl;
    int nQueries = 0;
    std::string q_file = "../data/benchmark/table1M_id" + i2_file + ".csv";
    int q_id = 1;
    int q_val = 2;
    std::vector<KeyValue> query = read_table(q_file, q_id, q_val, nQueries);
    std::cout << "Size of queries data: " << query.size() << " num queries: " << nQueries << std::endl;
    KeyValue* r_hash = create_hashtable();
    const uint32_t num_insert_batches = 64;
    uint32_t num_inserts_per_batch = (uint32_t)ref.size() / num_insert_batches;
    for (uint32_t i = 0; i < num_insert_batches; i++)
    {
        insert_hashtable(r_hash, ref.data() + i * num_inserts_per_batch, num_inserts_per_batch);
    }
    if (DEBUG) {
        printf("Printing Table 1\n");
        printf("Printing KV pairs on CPU\n");
        for (int i = 0; i < nRefs; i++) {
            printf("%u %s\n", ref[i].key, ref[i].value);
        }
        printf("Printing KV pairs on GPU\n");
        // print_arr_gpu(c_hash, customer.data(), nCustomer);
        printf("Printing table 2\n");
        for (int i = 0; i < nQueries; i++) {
            printf("%u %u\n", query[i].key, query[i].value);
        }
    }
    Match* result = (Match*)malloc(sizeof(Match) * nRefs * nQueries);
    int rpos = findMatches(result, r_hash, query.data(), nRefs, nQueries);
    std::cout << "Num matches: " << rpos << std::endl;
    qsort(result, rpos, sizeof(Match), compareMatches);
    write_to_csv(out_file, result, rpos);
    return 0;
}