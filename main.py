from dotenv import load_dotenv
import os
import datetime
import sys

from notion_client import Client
from canvasapi import Canvas

load_dotenv()
notion_auth = os.getenv("NOTION_AUTH")

notion = Client(auth=notion_auth)
database_id = os.getenv("DATABASE_ID")


canvas_token = os.getenv("CANVAS_TOKEN")
domain = os.getenv("CANVAS_DOMAIN")

courses = {
    "ECE 2031": 355084,
    "CS 7641": 374498,
    "CS 4803": 373008,
    "CS 3630": 380348,
}

canvas_assignments = {}


# Path to the timestamp file
timestamp_file_path = "last_run_timestamp.txt"
computer_flag = "--computer" in sys.argv


def should_run_script():
    # Check if the override flag is set
    force_flag = "--force" in sys.argv

    if force_flag:
        print("Cotion has been forced to run.")
        return True  # If --force flag is provided, allow the script to run

    # Check if the timestamp file exists
    if os.path.exists(timestamp_file_path):
        # Read the last run timestamp from the file
        with open(timestamp_file_path, "r") as file:
            last_run_date_str = file.read().strip()

        # Convert the last run timestamp to a datetime object
        last_run_date = datetime.datetime.strptime(last_run_date_str, "%Y-%m-%d").date()

        # Get the current date
        current_date = datetime.datetime.now().date()

        # Check if the script was run today
        return last_run_date != current_date
    else:
        print(f"Cotion was last run: {last_run_date}. Running Cotion now.")
        return True  # If the timestamp file doesn't exist, allow the script to run


def update_timestamp_file():
    # Write the current date to the timestamp file
    current_date = datetime.datetime.now().date()
    with open(timestamp_file_path, "w") as file:
        file.write(current_date.strftime("%Y-%m-%d"))


def get_canvas_assignments(domain, canvas_token, course_id):
    """query the canvas api and return the current assignments as a list"""

    try:

        canvas = Canvas(domain, canvas_token)
        assignments = canvas.get_course(int(course_id)).get_assignments()
        out = []

        for ass in assignments:
            out.append(
                {
                    "name": ass.__getattribute__("name"),
                    "due": str(ass.__getattribute__("due_at"))[:10],
                }
            )
        return out
    except Exception as e:
        ex = str(type(e))

        if "Unauthorized" in ex:
            message = "Unauthorized Class Access"
        elif "InvalidAccessToken" in ex:
            message = "Invalid Canvas Token"
        else:
            print(e.__class__, str(e), e.__traceback__.tb_lineno)
            message = "Try again Later"

        raise Exception(message)


# load notion assignments into a dictionary
def get_notion_assignments(database_id):
    """Use the notion api to load in the entries in the database"""

    start_cursor = None

    first_time = True
    assigments_dict = {}
    while start_cursor != None or first_time:

        first_time = False
        results = notion.databases.query(database_id, start_cursor=start_cursor)

        start_cursor = results["next_cursor"]
        assignments = results["results"]

        for assignment in assignments:

            if len(assignment["properties"]["Name"]["title"]) == 0:
                continue

            title = assignment["properties"]["Name"]["title"][0]["text"]["content"]
            due = (
                assignment["properties"]["Due"]["date"]["start"]
                if assignment["properties"]["Due"]["date"]
                else "None"
            )
            topic = (
                assignment["properties"]["Topic"]["select"]["name"]
                if assignment["properties"]["Topic"]["select"]
                else None
            )

            _id = assignment["id"]

            assigments_dict[f"{title}:{topic}"] = {
                "due": due,
                "topic": topic,
                "title": title,
                "id": _id,
            }
    return assigments_dict


def add_notion_assignment(topic, title, due=None):
    print(topic, "New Assignment:", title, "due:", due)
    data = {
        "Topic": {
            "type": "select",
            "select": {
                "name": topic,
            },
        },
        "Name": {
            "type": "title",
            "title": [{"text": {"content": title}}],
        },
    }

    if due != "None":
        data["Due"] = {"type": "date", "date": {"start": due}}

    notion.pages.create(parent={"database_id": database_id}, properties=data)


def update_notion_assignment(page_id, topic, title, due):
    print(topic, "Update Assignment:", title, "due:", due)
    page_id_to_update = page_id

    try:

        data = {
            "Topic": {
                "type": "select",
                "select": {
                    "name": topic,
                },
            },
            "Name": {
                "type": "title",
                "title": [{"text": {"content": title}}],
            },
        }

        if due != "None":
            data["Due"] = {"type": "date", "date": {"start": due}}

        notion.pages.update(page_id=page_id_to_update, properties=data)

    except Exception as e:
        print("Error:", e)
        pass


if should_run_script():
    for course, _id in courses.items():
        course_assignments = get_canvas_assignments(domain, canvas_token, _id)
        canvas_assignments[course] = course_assignments

    notion_assignments = get_notion_assignments(database_id)

    for course, assignments in canvas_assignments.items():
        for assignment in assignments:
            title = assignment["name"]
            due = assignment["due"]
            topic = course

            assignment_id = f"{title}:{topic}"

            if (
                assignment_id in notion_assignments
                and notion_assignments[assignment_id]["due"] != due
            ):
                print(due, notion_assignments[assignment_id]["due"])
                update_notion_assignment(
                    notion_assignments[assignment_id]["id"], topic, title, due
                )
            elif assignment_id not in notion_assignments:
                add_notion_assignment(topic, title, due)

    update_timestamp_file()
else:
    if not computer_flag:
        # dont print these flags if the computer runs this, and not the user.
        print("Script already ran today. To override, set OVERRIDE_FLAG=true.")
