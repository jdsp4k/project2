from Instructor import Instructor

class Course():

    def __init__(self,
                 name : str,
                 expectedEnrollment : int,
                 instructorPref : tuple[str],
                 instructorAlt : tuple[str],
                 instructors : tuple[Instructor],
                 ) -> None:
        self.name = name
        self.instructorDict : dict[Instructor, int] = {}
        for i in instructors:
            if i in instructorPref:
                self.instructorDict[i] = 1
            elif i in instructorAlt:
                self.instructorDict[i] = 0
            else:
                self.instructorDict[i] = -1
        self.expectedEnrollment = expectedEnrollment