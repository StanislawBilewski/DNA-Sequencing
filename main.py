import random
import time

iter = 40

class Ant:
    def __init__(self, initialNode=0, sightMatrix=[]):
        self.totalGain = 0
        self.initialNode = initialNode
        self.currentNode = initialNode
        self.sightMatrix = []
        self.route = [initialNode]
        for i in range(len(sightMatrix)):
            self.sightMatrix.append(sightMatrix[i].copy())
            self.sightMatrix[i][self.currentNode] = 0

    def calcProbabilities(self, pheromones, alpha, beta):
        probabilities = []
        for i in range(len(self.sightMatrix)):
            probabilities.append(
                (pheromones[self.currentNode][i] ** alpha) *
                (self.sightMatrix[self.currentNode][i] ** beta))
        temp = sum(probabilities)

        if(temp == 0):
            return [0]*len(self.sightMatrix)

        for i in range(len(self.sightMatrix)):
            probabilities[i] = probabilities[i]/temp

        for i in range(1,len(self.sightMatrix)):
            probabilities[i] += probabilities[i-1]

        return probabilities

    def chooseNextNode(self, probabilities):
        temp = random.random()
        nextNode = 0
        while temp > probabilities[nextNode]:
            nextNode += 1

        self.totalGain += gainMatrix[self.currentNode][nextNode]
        self.currentNode = nextNode
        self.route.append(self.currentNode)

        for i in range(len(self.sightMatrix)):
            self.sightMatrix[i][self.currentNode] = 0

    def updatePheromones(self, pheromones):
        if(self.totalGain > 0):
            temp = 1 - (1/self.totalGain)
            for i in range(len(self.route)-1):
                pheromones[self.route[i]][self.route[i+1]] += temp

def getGainMatrix(inp):
    gainMatrix = []
    l = len(inp[0])
    S = len(inp)

    for x in range(S):
        gainMatrix.append([])
        seq = inp[x]
        for y in range(S):
            neighbor = False
            for i in range(l):
                if (seq == inp[y]):
                    break
                if (seq[i:] == inp[y][:l - i]):
                    gainMatrix[x].append(l - i)
                    neighbor = True
                    break

            if (neighbor == False):
                gainMatrix[x].append(0)

    return gainMatrix

def getSightMatrix(gain):
    sightMatrix = []
    for i in range(len(gain)):
        sightMatrix.append([])
        for j in gain[i]:
            sightMatrix[i].append(j**2)

    return sightMatrix

def initPheromones(l):
    pheromones = []
    for _ in range(l):
        pheromones.append([1]*l)

    return pheromones

def vaporization(pheromoneMatrix, epsilon):
    for i in range(len(pheromoneMatrix)):
        for j in range(len(pheromoneMatrix)):
            pheromoneMatrix[i][j] *= (1-epsilon)

def antColonyOptimization(
        initialNode,    # mówi samo za siebie
        sightMatrix,    # mówi samo za siebie
        iter = 40,      # mówi samo za siebie
        nOfAnts = 40,   # mówi samo za siebie
        alpha = 1,      # waga feromonu
        beta = 2,       # współczynnik widoczności
        epsilon = 0.5   # współczynnik parowania feromonu
    ):

    for _ in range(iter):
        ants = []
        distance = 0
        distances = []
        paths=[]

        for _ in range(nOfAnts):
            ants.append(Ant(initialNode, sightMatrix))

        for ant in ants:
            while True:
                probabilities = ant.calcProbabilities(pheromoneMatrix, alpha, beta)
                if sum(probabilities) == 0:
                    break
                ant.chooseNextNode(probabilities)

            distances.append(ant.totalGain)
            paths.append(ant.route)

        vaporization(pheromoneMatrix, epsilon)

        for ant in ants:
            ant.updatePheromones(pheromoneMatrix)

        for i in range(len(paths)):
            if(distance > distances[i] or distance==0):
                distance = distances[i]             # wyznaczanie długości najkrótszej ścieżki
                shortestPath = paths[i]

    return shortestPath, distance




# input = open("data.txt", 'r')
# inputPoints = loadPoints(input.read().split("\n"))

f = open("sequence.txt", "r")

words = f.readlines()

for i in range(len(words)):
	words[i] = words[i].strip('\n')

gainMatrix = getGainMatrix(words)

sightMatrix = getSightMatrix(gainMatrix)
paths = []
diss = []

# print(gainMatrix)

for initialNode in range(len(gainMatrix)):
    pheromoneMatrix = initPheromones(len(sightMatrix))

    path, dis = antColonyOptimization(initialNode, sightMatrix)
    paths.append(path)
    diss.append(dis)

temp = 0
for i in range(len(paths)):
    if(diss[i] > temp):
        temp = diss[i]
        path = paths[i]

print(path)
print(temp)