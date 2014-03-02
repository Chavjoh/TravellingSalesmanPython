#!/usr/bin/python
# coding: latin-1

#------------------------------------------------------------------------------#
# Artificial intelligence - Genetic Algorithms: Travelling salesman problem    #
# ============================================================================ #
# Organization: HE-Arc Engineering                                             #
# Developer(s): Dany Jupille                                                   #
#               Johan Chavaillaz                                               #
#                                                                              #
# Filename:     ChavaillazJupille.py                                           #
# Description:  #N/A                                                           #
# Version:      1.0                                                            #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
#                                                                              #
#                               LIBRARIES IMPORT                               #
#                                                                              #
#------------------------------------------------------------------------------#

import pygame
import sys
import time
import math
import random

from math import hypot
from collections import deque
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN

#------------------------------------------------------------------------------#
#                                                                              #
#                                   CLASSES                                    #
#                                                                              #
#------------------------------------------------------------------------------#

# Uses to manage GUI of pygame
class GuiManager(object):
    """Manage the GUI provided by the Pygame module.

    The main purpose of this manager is to avoid multiple initialization of the
    Pygame display by calling multiple times the pygame.init() method. We check
    first if the GUI is already opened.
    """
    
    cityRadius = 3

    colorBlack = [0, 0, 0]
    colorRed = [255, 0, 0]
    colorGreen = [0, 255, 0]
    colorBlue = [0, 0, 255]
    colorWhite = [255, 255, 255]

    guiOpened = False

    screenDimensions = (500, 500)
    screenWindow = None
    screenSurface = None
    screenTitle = 'Travelling salesman solver - Chavaillaz & Jupille'

    @staticmethod
    def openGui():
        if not GuiManager.guiOpened:
        
            # Pygame initialization
            pygame.init()
            pygame.display.set_caption(GuiManager.screenTitle)

            # Create window and get useful informations
            GuiManager.screenWindow = pygame.display.set_mode(GuiManager.screenDimensions)
            GuiManager.screenSurface = pygame.display.get_surface()

            GuiManager.guiOpened = True

    @staticmethod
    def closeGui():
        if GuiManager.guiOpened:
        
            # Delete informations
            GuiManager.screenWindow = None
            GuiManager.screenSurface = None

            # Close window
            pygame.display.quit()

            GuiManager.guiOpened = False
    
    @staticmethod
    def drawSolution(bestPopulation):
        if GuiManager.guiOpened:
            GuiManager.screenSurface.fill(0)
            
            oldCity = None
            
            for city in bestPopulation.getTravel():
                if oldCity != None:
                    pygame.draw.line(GuiManager.screenSurface, GuiManager.colorWhite, oldCity.getLocation(), city.getLocation())
                
                oldCity = city
            
            pygame.draw.line(GuiManager.screenSurface, GuiManager.colorWhite, oldCity.getLocation(), bestPopulation.getTravel()[0].getLocation())

            for city in bestPopulation.getTravel():
                pygame.draw.circle(GuiManager.screenSurface, GuiManager.colorRed, city.getLocation(), GuiManager.cityRadius)
                
            pygame.display.flip()

# Class representing cities with a name and a location (x, y)
class City(object):
    """Represents a city for the travelling salesman problem.

    It simply requires a name and a location. It also provides a method to get
    the euclidian distance between two cities.
    """

    def __init__(self, name, x, y):

        if not isinstance(name, str):
            raise TypeError('City __init__: argument 1 must be a string.')
        
        if not isinstance(x, int):
            raise TypeError('City __init__: argument 2 must be an integer.')

        if not isinstance(y, int):
            raise TypeError('City __init__: argument 3 must be an intenger.')
        
        self._name = name
        self._x = x
        self._y = y
    
    def getName(self):
        return self._name

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getLocation(self):
        return (self.getX(), self.getY())

    def getDistance(self, other):
        # Euclidian distance
        x1,y1 = self.getX(), self.getY()
        x2,y2 = other.getX(), other.getY()
        
        return hypot(x2-x1, y2-y1)

# Class representing individual solution of the travelling salesman problem
class Solution(object):
    """Represents an individual solution of the travelling salesman problem.

    For performance purpose, we store the travel distance. It avoids multiples
    calculations who are preventables.
    """

    def __init__(self):
        self._travel = []
        self._travelDistance = 0

    def _calculateTravelDistance(self):
        self._travelDistance = 0
        
        previousCity = self._travel[-1]
        
        for city in self._travel:                
            self._travelDistance += previousCity.getDistance(city)
            previousCity = city;

    def getTravel(self):
        return self._travel

    def setTravel(self, travel):
        self._travel = travel
        self._calculateTravelDistance()

    def getTravelDistance(self):
        return self._travelDistance

#------------------------------------------------------------------------------#
#                                                                              #
#                             DECORATORS FUNCTIONS                             #
#                                                                              #
#------------------------------------------------------------------------------#

# Decorator for static variables
def staticvar(name, value):
    def decorate(function):
        setattr(function, name, value)
        return function
    return decorate

#------------------------------------------------------------------------------#
#                                                                              #
#                             UTILITIES FUNCTIONS                              #
#                                                                              #
#------------------------------------------------------------------------------#

# Convert temporarily a list into a deque to perform a shift
def shift(l, n):
    d = deque(l)
    d.rotate(-3) # Negative value: "to the left"
    return list(d)

# Get towns in a file containing names and locations (x, y)
def getCitiesByFile(citiesFilePath):
    cities = []
    citiesRowData = []

    # One city per row
    with open(citiesFilePath) as citiesFile:
        for citiesRow in citiesFile:
            citiesRowData.append(citiesRow.split(' '))

    # Axiom: [[CITY_NAME] [CITY_X] [CITY_Y]]
    for citiesData in citiesRowData:
        name = citiesData[0]
        x = int(citiesData[1])
        y = int(citiesData[2])

        cities.append(City(name, x, y))
        
    return cities

# Generate towns with mouse inputs by user
def getCitiesByGui():
    
    # Variables initialization
    cities = []
    nextCityId = 0

    # Stop condition
    collecting = True

    # Start collecting loop
    while collecting:

        # Events management
        for event in pygame.event.get():

            # Red cross / Alt+F4
            if event.type == QUIT:
                GuiManager.closeGui()
                sys.exit(0)

            # Key down events: only look for return button
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False

            # Mouse button down events
            elif event.type == MOUSEBUTTONDOWN:
                cities.append(City('v{0}'.format(nextCityId), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                nextCityId += 1

                GuiManager.screenSurface.fill(GuiManager.colorBlack)

                for city in cities:
                    pygame.draw.circle(GuiManager.screenSurface, GuiManager.colorRed, city.getLocation(), GuiManager.cityRadius)

                # Flip display (double buffering)
                pygame.display.flip()

    return cities

#------------------------------------------------------------------------------#
#                                                                              #
#                         GENETIC ALGORITHMS FUNCTIONS                         #
#                                                                              #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
#                                                                              #
#                             G.A.F.: SOLVE (MAIN)                             #
#                                                                              #
#------------------------------------------------------------------------------#

# Solve the travelling salesman problem with a genetic algorithm
def ga_solve(file = None, gui = True, maxtime = 0):
    cities = None
    bestSolution = None
    
    if file != None:
        cities = getCitiesByFile(file)
    else:
        GuiManager.openGui()
        cities = getCitiesByGui()
    
    if gui:
        GuiManager.openGui()
    else:
        GuiManager.closeGui()

    startTimestamp = time.time()
    
    # Create initial population and return list individual solution
    population = ga_initialization(cities)
    
    while True:
        
        # Selection in population
        ga_selection(population)
        
        # Crossing population
        ga_crossoverAll(population)
        
        # Mutation of the population
        ga_mutationAll(population)
        
        # Calculate distance
        populationSorted = sorted(population, key=lambda individualSolution: individualSolution.getTravelDistance())
        
        # Best solution 
        bestSolution = populationSorted[0]
        print("Best solution distance = ", bestSolution.getTravelDistance())
        
        # Draw solution
        GuiManager.drawSolution(bestSolution)
        
        # Break if maxtime is reached
        if maxtime > 0:
            if time.time() - startTimestamp > maxtime:
                break
        
        # Break if result is stagnating
        else:
            if ga_resultStagnation(bestSolution):
                break
    
    # Calculate city name list
    cityNameList = [x.getName() for x in bestSolution.getTravel()]
    
    # Return expected result
    return bestSolution.getTravelDistance(), cityNameList

#------------------------------------------------------------------------------#
#                                                                              #
#                            G.A.F.: INITIALIZATION                            #
#                                                                              #
#------------------------------------------------------------------------------#

# Initialization of the genetic algorithm
def ga_initialization(cities):
    population = []
    populationSize = calculatePopulationSize(len(cities))
    citiesSize = len(cities)

    # Greedy algorithm for the first solution
    citiesCopy = []
    cityIndex = 0
    
    lastCity = cities.pop(cityIndex)
    citiesCopy.append(lastCity)
        
    while len(cities) > 0:
        minDistance = -1

        for i, city in enumerate(cities):
            currentDistance = lastCity.getDistance(city)
                
            if minDistance == -1 or minDistance > currentDistance:
                cityIndex = i
                minDistance = currentDistance

        lastCity = cities.pop(cityIndex)
        citiesCopy.append(lastCity)

    solution = Solution()
    solution.setTravel(citiesCopy)

    population.append(solution)

    # Generate enough solutions, based on the first solution
    for i in range(1, populationSize):
        solution = Solution()
        solution.setTravel(list(population[0].getTravel()))

        # We use the ga_mutation function: it will simply swap two elements
        ga_mutation(solution)

        population.append(solution)

    return population

# Calculates the population size
def calculatePopulationSize(citiesCount):
    """Calculates the size of the population for the travelling salesman problem.

    The size is based on the cities count and the following formula:
    |1 + log(citiesCount)| * 1000

    This formula ensures enough people in the population and goes pretty quickly
    in big numbers without exceeding a certain limit.
    """
    
    populationSize = int(math.fabs(math.log1p(citiesCount) * 1000))

    # For futures operations purpose, the size must be dividable by 4
    while populationSize % 4 != 0:
        populationSize += 1
        
    return populationSize

#------------------------------------------------------------------------------#
#                                                                              #
#                              G.A.F.: SELECTION                               #
#                                                                              #
#------------------------------------------------------------------------------#

# Selection of the genetic algorithm
def ga_selection(population):
    """The selection for the genetic algorithm.

    It is based on a ranking roulette wheel.
    Because instanciation of objects is an expensive operation, especially in
    high-level programming language, we must avoid it.

    To avoid this, we don't destroy half of the list, but reorganize it. At the
    end of this function, the first half of the list contains the remaining
    population for the crossover, and the other half contains the people who
    "died" at the natural selection.
    """
    
    populationLength = len(population)
    halfPopulationLength = int(populationLength / 2)

    maxRandomValue = 0
    cumulativeRankingValuesList = []

    for i in range(populationLength):
        maxRandomValue += i
        cumulativeRankingValuesList.append(maxRandomValue)

    randomValuesFactorsList = []

    for i in range(halfPopulationLength):
        randomValuesFactorsList.append(random.uniform(0, 1))

    randomValuesFactorsList.sort()

    currentIndex = 0
    selectedSolutionsIndexesList = []

    for randomValueFactor in randomValuesFactorsList:
        randomValue = maxRandomValue * randomValueFactor
        
        while randomValue < cumulativeRankingValuesList[currentIndex]:
            currentIndex += 1

        selectedSolutionsIndexesList.append(currentIndex)

        maxRandomValue -= cumulativeRankingValuesList[currentIndex]
        cumulativeRankingValuesList[currentIndex] = 0

    # Bests solutions first
    population.sort(key = lambda solution: solution.getTravelDistance())

    for i, selectedIndex in enumerate(selectedSolutionsIndexesList):
        population[i], population[selectedIndex] = population[selectedIndex], population[i]

#------------------------------------------------------------------------------#
#                                                                              #
#                              G.A.F.: CROSSOVER                               #
#                                                                              #
#------------------------------------------------------------------------------#

# Crossover function
def ga_crossoverAll(population):
    """Cross the first half of the population.

    The children will be placed in the last half of the list.
    """
    
    populationLength = len(population)
    halfPopulationLength = int(populationLength / 2)
    i = 0

    while i < halfPopulationLength:
        ga_crossover(population, i, i + 1, halfPopulationLength + i, halfPopulationLength + i + 1)
        i += 2

# Crossover function (atom): cross two parents for two children
def ga_crossover(population, parent1Index, parent2Index, child1Index, child2Index):    
    new1 = []
    new2 = []
    cities1 = population[parent1Index].getTravel()
    cities2 = population[parent2Index].getTravel()
    
    # Axiom: len(cities1) == len(cities2)
    length = len(cities1)
    
    # indexPart1 = 0
    indexPart2 = math.floor(length / 3)
    indexPart3 = math.ceil(2 * length / 3)
    
    crossCities1 = cities1[indexPart2:indexPart3]
    crossCities2 = cities2[indexPart2:indexPart3]
    
    # Generation of crossover
    for increment in range(length):
        currentIndex = indexPart3 + increment
        if cities1[currentIndex % length] not in crossCities2:
            new1.append(cities1[currentIndex % length])
        if cities2[currentIndex % length] not in crossCities1:
            new2.append(cities2[currentIndex % length])
    
    new1.extend(crossCities2)
    new2.extend(crossCities1)
    shift(new1, length - indexPart3)
    shift(new2, length - indexPart3)
    
    population[child1Index].setTravel(new1)
    population[child2Index].setTravel(new2)

#------------------------------------------------------------------------------#
#                                                                              #
#                               G.A.F.: MUTATION                               #
#                                                                              #
#------------------------------------------------------------------------------#

# Mutation function
def ga_mutationAll(population):
    """Mutate 30% of the population.

    A mutation is "just" a swap of two cities in our case.
    """
    
    mutationPourcent = 0.3 # 30%
    
    sizePopulation = len(population)
    
    for i in range(round(sizePopulation * mutationPourcent)):
        randomIndex = random.randint(0, sizePopulation - 1)
        ga_mutation(population[randomIndex])

# Mutation function (atom)
def ga_mutation(solution):
    cities = solution.getTravel()
    
    maxIndex = len(cities) - 1
    randomIndex1 = random.randint(0, maxIndex)
    randomIndex2 = random.randint(0, maxIndex)
    
    cities[randomIndex1], cities[randomIndex2] = cities[randomIndex2], cities[randomIndex1]

    solution.setTravel(cities)

#------------------------------------------------------------------------------#
#                                                                              #
#                              G.A.F.: STAGNATION                              #
#                                                                              #
#------------------------------------------------------------------------------#

# Checks if the result varies from a delta
@staticvar("counter", 30)
@staticvar("oldDistance", -1)
def ga_resultStagnation(bestSolution):
    """Verify if our final result stagnates.

    A result "stagnates" if it is the same to millimeter (0.001 meter) for 30
    consecutives iterations.
    """
    
    test = False
    
    if ga_resultStagnation.oldDistance == -1:
        ga_resultStagnation.oldDistance = bestSolution.getTravelDistance()
    else:
        if abs(ga_resultStagnation.oldDistance - bestSolution.getTravelDistance()) < 0.001:
            ga_resultStagnation.counter -= 1
        else:
            ga_resultStagnation.counter = 30

        test = (ga_resultStagnation.counter == 0)

    ga_resultStagnation.oldDistance = bestSolution.getTravelDistance()

    return test

#------------------------------------------------------------------------------#
#                                                                              #
#                               "MAIN" FUNCTION                                #
#                                                                              #
#------------------------------------------------------------------------------#

# If this is the main module, run this
if __name__ == '__main__':

    argsCount = len(sys.argv)
    argsIndex = 1

    file = None
    gui = True
    maxtime = 0

    while argsIndex < argsCount:
        if sys.argv[argsIndex] == '--nogui':
            gui = False
        elif sys.argv[argsIndex] == '--maxtime':
            maxtime = int(sys.argv[argsIndex + 1])
            argsIndex += 1
        else:
            file = sys.argv[argsIndex]

        argsIndex += 1

    ga_solve(file, gui, maxtime)
