from Course import Course
from Instructor import Instructor
from Room import Room
from DayOfWeek import DayOfWeek

class Event():

    def __init__(self, 
                 course : Course,
                 instructor : Instructor,
                 room : Room, 
                 day : DayOfWeek,
                 hour : int
                 ) -> None:
        self.course = course
        self.instructor = instructor
        self.room = room
        self.day = day
        self.hour = hour