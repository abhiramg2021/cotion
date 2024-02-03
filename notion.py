from notion_client import Client
from assignment import Assignment


class NotionDatabaseClient:
    """A class that uses the Notion API to interact with my Notion database

    Note:
    This code depends on the specified database having these 3 specific columns:
        Title : (Name)
        Due : (Date)
        Topic : (Select)
    """

    def __init__(self, token: str, database_id: str):
        self.notion = Client(auth=token)
        self.database_id = database_id
        self.assignments = dict()

    def read_assignments(self) -> None:
        """Use the Notion API to load in assignments from my Notion database"""
        # Notion API queries only return 100 objects at a time, and point to the next set of objects to retrieve using a "start_cursor"
        start_cursor = None

        # Start cursor will be empty on the first iteration, so we address this edge case.
        is_first_iteration = True

        while start_cursor != None or is_first_iteration:

            is_first_iteration = False
            results = self.notion.databases.query(
                self.database_id, start_cursor=start_cursor
            )

            start_cursor = results["next_cursor"]
            notion_assignments = results["results"]

            for notion_assignment in notion_assignments:

                title, due, topic, _id = None, None, None, None

                # Do not parse any assignments that do not have a title
                if len(notion_assignment["properties"]["Name"]["title"]) == 0:
                    continue
                else:
                    title = notion_assignment["properties"]["Name"]["title"][0]["text"][
                        "content"
                    ]

                if notion_assignment["properties"]["Due"]["date"]:
                    due = notion_assignment["properties"]["Due"]["date"]["start"]

                if notion_assignment["properties"]["Topic"]["select"]:
                    topic = notion_assignment["properties"]["Topic"]["select"]["name"]

                _id = notion_assignment["id"]

                assignment = Assignment(title, due, topic, _id)

                self.assignments[assignment] = assignment

    def add_new_assignment(self, assignment: Assignment) -> None:
        """Add a new assignment to the Notion database"""
        print(
            assignment.course_name,
            "New Assignment:",
            assignment.name,
            "due:",
            assignment.due,
        )
        data = {
            "Topic": {
                "type": "select",
                "select": {
                    "name": assignment.course_name,
                },
            },
            "Name": {
                "type": "title",
                "title": [{"text": {"content": assignment.name}}],
            },
        }

        if assignment.due:
            data["Due"] = {"type": "date", "date": {"start": assignment.due}}

        self.notion.pages.create(
            parent={"database_id": self.database_id}, properties=data
        )

    def update_assignment(self, page_id: str, assignment: Assignment) -> None:
        """Update an existing assignment in the notion database"""
        print(
            assignment.course_name,
            "Update Assignment:",
            assignment.name,
            "due:",
            assignment.due,
        )
        page_id_to_update = page_id

        data = {
            "Topic": {
                "type": "select",
                "select": {
                    "name": assignment.course_name,
                },
            },
            "Name": {
                "type": "title",
                "title": [{"text": {"content": assignment.name}}],
            },
            "Due": {"type": "date", "date": {"start": assignment.due}},
        }

        self.notion.pages.update(page_id=page_id_to_update, properties=data)
