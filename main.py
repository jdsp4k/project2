import random
import statistics

import numpy

from Schedule import Schedule
from DayOfWeek import DayOfWeek
from Event import Event
from Course import Course
from Instructor import Instructor
from Room import Room

__INSTRUCTORS = (
    Instructor("LOCK"),
    Instructor("GLEN"),
    Instructor("BANKS"),
    Instructor("RICHARDS"),
    Instructor("SHAW"),
    Instructor("SINGER"),
    Instructor("UTHER"),
    Instructor("TYLER"),
    Instructor("NUMEN"),
    Instructor("ZELDIN")
)
__CORSES = (
    Course("SLA101A", 50, ("GLEN", "LOCK", "BANKS", "ZELDIN"), ("NUMEN", "RICHARDS"), __INSTRUCTORS),
    Course("SLA101B", 50, ("GLEN", "LOCK", "BANKS", "ZELDIN"), ("NUMEN", "RICHARDS"), __INSTRUCTORS),
    Course("SLA191A", 50, ("GLEN", "LOCK", "BANKS", "ZELDIN"), ("NUMEN", "RICHARDS"), __INSTRUCTORS),
    Course("SLA191B", 50, ("GLEN", "LOCK", "BANKS", "ZELDIN"), ("NUMEN", "RICHARDS"), __INSTRUCTORS),
    Course("SLA201", 50, ("GLEN", "BANKS", "ZELDIN", "SHAW"), ("NUMEN", "RICHARDS", "SINGER"), __INSTRUCTORS),
    Course("SLA291", 50, ("LOCK", "BANKS", "ZELDIN", "SINGER"), ("NUMEN", "RICHARDS", "SHAW", "TYLER"), __INSTRUCTORS),
    Course("SLA303", 60, ("GLEN", "ZELDIN", "BANKS"), ("NUMEN", "SINGER", "SHAW"), __INSTRUCTORS),
    Course("SLA304", 25, ("GLEN", "BANKS", "TYLER"), ("NUMEN", "SINGER", "SHAW", "RICHARDS", "UTHER", "ZELDIN"), __INSTRUCTORS),
    Course("SLA394", 20, ("TYLER", "SINGER"), ("RICHARDS", "ZELDIN"), __INSTRUCTORS),
    Course("SLA449", 60, ("TYLER", "SINGER", "SHAW"), ("ZELDIN", "UTHER"), __INSTRUCTORS),
    Course("SLA451", 100, ("TYLER", "SINGER", "SHAW"), ("ZELDIN", "UTHER", "RICHARDS", "BANKS"), __INSTRUCTORS)
)
__ROOMS = (
    Room("SLATER", 3, 45),
    Room("ROMAN", 216, 30),
    Room("LOFT", 206, 75),
    Room("ROMAN", 201, 50),
    Room("LOFT", 310, 108),
    Room("BEACH", 201, 60),
    Room("BEACH", 301, 75),
    Room("LOGOS", 325, 450),
    Room("FRANK", 119, 60)
)
__DAYS = (
    DayOfWeek.MONDAY,
    DayOfWeek.WEDNESDAY,
    DayOfWeek.FRIDAY
)
__HOURS = (
    10,
    11,
    12,
    13,
    14,
    15
)

def generateInitialCandidates(n : int = 500) -> list[tuple[float, Schedule]]:
    l = []
    for i in range(0, n):
        eList : list[Event] = []
        for q in __CORSES:
            ins = random.choice(__INSTRUCTORS)
            room = random.choice(__ROOMS)
            day = random.choice(__DAYS)
            hour = random.choice(__HOURS)
            e = Event(q, ins, room, day, hour)
            eList.append(e)
        s = Schedule(eList)
        l.append((s.evalFitness(), s))
    return l

def step(curGen : list[tuple[float, Schedule]], mutRate : float) -> list[tuple[float, Schedule]]:
    parentA = random.choice(curGen)[1]
    parentB = random.choice(curGen)[1]

    childList : list[Event] = []
    for e in range(0, len(parentA.events)):
        if random.random() > 0.5:
            childList.append(parentA.events[e])
        else:
            childList.append(parentB.events[e])

    for e in range(0, len(childList)):    
        if random.random() <= mutRate / len(childList):
            ins = random.choice(__INSTRUCTORS)
            room = random.choice(__ROOMS)
            day = random.choice(__DAYS)
            hour = random.choice(__HOURS)
            childList[e] = Event(childList[e].course, ins, room, day, hour)

    s = Schedule(childList)
    curGen[0] = (s.evalFitness(), s)
    
    return curGen

random.seed()
g = 0
p = 20000
mutRate = 1.0
stats : list[tuple[float, float, float]] = []
gen = generateInitialCandidates()
print("Gen      Mean Fit Stdev Fit Max Fit Mut Rate")
while (g < p):
    gen.sort(key = lambda x : x[0])
    fitList = [item[0] for item in gen]
    stats.append((statistics.mean(fitList), statistics.stdev(fitList), gen[-1][0]))
    print(f"{g:6d}:  {stats[-1][0]:8.2f} {stats[-1][1]:9.2f} {stats[-1][2]:7.2f} {mutRate:6f}\r", end="")
    gen = step(gen, mutRate)
    prog = g/p
    mutRate = -(prog + 0.07) ** 4 + 0.75
    g += 1
print("")
#print(stats)
print(gen[-1][1])