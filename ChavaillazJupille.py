#!/usr/bin/python
# coding: latin-1

# Libraries import
import pygame
import sys
import time

from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN

# Use to manage GUI of pygame
class GuiManager(object):

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

# Class representing cities with a name and a location (x, y)
class City(object):

    def __init__(self, name, x, y):

        if not isinstance(name, str):
            raise TypeError('City __init__: argument 1 must be a string')
        
        if not isinstance(x, int):
            raise TypeError('City __init__: argument 2 must be an integer')

        if not isinstance(y, int):
            raise TypeError('City __init__: argument 3 must be an intenger')

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

# Class representing individual solution of the travelling salesman problem
class IndividualSolution(object):

    def __init__(self):
        self._citiesPathList = []
        self._citiesPathValue = 0

    def addCityPath(self, cityPath):
        if len(self._citiesPathList) > 0:
            self._citiesPathValue += 
        
        self._citiesPathList.append(cityPath)

    def getCitiesPathList(self):
        return self._citiesPathList

    def getCitiesPathValue(self):
        return self._citiesPathValue

def calculatePopulationSize(citiesCount):
    return 5000

# Initialization of the genetic algorithm
def ga_initialization(cities):
    population = []

    # Generate enough population, based on cities count
    for i in range(calculatePopulationSize(len(cities))):

        # Greedy algorithm
        citiesCopy = list(cities)
        cityIndex = random.randrange(0, 5000)

        individualSolution = IndividualSolution()
        
        while len(citiesCopy) > 0:
            for city in citiesCopy:
                

        population.append(IndividualSolution())

# Selection of the genetic algorithm
def ga_selection():
    pass

# Solve the travelling salesman problem with a genetic algorithm
def ga_solve(file = None, gui = True, maxtime = 0):
    cities = None
    
    if file != None:
        cities = getCitiesByFile(file)
    else:
        GuiManager.openGui()
        cities = getCitiesByGui()

    

    if gui:
        GuiManager.openGui()
    else:
        GuiManager.closeGui()

    # time example : time.time() -> timestamp

    GuiManager.closeGui()
    
    return None

# Get towns in a file containing names and locations (x, y)
def getCitiesByFile(citiesFilePath):
    cities = []
    citiesRowData = []

    with open(citiesFilePath) as citiesFile:
        for citiesRow in citiesFile:
            citiesRowData.append(citiesRow.split(' '))

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
