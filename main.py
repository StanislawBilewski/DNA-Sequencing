import random
from os import listdir
import time

iterations = 40
antsNumber = 20

class Ant:
    def __init__(self, initialNode=0, sightMatrix=[]):
        self.totalGain = 0
        self.initialNode = initialNode
        self.currentNode = initialNode
        self.sightMatrix = []
        self.route = []
        self.route1 = [initialNode]
        self.route2 = []
        for i in range(len(sightMatrix)):
            self.sightMatrix.append(sightMatrix[i].copy())

    def calcProbabilities(self, pheromones, alpha, beta):
        probabilities = []
        temp = 0
        for i in range(len(self.sightMatrix)):
            if i in self.route1 or i in self.route2:                 # jeśli węzeł 'i' został już odwiedzony, to wtedy nie możemy go wykorzystać
                probabilities.append(0)
                probabilities.append(0)

            else:
                probabilities.append(           # prawdopodobieństwo przejścia z węzła 'currentNode' do węzła 'i' (doklejanie do końca)
                    (pheromones[self.currentNode][i] ** alpha) *        # indeks w liscie 'probabilities' będzie parzysty
                    (self.sightMatrix[self.currentNode][i] ** beta))
                    
                probabilities.append(           # prawdopodobieństwo przejścia z węzła 'i' do węzła 'initialNode' (doklejanie do początku)
                    (pheromones[i][self.initialNode] ** alpha) *        # indeks w liscie 'probabilities' będzie nieparzysty
                    (self.sightMatrix[i][self.initialNode] ** beta))
                temp += probabilities[-1] + probabilities[-2]

        if(temp == 0):
            return [0]*len(probabilities)

        probabilities[0] = probabilities[0]/temp
        for i in range(1, len(probabilities)):
            probabilities[i] = probabilities[i]/temp
            probabilities[i] += probabilities[i-1]

        return probabilities

    def chooseNextNode(self, probabilities):
        temp = random.random()
        nextNode = 0
        while temp > probabilities[nextNode]:
            nextNode += 1

        if nextNode % 2 == 0:
            nextNode //= 2
            self.totalGain += gainMatrix[self.currentNode][nextNode]
            self.currentNode = nextNode
            self.route1.append(self.currentNode)
        
        else:
            nextNode //= 2
            self.totalGain += gainMatrix[nextNode][self.initialNode]
            self.initialNode = nextNode
            self.route2.append(self.initialNode)


    def updatePheromones(self, pheromones):
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
        gain = 0
        path = []

        for _ in range(nOfAnts):
            ants.append(Ant(initialNode, sightMatrix))

        antno=0
        for ant in ants:
            print("ant",antno)
            antno+=1
            while True:
                probabilities = ant.calcProbabilities(pheromoneMatrix, alpha, beta)
                if probabilities[-1] == 0:
                    break
                ant.chooseNextNode(probabilities)

            for i in range(len(ant.route2) - 1, -1, -1):
                ant.route.append(ant.route2[i])

            for i in range(len(ant.route1)):
                ant.route.append(ant.route1[i])

            if(ant.totalGain > gain or gain == 0):
                gain = ant.totalGain
                path = ant.route

        vaporization(pheromoneMatrix, epsilon)

        for ant in ants:
            ant.updatePheromones(pheromoneMatrix)

    return path, gain


inp = input("Would you like to overwrite files that are already in output? (Y/N)")

if inp == "Y":
    outputs = []
elif inp == "N":
    outputs = listdir('outputs/')
else:
    exit

for filename in listdir('inputs/'):
    if(filename == 'Thumbs.db' or filename in outputs):
        continue

    f = open('inputs/'+filename, "r")

    words = f.readlines()

    for i in range(len(words)):
        words[i] = words[i].strip('\n')

    gainMatrix = getGainMatrix(words)

    sightMatrix = getSightMatrix(gainMatrix)

    for i in gainMatrix:
        print(i)
    
    print()

    for i in sightMatrix:
        print(i)
    # print(gainMatrix)

    pheromoneMatrix = initPheromones(len(sightMatrix))

    timetest = time.time()
    path, gain = antColonyOptimization(len(sightMatrix)//2, sightMatrix, iter=iterations, nOfAnts=antsNumber)
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
                    break

    print("Number of ants:",antsNumber)
    print("Number of iterations:",iterations)
    print("Path:",path)
    print("Length:",len(path))
    print("Instance Length:",len(gainMatrix))
    print("Gain:",gain)
    print("seq:", seq)
    print("Sequence Length:",len(seq))
    print("Time:",timetest,"\n")

    outputFile = open("outputs/" + filename, "w")

    outputFile.write("Number of ants: " + str(antsNumber) + "\n")

    outputFile.write("Number of iterations: " + str(iterations) + "\n")

    outputFile.write("Path: [" + ', '.join([str(elem) for elem in path]) + "]\n")
    
    outputFile.write("Length: " + str(len(path)) + "\n")
    
    outputFile.write("Instance Length: " + str(len(gainMatrix)) + "\n")

    outputFile.write("Gain: " + str(gain) + "\n")
    
    outputFile.write("seq: " + seq + "\n")
    
    outputFile.write("Sequence Length:" + str(len(seq)) + "\n")
    
    outputFile.write("Time: " + str(timetest) + "\n")
    
    outputFile.close()