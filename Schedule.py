from Event import Event
from Instructor import Instructor

class Schedule():

    def __init__(self, events : list[Event]) -> None:
        self.events = events

    def evalFitness(self) -> int:
        fit = 0.0
        ins : dict[Instructor, int] = {}

        for e in self.events:
            for q in self.events:

                #Check if the two classes are in the same room at the same time
                if e.room == q.room and e.day == q.day and e.hour == q.hour:
                    fit -= 0.5
                
                #Check if an instructor is double booked
                insDoubleBooked = False
                if e.day == q.day and e.hour == q.hour and e.instructor == q.instructor:
                    insDoubleBooked = True
                #Check if an instructor is seqential classes
                elif e.day == q.day and e.hour == (q.hour + 1) and e.instructor == q.instructor:
                    if (e.room.bldg == "ROMAN" and q.room.bldg == "BEACH") or (e.room.bldg == "BEACH" and q.room.bldg == "ROMAN"):
                        fit -= 0.4
                    else:
                        fit += 0.5
                
                #Course specific requirements
                if e.course.name == "SLA101A" and q.course.name == "SLA101B":
                    if e.day == q.day:
                        if e.hour == q.hour:
                            fit -= 0.5
                        elif abs(q.hour - e.hour) > 4:
                            fit += 0.5
                    else:
                        fit += 0.5
                elif e.course.name == "SLA191A" and q.course.name == "SLA191B":
                    if e.day == q.day:
                        if e.hour == q.hour:
                            fit -= 0.5
                        elif abs(q.hour - e.hour) > 4:
                            fit += 0.5
                    else:
                        fit += 0.5
                elif (e.course.name == "SLA101A" or e.course.name == "SLA101B") and (q.course.name == "SLA191A" or q.course.name == "SLA191B"):
                    if e.day == q.day:
                        if abs(e.hour - q.hour) == 1:
                            if (e.room.bldg == "ROMAN" and q.room.bldg == "BEACH") or (e.room.bldg == "BEACH" and q.room.bldg == "ROMAN"):
                                fit -= 0.4
                            else:
                                fit += 0.5
                        elif abs(e.hour - q.hour) == 2:
                            fit += 0.25
                        elif e.hour == q.hour:
                            fit -= 0.25

                if insDoubleBooked:
                    fit -= 0.2
                else:
                    fit += 0.2

            #Check if the room is the right size
            if e.room.capacity < e.course.expectedEnrollment:
                fit -= 0.5
            elif e.room.capacity > (6 * e.course.expectedEnrollment):
                fit -= 0.4
            elif (3 * e.room.capacity) > (3 * e.course.expectedEnrollment):
                fit -= 0.2
            else:
                fit += 0.3

            #Check preference of instructor
            match (e.course.instructorDict[e.instructor]):
                case 1:
                    fit += 0.5
                case 0:
                    fit += 0.2
                case -1:
                    fit -= 0.1
                case _:
                    raise ValueError("Instructor must have a value between -1, and 1")
                
            #Count the number of classes each instructor has
            if e.instructor in ins:
                ins[e.instructor] = ins[e.instructor] + 1
            else:
                ins[e.instructor] = 1
        
        for i in ins:
            if ins[i] > 4:
                fit -= 0.5
            elif ins[i] < 2:
                if i.name != "TYLER":
                    fit -= 0.4
        
        return fit
    
    def __str__(self):
        out = "\033[4mTIME     LOC            COURSE  INS     \033[0m\n"
        l = sorted(self.events, key=lambda x : (x.day.value, x.hour, x.room.bldg, x.room.num))
        for e in l:
            partStr = "AM"
            time = e.hour
            if time > 12:
                time -= 12
                partStr = "PM"
            out += f"{e.day.name[:3]} {time:02}{partStr} {e.room.bldg:6} {e.room.num:03}:\t{e.course.name:7}\t{e.instructor.name}\n"
        out += f"FITNESS: {self.evalFitness()}"
        return(out)