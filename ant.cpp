#include "ant.hpp"

Ant::Ant(int initialNode, std::vector<std::vector<float>> sightMatrix){
    this->totalGain = 0;
    this->initialNode = initialNode;
    this->currentNode = initialNode;
    this->sightMatrix = sightMatrix;
    this->route.resize(sightMatrix.size(), -1);
    this->route1.resize(sightMatrix.size(), -1);
    this->route2.resize(sightMatrix.size(), -1);

    this->route1[0] = initialNode;
}

bool Ant::visited(int node){
    for(int i = 0; i < this->route1.size(); i++){
        if(this->route1[i] == node) return true;
        if(this->route1[i] == -1) break;
    }
    for(int i = 0; i < this->route2.size(); i++){
        if(this->route2[i] == node) return true;
        if(this->route2[i] == -1) break;
    }
    return false;
}

bool Ant::chooseNextNode(std::vector<std::vector<int>> &gainMatrix, std::vector<std::vector<float>> &pheromones, float alpha, float beta){
    // Calculate probabilities
    std::vector<float> probabilities(2*this->sightMatrix.size(), 0);

    int sum = 0;

    for(int i = 0; i < this->sightMatrix.size(); i++){
        if(!visited(i)){
            probabilities[2*i] = 
                (pow(pheromones[this->currentNode][i], alpha)) * 
                (pow(this->sightMatrix[this->currentNode][i], beta));
            probabilities[2*i + 1] = 
                (pow(pheromones[i][this->initialNode], alpha)) * 
                (pow(this->sightMatrix[i][this->initialNode], beta));
            sum += probabilities[2*i] + probabilities[2*i+1];
        }
    }
    if(sum == 0){
        return false;
    }

    probabilities[0] = probabilities[0]/2.0;
    for(int i = 1; i < probabilities.size(); i++){
        probabilities[i] = probabilities[i]/sum;
        probabilities[i] += probabilities[i-1];
    }

    // Choose next node based on calculated probabilities

    double choice = (float) rand()/RAND_MAX;
    int nextNode = 0;

    while(choice > probabilities[nextNode]){
        nextNode += 1;
    }

    if(nextNode == this->currentNode){
        return false;
    }

    if(nextNode%2){     //if nextNode can't be divided by 2
        nextNode = nextNode/2;
        this->totalGain += gainMatrix[nextNode][this->initialNode];
        this->initialNode = nextNode;

        for(int i = 0; i < this->route1.size(); i++){
            if(this->route1[i] == -1){
                this->route1[i] = nextNode;
                break;
            }
        }
    }
    else{               //if nextNode can be divided by 2
        nextNode = nextNode/2;
        this->totalGain += gainMatrix[this->currentNode][nextNode];
        this->currentNode = nextNode;

        for(int i = 0; i < this->route1.size(); i++){
            if(this->route1[i] == -1){
                this->route1[i] = nextNode;
                break;
            }
        }
    }

    return true;
}

void Ant::updatePheromones(std::vector<std::vector<float>> &pheromones){
    float temp = 1 - (1/((float) this->totalGain));
    for(int i; i < this->route.size() - 1; i++){
        pheromones[this->route[i]][this->route[i+1]] += temp;
    }
}

void Ant::updateRoute(){
    int index = 0;
    for(int i = this->route2.size()-1; i >= 0; i--){
        if(this->route2[i] == -1) continue;
        this->route[index] = this->route2[i];
        index++;
    }
    
    for(int i = 0; i < this->route1.size(); i++){
        if(this->route1[i] == -1) break;
        this->route[index] = this->route1[i];
        index++;
    }
}

std::vector<int> Ant::getRoute(){
    this->updateRoute();
    return this->route;
}

int Ant::getGain(){
    return this->totalGain;
}