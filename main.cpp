#include <cstdio>
#include <iostream>
#include <filesystem>
#include <fstream>
#include <algorithm>
#include <string>
#include <ctime>
#include "functions.cpp"

#define ITERATIONS 40
#define ANTS 40

int main(){
    int orgLength;

    srand((unsigned int)time(NULL));

    printf("Would you like to overwrite files that are already in output? (Y/N) \n");

    char ans;
    std::cin >> ans;

    std::vector<std::string> out(0);

    if(ans == 'N' || ans == 'n'){
        for(const auto &entry : std::filesystem::directory_iterator("outputs")){
            out.push_back(entry.path().string().erase(0,8));
        }
    }

    bool skip;
    std::fstream inputFile;
    std::fstream outputFile;
    std::string instanceName;
    std::string orgLengthStr;

    for(const auto &entry : std::filesystem::directory_iterator("inputs")){
        skip = false;
        orgLengthStr = "";

        instanceName = entry.path().string().erase(0,7);

        for(auto fileToSkip : out){
            if(instanceName == fileToSkip){
                skip = true;
                break;
            }
        }
        if(skip == true){
            continue;
        }

        inputFile.open(entry.path(), std::ios::in);

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
        int l = words[0].length();
        
        for (int i = 0; i < instanceName.length(); i++)
        {
            if(instanceName[i] == '.'){
                i++;
                for (int j = i; j < instanceName.length(); j++)
                {
                    if(instanceName[j]=='+' || instanceName[j]=='-')
                        break;
                    else
                        orgLengthStr += instanceName[j];
                }
                break;
            }
        }

        orgLength = atoi(orgLengthStr.c_str());
        orgLength += 9;

        auto start = time(nullptr);
        result = antColonyOptimization(sightMatrix.size()/2, sightMatrix, gainMatrix, l, orgLength, ITERATIONS, ANTS);
        auto duration = time(nullptr) - start;

        std::vector<int> path = result.first;
        int gain = result.second;

        std::string seq = "";

        for(int i = 0; i < path.size(); i++){
            if(path[i] == -1) break;
            if(i == 0){
                seq = words[path[i]];
            }
            else{
                for(int j = 0; j < l; j++){
                    auto a = words[path[i-1]].substr(j,l-j);
                    auto b = words[path[i]].substr(0,l-j);
                    if(a == b){
                        seq += words[path[i]].substr(l-j, j);
                        break;
                    }
                }
            }
        }

        printf("Number of ants: %d \n", ANTS);
        printf("Number of iterations: %d \n", ITERATIONS);
        printf("Path: [");
        int pathLength = 0;
        for(int i = 0; i < path.size(); i++){
            if(path[i] == -1) break;
            else{
                pathLength += 1;
                printf("%d", path[i]);
                if(i+1 < path.size() && path[i+1] != -1) printf(", ");
            }
        }
        printf("]\n");
        printf("Length: %d \n",pathLength);
        printf("Instance Length: %d \n",gainMatrix.size());
        printf("Gain: %d \n",gain);
        printf("seq: ");
        std::cout << seq << std::endl;
        printf("Sequence Length: %d \n",seq.length());
        printf("Time: %d seconds\n",duration);

        outputFile.open("outputs\\" + instanceName, std::ios::out);
        outputFile << "Number of ants: " << ANTS << "\n";
        outputFile << "Number of iterations: " << ANTS << "\n";
        outputFile << "Path: [";
        for(int i = 0; i < path.size(); i++){
            if(path[i] == -1) break;
            else{
                outputFile << path[i];
                if(i+1 < path.size() && path[i+1] != -1) outputFile << ", ";
            }
        }
        outputFile << "]\n";
        outputFile << "Length: " << pathLength << "\n";
        outputFile << "Instance Length: " << gainMatrix.size() << "\n";
        outputFile << "Gain: " << gain << "\n";
        outputFile << "seq: " << seq.c_str() << "\n";
        outputFile << "Sequence Length: " << seq.length() << "\n";
        outputFile << "Time: " << duration << " seconds\n";

        outputFile.close();
    }

    getchar();
    
    return 0;
}