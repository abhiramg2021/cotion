class Assignment:
    """A class that represents an assignment"""

    def __init__(
        self, name: str, due: str, course_name: str, assignment_id: str = ""
    ) -> None:
        self.name = name
        self.due = due
        self.course_name = course_name
        self.assignment_id = assignment_id

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Assignment):
            return self.name == other.name and self.course_name == self.course_name

        return False

    def __hash__(self) -> int:
        return hash((self.name, self.due, self.course_name))

    def __str__(self) -> str:
        return f"Course: {self.course_name}, Name: {self.name}, Due: {self.due}"
