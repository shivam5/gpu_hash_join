#include "random"
#include "stdio.h"
#include "helper.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstring>
#include <cassert>
#define DEBUG false
std::vector<KeyValue> read_table(std::string file_path, int key_id, int val_id, int& numPairs) {
    std::ifstream file(file_path);
    std::string line;

    if (!file) {
        std::cerr << "Error opening file." << std::endl;
        return {};
    }

    std::vector<KeyValue> kv_pairs;
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string token;
        KeyValue temp;
        int count = 0;
        while (std::getline(ss, token, '|')) {  // Parsing based on '|' delimiter
            if (count == key_id) {
                temp.key = std::stoi(token);
            }
            else if (count == val_id) {
                temp.value = strdup(token.c_str());
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

int main() {
    // generate query table
    std::string customer_file = "../data/customer.tbl";
    int cust_key = 0;
    int cust_val = 1;
    int nCustomer = 0;
    std::vector<KeyValue> customer = read_table(customer_file, cust_key, cust_val, nCustomer);
    std::cout << "Size of customer data: " << customer.size() << " num pairs: " << nCustomer << std::endl;
    int nLines = 0;
    std::string lineorder_file = "../data/lineorder.tbl";
    int line_id = 2;
    int line_val = 3;
    std::vector<KeyValue> lineorder = read_table(lineorder_file, line_id, line_val, nLines);
    std::cout << "Size of lineorder data: " << lineorder.size() << " num lines: " << nLines << std::endl;
    KeyValue* c_hash = create_hashtable();
    const uint32_t num_insert_batches = 128;
    uint32_t num_inserts_per_batch = (uint32_t)customer.size() / num_insert_batches;
    for (uint32_t i = 0; i < num_insert_batches; i++)
    {
        insert_hashtable(c_hash, customer.data() + i * num_inserts_per_batch, num_inserts_per_batch);
    }
    if (DEBUG) {
        printf("Printing Table 1\n");
        printf("Printing KV pairs on CPU\n");
        for (int i = 0; i < nCustomer; i++) {
            printf("%u %s\n", customer[i].key, customer[i].value);
        }
        printf("Printing KV pairs on GPU\n");
        // print_arr_gpu(c_hash, customer.data(), nCustomer);
        printf("Printing table 2\n");
        for (int i = 0; i < nLines; i++) {
            printf("%u %u\n", lineorder[i].key, lineorder[i].value);
        }
    }
    Match* result = (Match*)malloc(sizeof(Match) * nLines);
    int rpos = findMatches(result, c_hash, lineorder.data(), nLines);
    std::cout << "Num matches: " << rpos << std::endl;
    assert(rpos == nLines && "Number of matches are incorrect");
    return 0;
}