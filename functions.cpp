#include <vector>
#include <math.h>
#include <string>
#include "Ant.cpp"

std::vector<std::vector<int>> getGainMatrix(std::vector<std::string> input){
    int S = input.size();
    int l = input[0].length();

    std::vector<std::vector<int>> gainMatrix(S, std::vector<int>(S, 0));

    for(int x = 0; x < S; x++){
        for(int y = 0; y < S; y++){
            if(input[x] == input[y]) continue;
            for(int i = 0; i < l; i++){
                if(input[x].substr(i,l-i) == input[y].substr(0,l-i)){
                    gainMatrix[x][y] = l - i;
                    break;
                }
            }
        }
    }

    // for(int x = 0; x<S; x++){
    //     printf("[");
    //     for(int y = 0; y<S-1; y++){
    //         printf("%d, ", gainMatrix[x][y]);
    //     }
    //     printf("%d]\n", gainMatrix[x][S-1]);
    // }

    return gainMatrix;
}

std::vector<std::vector<float>> getSightMatrix(std::vector<std::vector<int>> gainMatrix){
    int size = gainMatrix.size();
    std::vector<std::vector<float>> sightMatrix(size, std::vector<float>(size, 0));

    for(int i = 0; i < size; i++){
        for(int j = 0; j < size; j++){
            sightMatrix[i][j] = pow(gainMatrix[i][j], 2);
        }
    }

    return sightMatrix;
}

std::vector<std::vector<float>> initPheromones(unsigned int length){
    std::vector<std::vector<float>> pheromones(length, std::vector<float>(length, 1.0f));
    return pheromones;
}

void vaporization(std::vector<std::vector<float>> &pheromoneMatrix, float epsilon){
    for(int i = 0; i < pheromoneMatrix.size(); i++){
        for(int j = 0; j < pheromoneMatrix[i].size(); j++){
            pheromoneMatrix[i][j] *= (1-epsilon);
        }
    }
}

std::pair<std::vector<int>, int> antColonyOptimization(
    unsigned int initialNode,
    const std::vector<std::vector<float>>& sightMatrix,
    std::vector<std::vector<int>> gainMatrix,
    int wordLength,
    int orgLength,
    int iterations = 40,
    int nOfAnts = 40,
    float alpha = 1,
    float beta = 2,
    float epsilon = 0.5
){
    int gain = 0;
    std::vector<int> path;
    std::vector<std::vector<float>> pheromoneMatrix = initPheromones(sightMatrix.size());

    for(int i = 0; i < iterations; i++){
        printf("Iteration: %d\n", i);

        std::vector<Ant> ants;

        for(int x = 0; x < nOfAnts; x++){
            ants.emplace_back(initialNode, sightMatrix, wordLength, orgLength);
        }

        for(int antNo = 0; antNo < nOfAnts; antNo++){
            // printf("\tAnt number: %d\n", antNo);
            while(ants[antNo].chooseNextNode(gainMatrix, pheromoneMatrix, alpha, beta)){}
            if(ants[antNo].getGain() > gain || gain == 0){
                gain = ants[antNo].getGain();
                path = ants[antNo].getRoute();
            }
        }

        vaporization(pheromoneMatrix, epsilon);
        
        for(int antNo = 0; antNo < nOfAnts; antNo++){
            ants[antNo].updatePheromones(pheromoneMatrix);
        }

        ants.clear();
    }

    std::pair<std::vector<int>, int> output;

    output = std::make_pair(path, gain);
    output.first = path;
    output.second = gain;

    for(int i = 0; i<pheromoneMatrix.size(); i++){
        pheromoneMatrix[i].clear();
    }

    pheromoneMatrix.clear();

    return output;
}