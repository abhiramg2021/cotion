import sys
import json
from datetime import datetime


def parse_flags() -> dict:
    """Parse the flags from the command line"""
    computer, force = False, False
    if "--computer" in sys.argv:
        computer = True
    if "--force" in sys.argv:
        force = True

    return {"computer": computer, "force": force}


def parse_config_file() -> dict:
    """Parse the config file"""
    with open("config.json", "r") as file:
        config = json.load(file)
    return config


def should_run_script(force_flag: bool, last_run_date_str: str) -> bool:
    """Checks conditions to determine if the script should run.
    Conditions
    - The --force flag is set
    - The script hasn't been run today, by default, the last_run_date is set to 01/01/2000
    """

    # If --force flag is provided, allow the script to run
    if force_flag:
        print("Cotion has been forced to run.")
        return True

    # Check For Timestamp
    last_run_date = datetime.strptime(last_run_date_str, "%Y-%m-%d").date()
    current_date = datetime.now().date()

    run = last_run_date != current_date

    if run:
        print(f"Cotion was last run: {last_run_date}. Running Cotion.")
    return run


def update_timestamp(config: dict):
    """Update the timestamp file with the current date."""
    current_date = datetime.now().date()
    config["LAST_RUN_DATE"] = current_date.strftime("%Y-%m-%d")
    with open("config.json", "w") as file:
        json.dump(config, file)
