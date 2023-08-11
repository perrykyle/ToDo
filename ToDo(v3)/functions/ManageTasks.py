from pymstodo import ToDoConnection
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os
import ast
import uuid

# Dictionary mapping day numbers to their string names
days_of_week = {
    "0": "Sun",
    "1": "Mon",
    "2": "Tue",
    "3": "Wed",
    "4": "Thu",
    "5": "Fri",
    "6": "Sat"
}


# Tasks class
class WeeklyTasks:
    """Class to represent a Task"""

    def __init__(self, id, name, time, days, description=''):
        self.id = id
        self.name = name
        self.time = time
        self.days = days
        self.description = description


# Upcoming Tasks class
class UpcomingTasks:
    """Class to represent an Upcoming Task"""

    def __init__(self, id, name, datetime, description):
        self.id = id
        self.name = name
        self.datetime = datetime
        self.description = description


# Uniform tasks which can be pushed to Microsoft to do
class UniTasks:
    """Class which handles conversions to uniform tasks"""

    def __init__(self, name, time, description):
        self.name = name,
        self.time = time,
        self.description = description


# Establishes connection based on the parameters in the environment
def establish_connection():
    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    token = ast.literal_eval(os.getenv("TOKEN"))

    return ToDoConnection(client_id=client_id, client_secret=client_secret, token=token)


# Ensures that the guaranteed lists exist to display information
def guarantee_lists(client):
    todo_lists = client.get_lists()

    req_lists = {
        'tomorrow': False,
        'new task list': False
    }
    # for every existing list in microsoft to do
    for todo_list in todo_lists:

        # for every required list from me
        for req_list_name in list(req_lists.keys()):

            # if there is a list that matches my desired list, marks true
            if req_list_name in todo_list.displayName.lower():
                req_lists[req_list_name] = True

    # if there is a missing task list, create new tasklist
    for task, status in req_lists.items():
        if not status:
            client.create_list(task.title())


# Turns datetime string into EST from UTC, in correct format
def convert_to_est(utc_string):
    if utc_string != 'None':
        utc_time = datetime.strptime(utc_string, '%Y-%m-%d %H:%M:%S')
        est_time = utc_time.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-4)))
        formatted_est_time = est_time.strftime('%H:%M-%Y-%m-%d')
        return formatted_est_time
    else:
        # Marks for delete if there is no date or time
        ### You can have a task with no time but a date is necessary
        return 'Delete'


# Appends upcoming tasks to upcoming_tasks.txt
def append_to_file(tasks):
    with open('../references/upcoming_tasks.txt', 'a') as file:
        for task in tasks:
            if task["due_date"] != 'Delete':
                line = f'{uuid.uuid4()},{task["name"]},{task["due_date"]},{task["body"]}\n'
                file.write(line)


# Pulls new tasks from task list, deletes them and then adds them to upcoming_tasks.txt
def add_new_tasks(client):
    task_list = []

    # Finds list with "new tasks" in the name
    for list in client.get_lists():
        if "new task list" in str(list.displayName).lower():

            # Pulls new tasks into tasks
            tasks = client.get_tasks(list.list_id)

            # Deletes every task
            for task in tasks:
                client.delete_task(task_id=task.task_id, list_id=list.list_id)
                task_list.append({"name": task.title.replace(',', '-'),
                                  "due_date": convert_to_est(str(task.due_date)),
                                  "body": task.body_text.replace(',', '-')})

    # Returns the task list
    if task_list:
        append_to_file(task_list)
    return task_list


# Pulls the tasks from the text file, removes any tasks that are expired
# then sorts them in order of upcoming to later on
# Also deletes all tasks in "Tomorrow" and in "Tasks"
def sort_and_remove_past_tasks(client):
    file_path = '../references/upcoming_tasks.txt'
    current_datetime = datetime.now()
    midnight_today = datetime(current_datetime.year, current_datetime.month, current_datetime.day)

    # Read the tasks
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Parse and filter the tasks, then sort
    filtered_tasks = [line for line in lines if
                      datetime.strptime(line.split(',')[2], '%H:%M-%Y-%m-%d') >= midnight_today]
    sorted_tasks = sorted(filtered_tasks, key=lambda line: datetime.strptime(line.split(',')[2], '%H:%M-%Y-%m-%d'))

    # Write the sorted and filtered tasks
    with open(file_path, 'w') as file:
        file.writelines(sorted_tasks)

    # Initialize array for holding list id's we want to clear
    rem_list_ids = []
    todo_lists = client.get_lists()
    # for each list in to do lists
    for todo_list in todo_lists:

        # if tasks or tomorrow exist in a list name
        list_name = todo_list.displayName.lower()
        if 'tasks' in list_name or 'tomorrow' in list_name:
            # add the list id to the list ids
            rem_list_ids.append(todo_list.list_id)

    # for each list id
    for list_id in rem_list_ids:

        # for each task in each lists tasks
        for list_task in client.get_tasks(list_id):
            # delete the task
            client.delete_task(list_task.task_id, list_id)


# Pulls tasks from tasks.txt
def read_weekly_tasks_from_file():
    tasks_list = []

    with open('../references/tasks.txt', 'r') as file:
        for line in file:
            task_data = line.strip().split(',')
            task = WeeklyTasks(*task_data)
            tasks_list.append(task)

    return tasks_list


# Pulls tasks from upcoming_tasks.txt
def read_upcoming_tasks_from_file():
    upcoming_tasks_list = []

    with open('../references/upcoming_tasks.txt', 'r') as file:
        for line in file:
            task_data = line.strip().split(',')
            task = UpcomingTasks(*task_data)
            upcoming_tasks_list.append(task)

    return upcoming_tasks_list


# DEBUG function to print a list of UniTasks
def print_unitasks(task_list):
    for task in task_list:
        print(f"Name: {task.name}, Time: {task.time}, Description: {task.description}")


# Posts the UniTask lists to Microsoft To Do
def post_unilist(client, tasks, key, deltaval):
    # Pulls lists
    todo_lists = client.get_lists()

    # if the key provided matches the list (tasks or tomorrow)
    for todo_list in todo_lists:
        if key in todo_list.displayName.lower():
            list_id = todo_list.list_id

    # adds each task to the to do
    for task in tasks:
        title = str(task.time).replace("'", "").replace("(", "").replace(")", "").replace(",", "") + " - " + str(task.name).replace("'", "").replace("(", "").replace(")", "").replace(",", "")
        client.create_task(title=title,
                           body_text=task.description,
                           list_id=list_id,

                           # Due date will either say "Today" or "Tomorrow" depending on deltaval
                           due_date=datetime(year=datetime.now().year, month=datetime.now().month, day=(datetime.now() + timedelta(days=deltaval)).day))


# Populate the tasks and tomorrow lists with the upcoming tasks. Order them appropriately
def populate_lists(client):
    # Pulls tasks from both files
    weekly_tasks = read_weekly_tasks_from_file()
    upcoming_tasks = read_upcoming_tasks_from_file()

    # Today's and Tomorrow's dates in string representation
    today_date = str(datetime.now().date())
    tomorrow_date = str(datetime.now().date() + timedelta(days=1))

    # Gets today's weekday representation from datetime
    today = (datetime.now().weekday() + 1) % 7
    tomorrow = (today + 1) % 7

    # Initialize today and tomorrow task lists
    today_tasks = []
    tomorrow_tasks = []

    # For each weekly task, add to tasks list depending on if it falls on today or tomorrow's day
    for weekly_task in weekly_tasks:
        if str(today) in weekly_task.days:
            today_tasks.append(UniTasks(weekly_task.name, weekly_task.time, weekly_task.description))
        if str(tomorrow) in weekly_task.days:
            tomorrow_tasks.append(UniTasks(weekly_task.name, weekly_task.time, weekly_task.description))

    # For each upcoming task, add it to the tasks list if the dates fall on either today or tomorrow's day
    for upcoming_task in upcoming_tasks:

        # Separates time and date from values
        time = str(upcoming_task.datetime.split('-')[0])
        date = str('-'.join(upcoming_task.datetime.split('-')[1:]))

        # For each upcoming task, add it to the list of tasks if it falls on the correct date
        if date == today_date:
            today_tasks.append(UniTasks(upcoming_task.name, time, upcoming_task.description))
        if date == tomorrow_date:
            tomorrow_tasks.append(UniTasks(upcoming_task.name, time, upcoming_task.description))

    # Sorts tasks based on time
    today_tasks = sorted(today_tasks, key=lambda x: x.time)
    tomorrow_tasks = sorted(tomorrow_tasks, key=lambda x: x.time)

    # Uploads the lists
    post_unilist(client, today_tasks, "tasks", 0)
    post_unilist(client, tomorrow_tasks, "tomorrow", 1)


# Organizes functions
if __name__ == "__main__":
    # Firstly, we establish the connection to the client using the values in the environment
    client = establish_connection()

    # Then, we guarantee that "New Tasks" and "Tomorrow" lists exist, as necessary for the program
    guarantee_lists(client)

    # Then, we take the new tasks in the "New Tasks" list, and then add them to the "upcoming_tasks.txt" file
    # We also remove the tasks from the "New Tasks" list in Microsoft To Do, opting to store them locally
    new_tasks = add_new_tasks(client)

    # Next, we analyze every single task in "upcoming_tasks.txt", check to see if they are expired (prior to today)
    # If expired, we remove them from the file. Then, we sort the remaining tasks in soonest to latest order
    # Then, we locate the "Tasks" and "Tomorrow" lists and remove everything from them
    sort_and_remove_past_tasks(client)

    # Finally, we populate the "Tasks" and "Tomorrow" lists with the data from "tasks.txt" and "upcoming_tasks.txt"
    populate_lists(client)
