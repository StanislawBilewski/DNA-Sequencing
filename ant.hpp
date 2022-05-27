#ifndef ANTHPP
#define ANTHPP

#include <vector>

class Ant{
    private:
        int totalGain;
        int initialNode;
        int currentNode;
        std::vector<int> route;
        std::vector<int> route1;
        std::vector<int> route2;
        std::vector<std::vector<float>> sightMatrix;
        bool visited(int node);
        void updateRoute();

    public:
        Ant(int initialNode, std::vector<std::vector<float>> sightMatrix);

        bool chooseNextNode(std::vector<std::vector<int>> &gainMatrix, std::vector<std::vector<float>> &pheromones, float alpha, float beta);
        void updatePheromones(std::vector<std::vector<float>> &pheromones);

        int getGain();
        std::vector<int> getRoute();

};

#endif