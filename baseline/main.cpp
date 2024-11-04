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
        std::cerr << "Error opening file." << file_path << std::endl;
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

void print_usage(const char* program_name) {
    std::cerr << "Usage: " << program_name << " <i1_file> <i2_file>\n";
    std::cerr << "Example: " << program_name << " 10k 1k\n";
}

int main(int argc, char* argv[]) {
    // Check command line arguments
    if (argc != 3) {
        print_usage(argv[0]);
        return 1;
    }

    // Get input parameters from command line
    std::string i1_file = argv[1];  // Will be like "1M_id10"
    std::string i2_file = argv[2];  // Will be like "1k"
    
    // Define file paths using command line arguments
    std::string out_file = "data/pred_table" + i1_file + "_" + i2_file + ".csv";
    std::string ref_file = "data/table" + i2_file + ".csv";
    std::string q_file = "data/table" + i1_file + ".csv";

    std::cout << "Reading reference file: " << ref_file << std::endl;
    std::cout << "Reading query file: " << q_file << std::endl;
    std::cout << "Output will be written to: " << out_file << std::endl;
    
    int ref_key = 1;
    int ref_val = 2;
    int nRefs = 0;
    
    // Read reference table
    std::vector<KeyValue> ref = read_table(ref_file, ref_key, ref_val, nRefs);
    if (ref.empty()) {
        std::cerr << "Failed to read reference table" << std::endl;
        return 1;
    }
    std::cout << "Size of ref data: " << ref.size() << " num pairs: " << nRefs << std::endl;
    
    // Read query table
    int nQueries = 0;
    int q_id = 1;
    int q_val = 2;
    std::vector<KeyValue> query = read_table(q_file, q_id, q_val, nQueries);
    if (query.empty()) {
        std::cerr << "Failed to read query table" << std::endl;
        return 1;
    }
    std::cout << "Size of queries data: " << query.size() << " num queries: " << nQueries << std::endl;

    // Create and populate hash table
    KeyValue* r_hash = create_hashtable();
    const uint32_t num_insert_batches = 64;
    uint32_t num_inserts_per_batch = (uint32_t)ref.size() / num_insert_batches;
    for (uint32_t i = 0; i < num_insert_batches; i++) {
        insert_hashtable(r_hash, ref.data() + i * num_inserts_per_batch, num_inserts_per_batch);
    }

    if (DEBUG) {
        printf("Printing Table 1\n");
        printf("Printing KV pairs on CPU\n");
        for (int i = 0; i < nRefs; i++) {
            printf("%u %s\n", ref[i].key, ref[i].value);
        }
        printf("Printing KV pairs on GPU\n");
        printf("Printing table 2\n");
        for (int i = 0; i < nQueries; i++) {
            printf("%u %u\n", query[i].key, query[i].value);
        }
    }

    // Process matches
    Match* result = (Match*)malloc(sizeof(Match) * nRefs * nQueries);
    int rpos = findMatches(result, r_hash, query.data(), nRefs, nQueries);
    std::cout << "Num matches: " << rpos << std::endl;
    
    // Sort and write results
    qsort(result, rpos, sizeof(Match), compareMatches);
    write_to_csv(out_file, result, rpos);

    // Cleanup
    free(result);
    
    return 0;
}