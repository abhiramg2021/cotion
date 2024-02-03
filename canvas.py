from canvasapi import Canvas
from assignment import Assignment


class CanvasAPIClient:
    """A class that reads assignments in a class using the Canvas API

    Members:
    canvas: Canvas - the Canvas API client
    assignments: set - a set of assignments}
    """

    def __init__(self, domain: str, token: str) -> None:
        self.canvas = Canvas(domain, token)
        self.assignments = list()

    def read_assignments_for_course(self, course_id: int, course_name: str) -> None:
        """Given a course_id, get the assignments for that course using the Canvas API, and add them to self.assignments"""

        canvas_assignments = self.canvas.get_course(int(course_id)).get_assignments()

        for ass in canvas_assignments:
            name = ass.__getattribute__("name")

            due = (
                str(ass.__getattribute__("due_at"))[:10]
                if ass.__getattribute__("due_at")
                else None
            )

            self.assignments.append(Assignment(name, due, course_name))
