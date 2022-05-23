import random
from os import listdir
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

    def calcProbabilities(self, pheromones, alpha, beta):
        probabilities = []
        for i in range(len(self.sightMatrix)):
            if i in self.route:                 # jeśli węzeł 'i' został już odwiedzony, to wtedy nie możemy go wykorzystać
                probabilities.append(0)
                probabilities.append(0)

            else:
                probabilities.append(           # prawdopodobieństwo przejścia z węzła 'currentNode' do węzła 'i' (doklejanie do końca)
                    (pheromones[self.currentNode][i] ** alpha) *        # indeks w liscie 'probabilities' będzie parzysty
                    (self.sightMatrix[self.currentNode][i] ** beta))
                    
                probabilities.append(           # prawdopodobieństwo przejścia z węzła 'i' do węzła 'initialNode' (doklejanie do początku)
                    (pheromones[i][self.initialNode] ** alpha) *        # indeks w liscie 'probabilities' będzie nieparzysty
                    (self.sightMatrix[i][self.initialNode] ** beta))
        temp = sum(probabilities)

        if(temp == 0):
            return [0]*len(probabilities)

        for i in range(len(probabilities)):
            probabilities[i] = probabilities[i]/temp

        for i in range(1,len(probabilities)):
            probabilities[i] += probabilities[i-1]

        return probabilities

    def chooseNextNode(self, probabilities):
        temp = random.random()
        nextNode = 0
        while temp > probabilities[nextNode]:
            nextNode += 1

        if nextNode%2 == 0:
            nextNode = nextNode//2
            self.totalGain += gainMatrix[self.currentNode][nextNode]
            self.currentNode = nextNode
            self.route.append(self.currentNode)
        
        else:
            nextNode = nextNode//2
            self.totalGain += gainMatrix[nextNode][self.initialNode]
            self.initialNode = nextNode
            self.route.insert(0, self.initialNode)


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

    for iteration in range(iter):
        print("iteracja:",iteration)
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


for filename in listdir('inputs/'):
    if(filename == 'Thumbs.db'):
        continue

    f = open('inputs/'+filename, "r")

    words = f.readlines()

    for i in range(len(words)):
        words[i] = words[i].strip('\n')

    gainMatrix = getGainMatrix(words)

    sightMatrix = getSightMatrix(gainMatrix)
    paths = []
    diss = []

    # print(gainMatrix)

    pheromoneMatrix = initPheromones(len(sightMatrix))

    timetest = time.time()
    path, gain = antColonyOptimization(0, sightMatrix, iter=60, nOfAnts=60)
    timetest = time.time() - timetest

    seq = ""
    l = len(words[0])

    for i in range(len(path)):
        if seq == "":
            seq = words[path[i]]

        else:
            for j in range(l):
                if (words[path[i-1]][j:] == words[path[i]][:l - j]):
                    seq += words[path[i]][l-j:]

    print("Path:",path)
    print("Gain:",gain)
    print("seq:", seq)
    print("Time:",timetest,"\n")

    outputFile = open("outputs/" + filename, "w")

    outputFile.write("Path:")
    outputFile.write(path)
    outputFile.write("\n")

    outputFile.write("Gain:")
    outputFile.write(gain)
    outputFile.write("\n")
    
    outputFile.write("seq:")
    outputFile.write(seq)
    outputFile.write("\n")
    
    outputFile.write("Time:")
    outputFile.write(timetest)
    outputFile.write("\n")