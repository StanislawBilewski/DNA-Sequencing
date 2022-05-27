#include <cstdio>
#include <iostream>
#include <filesystem>
#include <fstream>
#include <algorithm>
#include <string>
#include <chrono>
#include "functions.cpp"

#define ITERATIONS 40
#define ANTS 40

int main(){

    // printf("Would you like to overwrite files that are already in output? (Y/N) \n");

    // char ans;
    // std::cin >> ans;

    std::fstream inputFile;
    inputFile.open("inputs/9.200-80.txt", std::ios::in);

    std::string data;
    std::vector<std::string> words;
    int i = 0;

    while(getline(inputFile, data)){
        words.push_back(data);

        i++;
    }
    inputFile.close();

    std::vector<std::vector<int>> gainMatrix = getGainMatrix(words);
    std::vector<std::vector<float>> sightMatrix = getSightMatrix(gainMatrix);
    std::pair<std::vector<int>, int> result;

    auto start = std::chrono::high_resolution_clock::now();
    result = antColonyOptimization(0, sightMatrix, gainMatrix, ITERATIONS, ANTS);
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::high_resolution_clock::now() - start);

    std::vector<int> path = result.first;
    int gain = result.second;

    std::string seq = "";
    int l = words[0].length();

    for(int i = 0; i < path.size(); i++){
        if(i == 0){
            seq = words[path[i]];
        }
        else{
            for(int j = 0; j < l; j++){
                if(words[i-1].substr(i,l-i) == words[i].substr(0,l-i)){
                    seq += words[path[i]].substr(l-j, l-i);
                }
            }
        }
    }

    printf("Number of ants: %d \n", ANTS);
    printf("Number of iterations: %d \n", ITERATIONS);
    printf("Path: [");
    for(int i = 0; i < path.size()-1; i++){
        printf("%d, ", path[i]);
    }
    printf("%d]\n", path[path.size()-1]);
    printf("Length: %d \n",path.size());
    printf("Instance Length: %d \n",gainMatrix.size());
    printf("Gain: %d \n",gain);
    printf("seq: %s \n", seq);
    printf("Sequence Length: %d \n",seq.length());
    printf("Time: %d \n",duration);
    
    return 0;
}