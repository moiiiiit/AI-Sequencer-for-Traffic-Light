# Author: Mohit Bhole
# The University of Texas at Dallas, CS 4365 - Artificial Intelligence | Dr. Elmer Salazar
# Traffic lights scheduler at an intersection from pre-known car arrival data.
# Time is discrete steps, each car takes 1 time to cross intersection.
# Input file has each line of format: "TIME ORIGIN DESTINATION" (of arrival of a car at the intersection)
# DESTINATION can be straight or left and ORIGIN can be N,S,E,W (Four way intersection, 3 lane each way)

# ====================================================================================================================

# Run script using python main.py *input filename*

# State Space Search Strategy: Greedy Best First Search (Variable Heuristic)

# ====================================================================================================================

import sys
from operator import itemgetter

maximumWaitTime = 19    # maximum time a car can wait and we keep ignoring adding it to queue
timeElapsed = 0     # current time elapsed
minimumLightTime = 4    # at least four cars at once
currLightTime = 0   # just a counter


# ====================================================================================================================

class Car:  # Car Object
    def __init__(self, time, origin, direction):  # Initialize the object
        self.time = int(time.strip())
        self.origin = origin.strip()
        self.direction = direction.strip()

    def print(self):  # Print the values stored in the Car object
        print(self.time + " " + self.origin + " " + self.direction, end='\t')


# State: list of cars in each lane, the traffic signal on each light, and the current time step.
class State:
    def __init__(self, nSList=[], sSList=[], eSList=[], wSList=[], nLList=[], sLList=[], eLList=[], wLList=[], nArrow=0,
                 sArrow=0, eArrow=0, wArrow=0, nLight=0,
                 sLight=0, eLight=0, wLight=0, currDepth=0, currConfig=-1):
        self.nSList = nSList.copy()
        self.sSList = sSList.copy()
        self.eSList = eSList.copy()
        self.wSList = wSList.copy()
        self.nLList = nLList.copy()
        self.sLList = sLList.copy()
        self.eLList = eLList.copy()
        self.wLList = wLList.copy()
        self.nArrow = nArrow
        self.sArrow = sArrow
        self.eArrow = eArrow
        self.wArrow = wArrow
        self.nLight = nLight
        self.eLight = eLight
        self.wLight = wLight
        self.sLight = sLight
        self.depth = currDepth
        self.config = currConfig

    def makeCopyState(self, state):
        self.nSList = state.nSList.copy()
        self.sSList = state.sSList.copy()
        self.eSList = state.eSList.copy()
        self.wSList = state.wSList.copy()
        self.nLList = state.nLList.copy()
        self.sLList = state.sLList.copy()
        self.eLList = state.eLList.copy()
        self.wLList = state.wLList.copy()
        self.nArrow = state.nArrow
        self.sArrow = state.sArrow
        self.eArrow = state.eArrow
        self.wArrow = state.wArrow
        self.nLight = state.nLight
        self.eLight = state.eLight
        self.wLight = state.wLight
        self.sLight = state.sLight
        self.depth = state.depth
        self.config = state.config

    def lightsOff(self):
        self.nLight = 0
        self.sLight = 0
        self.eLight = 0
        self.wLight = 0
        self.nArrow = 0
        self.sArrow = 0
        self.eArrow = 0
        self.wArrow = 0
        self.config = -1

    def printLights(self):
        print("\nTime Stamp " + str(timeElapsed))
        print("\nNorth Light: " + ("Green" if self.nLight==1 else "Red"))
        print("South Light: " + ("Green" if self.sLight==1 else "Red"))
        print("East Light: " + ("Green" if self.eLight==1 else "Red"))
        print("West Light: " + ("Green" if self.wLight==1 else "Red"))

        print("\nNorth Arrow: " + ("Green" if self.nArrow==1 else "Red"))
        print("South Arrow: " + ("Green" if self.sArrow==1 else "Red"))
        print("East Arrow: " + ("Green" if self.eArrow==1 else "Red"))
        print("West Arrow: " + ("Green" if self.wArrow==1 else "Red"))
        print(
            "\n=================================")

    def printState(self):
        print("\nState " + str(self.depth) + " at Time Step " + str(timeElapsed))
        print("\nCars with N Origin going Straight: \t" + str(len(self.nSList)) + " cars")
        for i in range(len(self.nSList)):
            print(self.nSList[i], end='\t')
        print("\n\nCars with N Origin going Left: \t" + str(len(self.nLList)) + " cars")
        for i in range(len(self.nLList)):
            print(self.nLList[i], end='\t')

        print("\n\nCars with S Origin going Straight: \t" + str(len(self.sSList)) + " cars")
        for i in range(len(self.sSList)):
            print(self.sSList[i], end='\t')
        print("\n\nCars with S Origin going Left: \t" + str(len(self.sLList)) + " cars")
        for i in range(len(self.sLList)):
            print(self.sLList[i], end='\t')

        print("\n\nCars with E Origin going Straight: \t" + str(len(self.eSList)) + " cars")
        for i in range(len(self.eSList)):
            print(self.eSList[i], end='\t')
        print("\n\nCars with E Origin going Left: \t" + str(len(self.eLList)) + " cars")
        for i in range(len(self.eLList)):
            print(self.eLList[i], end='\t')

        print("\n\nCars with W Origin going Straight: \t" + str(len(self.wSList)) + " cars")
        for i in range(len(self.wSList)):
            print(self.wSList[i], end='\t')
        print("\n\nCars with W Origin going Left: \t" + str(len(self.wLList)) + " cars")
        for i in range(len(self.wLList)):
            print(self.wLList[i], end='\t')

        print("\n\nNorth Light: " + str(self.nLight) + " Arrow: " + str(self.nArrow))
        print("\nSouth Light: " + str(self.sLight) + " Arrow: " + str(self.sArrow))
        print("\nEast Light: " + str(self.eLight) + " Arrow: " + str(self.eArrow))
        print("\nWest Light: " + str(self.wLight) + " Arrow: " + str(self.wArrow))
        print(
            "\n=======================================================================================================")


# ====================================================================================================================

# We have to generate children for every single possibility of signal change
# There are universally two acceptable ways of having the lights on
# First having both the turn light and straight light GREEN of each of the directions N,S,E,W
# Second is having the straight light GREEN of opposite directions, i.e. North-South and East-West. Separately.
# Implementation:
def generateChildren(state):
    children = []
    global currLightTime
    # First, turn N-S light on
    child1 = State()
    child1.makeCopyState(state)
    child1.lightsOff()
    child1.nLight = 1
    child1.sLight = 1
    child1.config = 0
    child1.depth = child1.depth + 1
    if child1.nSList:  # If there is a car in the list
        if child1.nSList[0] <= timeElapsed:  # If the car is actually at the intersection
            child1.nSList.pop(0)  # Remove 1 car from the North-going-straight queue
    if child1.sSList:  # If there is a car in the list
        if child1.sSList[0] <= timeElapsed:  # If the car is actually at the intersection
            child1.sSList.pop(0)  # Remove 1 car from the South-going-straight queue

    # Second, turn E-W light on
    child2 = State()
    child2.makeCopyState(state)
    child2.lightsOff()
    child2.eLight = 1
    child2.wLight = 1
    child2.config = 1
    child2.depth = child2.depth + 1
    if child2.eSList:
        if child2.eSList[0] <= timeElapsed:
            child2.eSList.pop(0)  # Remove 1 car from the East-going-straight queue
    if child2.wSList:
        if child2.wSList[0] <= timeElapsed:
            child2.wSList.pop(0)  # Remove 1 car from the West-going-straight queue

    # Third, turn N light and N arrow on
    child3 = State()
    child3.makeCopyState(state)
    child3.lightsOff()
    child3.nLight = 1
    child3.nArrow = 1
    child3.config = 2
    child3.depth = child3.depth + 1
    if child3.nSList:
        if child3.nSList[0] <= timeElapsed:
            child3.nSList.pop(0)
    if child3.nLList:
        if child3.nLList[0] <= timeElapsed:
            child3.nLList.pop(0)

    # Fourth, turn S light and S arrow on
    child4 = State()
    child4.makeCopyState(state)
    child4.lightsOff()
    child4.sLight = 1
    child4.sArrow = 1
    child4.config = 3
    child4.depth = child4.depth + 1
    if child4.sSList:
        if child4.sSList[0] <= timeElapsed:
            child4.sSList.pop(0)
    if child4.sLList:
        if child4.sLList[0] <= timeElapsed:
            child4.sLList.pop(0)

    # Fifth, turn E light and E arrow on
    child5 = State()
    child5.makeCopyState(state)
    child5.lightsOff()
    child5.eLight = 1
    child5.eArrow = 1
    child5.config = 4
    child5.depth = child5.depth + 1
    if child5.eSList:
        if child5.eSList[0] <= timeElapsed:
            child5.eSList.pop(0)
    if child5.eLList:
        if child5.eLList[0] <= timeElapsed:
            child5.eLList.pop(0)

    # Sixth, turn W light and W arrow on
    child6 = State()
    child6.makeCopyState(state)
    child6.lightsOff()
    child6.wLight = 1
    child6.wArrow = 1
    child6.config = 5
    child6.depth = child6.depth + 1
    if child6.wSList:
        if child6.wSList[0] <= timeElapsed:
            child6.wSList.pop(0)
    if child6.wLList:
        if child6.wLList[0] <= timeElapsed:
            child6.wLList.pop(0)

    # The above methods shall cover all optimal legal ways of turning on the lights
    # I have removed the case where opposite directions have arrows GREEN because on a three lane road they're likely
    # to cause accidents
    children.append(child1)
    children.append(child2)
    children.append(child3)
    children.append(child4)
    children.append(child5)
    children.append(child6)
    return children


# Heuristic: Prefer to keep the light the same. Change light when the wait time of a car is greater than maximumWaitTime
# Heuristic will be determined from the current and next state


def bestFirstSearch(state):  # Recursive Method
    global timeElapsed
    global currLightTime
    if not state.nSList and not state.nLList and not state.sSList and not state.sLList and not state.eSList and not state.eLList and not state.wSList and not state.wLList:
        print("\nGoal State Reached")
        # state.printState()    # Print the whole state
        return state  # Base Case
    # else:
    # state.printState()    # Print the whole state

    # timeElapsed - list[0] + ((number of cars in the lane)<50?numCars/5:0)
    waitTimes = [{"list": "nSList", "value": timeElapsed - state.nSList[0] + (
        state.nSList.__len__() / 4 if state.nSList.__len__() < 40 else 0) if state.nSList else -100000},
                 # This is the heuristic
                 {"list": "nLList", "value": timeElapsed - state.nLList[0] + (
                     state.nLList.__len__() / 4 if state.nLList.__len__() < 40 else 0) if state.nLList else -100000},
                 {"list": "sSList", "value": timeElapsed - state.sSList[0] + (
                     state.sSList.__len__() / 4 if state.sSList.__len__() < 40 else 0) if state.sSList else -100000},
                 {"list": "sLList", "value": timeElapsed - state.sLList[0] + (
                     state.sLList.__len__() / 4 if state.sLList.__len__() < 40 else 0) if state.sLList else -100000},
                 {"list": "eSList", "value": timeElapsed - state.eSList[0] + (
                     state.eSList.__len__() / 4 if state.eSList.__len__() < 40 else 0) if state.eSList else -100000},
                 {"list": "eLList", "value": timeElapsed - state.eLList[0] + (
                     state.eLList.__len__() / 4 if state.eLList.__len__() < 40 else 0) if state.eLList else -100000},
                 {"list": "wSList", "value": timeElapsed - state.wSList[0] + (
                     state.wSList.__len__() / 4 if state.wSList.__len__() < 40 else 0) if state.wSList else -100000},
                 {"list": "wLList", "value": timeElapsed - state.wLList[0] + (
                     state.wLList.__len__() / 4 if state.wLList.__len__() < 40 else 0) if state.wLList else -100000},
                 ]
    waitTimes.sort(key=itemgetter("value"), reverse=True)
    # print(waitTimes)

    currChildren = generateChildren(state)
    timeElapsed = timeElapsed + 1
    # Go through the children and select one that is optimal according to our selected heuristic
    for i in currChildren:
        # Case 1: Keep the light the same if wait time for each of the lanes is less than maximum wait time
        if currLightTime > minimumLightTime:
            currLightTime=0
            if waitTimes[0].get("value") >= maximumWaitTime:

                # FIRST PRIORITY NORTH
                if waitTimes[0].get("list") == "nSList":
                    for item in waitTimes:
                        if item.get("list") == "nLList":
                            # nL, nS
                            if currChildren[2].config != state.config:
                                state.printLights()
                            return bestFirstSearch(currChildren[2])
                        elif item.get("list") == "sSList":
                            # sS, nS
                            if currChildren[0].config != state.config:
                                state.printLights()
                            return bestFirstSearch(currChildren[0])
                    if currChildren[2].config != state.config:
                        state.printLights()
                    return bestFirstSearch(currChildren[2])

                elif waitTimes[0].get("list") == "nLList":
                    # nL, nS
                    if currChildren[2].config != state.config:
                        state.printLights()
                    return bestFirstSearch(currChildren[2])

                # FIRST PRIORITY SOUTH
                elif waitTimes[0].get("list") == "sSList":
                    for item in waitTimes:
                        if item.get("list") == "sLList":
                            # sL, sS
                            if currChildren[3].config != state.config:
                                state.printLights()
                            return bestFirstSearch(currChildren[3])
                        elif item.get("list") == "nSList":
                            # sS, nS
                            if currChildren[0].config != state.config:
                                state.printLights()
                            return bestFirstSearch(currChildren[0])
                    if currChildren[3].config != state.config:
                        state.printLights()
                    return bestFirstSearch(currChildren[3])

                elif waitTimes[0].get("list") == "sLList":
                    # sL, sS
                    if currChildren[3].config != state.config:
                        state.printLights()
                    return bestFirstSearch(currChildren[3])

                # FIRST PRIORITY EAST
                elif waitTimes[0].get("list") == "eSList":
                    for item in waitTimes:
                        if item.get("list") == "eLList":
                            # eL, eS
                            if currChildren[4].config != state.config:
                                state.printLights()
                            return bestFirstSearch(currChildren[4])
                        elif item.get("list") == "wSList":
                            # eS, wS
                            if currChildren[1].config != state.config:
                                state.printLights()
                            return bestFirstSearch(currChildren[1])
                    if currChildren[4].config != state.config:
                        state.printLights()
                    return bestFirstSearch(currChildren[4])

                elif waitTimes[0].get("list") == "eLList":
                    # eL, eS
                    if currChildren[4].config != state.config:
                        state.printLights()
                    return bestFirstSearch(currChildren[4])

                # FIRST PRIORITY WEST
                elif waitTimes[0].get("list") == "wSList":
                    for item in waitTimes:
                        if item.get("list") == "wLList":
                            # wL, wS
                            if currChildren[5].config != state.config:
                                state.printLights()
                            return bestFirstSearch(currChildren[5])
                        elif item.get("list") == "eSList":
                            # wS, eS
                            if currChildren[1].config != state.config:
                                state.printLights()
                            return bestFirstSearch(currChildren[1])
                    if currChildren[5].config != state.config:
                        state.printLights()
                    return bestFirstSearch(currChildren[5])

                else:  # waitTimes[0].get("list") == "wLList"
                    # wL, wS
                    if currChildren[5].config != state.config:
                        state.printLights()
                    return bestFirstSearch(currChildren[5])

            else:  # maximumWaitTime is greater, keep the lights the same
                for item in currChildren:
                    if item.config == state.config:
                        return bestFirstSearch(item)
                if currChildren[1].config != state.config:
                    state.printLights()
                return bestFirstSearch(currChildren[1])  # Something really didn't work, so just default to N-S on
        else:  # maximumWaitTime is greater, keep the lights the same
            currLightTime=currLightTime+1
            for item in currChildren:
                if item.config == state.config:
                    return bestFirstSearch(item)
            if currChildren[1].config != state.config:
                state.printLights()
            return bestFirstSearch(currChildren[1])  # Something really didn't work, so just default to N-S on


# =====================================================================================================================
#   DRIVER METHOD
# =====================================================================================================================

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "uniform.txt"

fileContents = open(filename, "r")
carListNS = []
carListSS = []
carListES = []
carListWS = []
carListNL = []
carListSL = []
carListEL = []
carListWL = []
# print(fileContents.read())  # Print the file for testing

for line in fileContents:
    # print(line)
    temp = line.split(" ")
    c1 = Car(temp[0], temp[1], temp[2])
    # c1.print()
    if c1.origin == "N":
        if c1.direction == "straight":
            carListNS.append(c1.time)
        else:
            carListNL.append(c1.time)

    if c1.origin == "S":
        if c1.direction == "straight":
            carListSS.append(c1.time)
        else:
            carListSL.append(c1.time)

    if c1.origin == "E":
        if c1.direction == "straight":
            carListES.append(c1.time)
        else:
            carListEL.append(c1.time)

    if c1.origin == "W":
        if c1.direction == "straight":
            carListWS.append(c1.time)
        else:
            carListWL.append(c1.time)

initialState = State(carListNS, carListSS, carListES, carListWS, carListNL, carListSL, carListEL, carListWL, 0, 0, 0, 0,
                     0, 0, 0, 0, 0)
print("\n=======================================================================================================")
print(" -----------------EACH STATE TRAVERSED IS PRINTED ONE BY ONE UNTIL GOAL IS REACHED--------------------")
print("=======================================================================================================")

bestFirstSearch(initialState)

# ====================================================================================================================
