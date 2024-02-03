import util
from notion import NotionDatabaseClient
from canvas import CanvasAPIClient

config = util.parse_config_file()
flags = util.parse_flags()

canvas_client = CanvasAPIClient(config["CANVAS"]["DOMAIN"], config["CANVAS"]["TOKEN"])
notion_client = NotionDatabaseClient(
    config["NOTION"]["TOKEN"], config["NOTION"]["DATABASE_ID"]
)

courses = config["COURSES"]


if util.should_run_script(
    force_flag=flags["force"], last_run_date_str=config["LAST_RUN_DATE"]
):

    for course_name, _id in courses.items():
        canvas_client.read_assignments_for_course(_id, course_name)

    notion_client.read_assignments()

    # Update / Add assignments to Notion
    for canvas_assignment in canvas_client.assignments:
        if canvas_assignment not in notion_client.assignments:
            notion_client.add_new_assignment(canvas_assignment)
        else:
            notion_assignment = notion_client.assignments[canvas_assignment]
            if (
                canvas_assignment.due
                != notion_client.assignments[canvas_assignment].due
            ):
                notion_client.update_assignment(canvas_assignment)
    util.update_timestamp(config)
else:
    # Only print this message if the --computer flag is not set
    if not flags["computer"]:
        print("Cotion has already been run today. Use --force to run Cotion anyway.")
