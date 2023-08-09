from pymstodo import ToDoConnection
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os
import ast
import uuid


def establish_connection():
    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    token = ast.literal_eval(os.getenv("TOKEN"))

    return ToDoConnection(client_id=client_id, client_secret=client_secret, token=token)


# Turns datetime string into EST from UTC, in correct format
def convert_to_est(utc_string):
    utc_time = datetime.strptime(utc_string, '%Y-%m-%d %H:%M:%S')
    est_time = utc_time.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-4)))
    formatted_est_time = est_time.strftime('%H:%M-%Y-%m-%d')
    return formatted_est_time


# Pulls new tasks from task list, deletes them and then adds them to upcoming_tasks.txt
def pull_new_tasks(client):
    task_list = []

    # Finds list with "new tasks" in the name
    for list in client.get_lists():
        if "new tasks" in str(list.displayName).lower():

            # Pulls new tasks into tasks
            tasks = client.get_tasks(list.list_id)

            # Deletes every task
            for task in tasks:
                client.delete_task(task_id=task.task_id, list_id=list.list_id)
                task_list.append({"name": task.title,
                                  "due_date": convert_to_est(str(task.due_date)),
                                  "body": task.body_text})

    # Returns the task list
    ### CHANGE THIS TO AUTOMATICALLY ADD TO UPCOMING_TASKS
    return task_list


# Organizes functions
if __name__ == "__main__":
    client = establish_connection()
    new_tasks = pull_new_tasks(client)
