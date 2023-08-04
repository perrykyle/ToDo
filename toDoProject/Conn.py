from datetime import datetime, timedelta
from pymstodo import ToDoConnection
import pandas as pd
import openpyxl
from pytz import timezone
import random
import warnings
import time


def str_to_token(string):
    string = string.strip('{}')
    pairs = string.split(', ')
    new_pairs = [pairs[0], pairs[1] + ", " + pairs[2]]
    for x in range(3, len(pairs)):
        new_pairs.append(pairs[x])
    pairs = new_pairs
    keyval = []
    for x in range(len(pairs)):
        keyval.append(pairs[x].replace("'", "").split(": "))
    remList = [1, 2, 3, 7]
    intList = [2, 3]
    floatList = [7]
    newDict = {}
    for x in range(len(keyval)):
        key = keyval[x][0]
        val = keyval[x][1]
        if x in remList:
            val = val.replace("'", "")
            val = val.replace("}", "")
        if x in intList:
            val = int(val)
        if x in floatList:
            val = float(val)
        newDict[key] = val
    tempList = ['openid', 'Tasks.ReadWrite']
    newDict['scope'] = tempList
    return newDict
# Turns token from notepad into proper dictionary containing accurate types


def establish():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    f = open('C:/Users/kylep/Desktop/PyCharm Projects/toDoProject/references/token.txt', 'r')
    lines = f.readlines()
    client_id = lines[0]
    client_secret = lines[1]
    token = str_to_token(lines[2])
    f.close()
    return ToDoConnection(client_id=client_id, client_secret=client_secret, token=token)
# Returns an established connection to the client


def update_lists(client):
    lists = client.get_lists()
    ids = []
    names = []
    for list in lists:
        ids.append(list.list_id)
        names.append(list.displayName)
    df = {
        'List Name': names,
        'ID': ids
    }
    df = pd.DataFrame(df)
    df.to_excel('C:/Users/kylep/Desktop/PyCharm Projects/toDoProject/references/lists.xlsx')
# Updates the lists on Microsoft To-Do in the Excel sheet, along with their ID's
#### Only Run when necessary ####


def get_lists():
    df = pd.read_excel('C:/Users/kylep/Desktop/PyCharm Projects/toDoProject/references/lists.xlsx')
    lists = df['List Name'].values.tolist()
    ids = df['ID'].values.tolist()
    return {lists[i]: ids[i] for i in range(len(lists))}
# Retrieves a dictionary containing all the existing lists in the Excel


def get_list_id(keyword):
    lists = get_lists()
    for l in lists:
        if keyword in l:
            return lists[l]
# Returns the ID of a list containing a given Substring


def get_tasks(list_keyword, client):
    l = get_list_id(list_keyword)
    return client.get_tasks(l)
# Returns a list of all tasks in a list
# Uses todo_client and a substring of the desired list


def push_tomorrow_tasks(test_date):
    df = pd.read_excel('C:/Users/kylep/Desktop/PyCharm Projects/toDoProject/references/lifestyle.xlsx')
    titles = []
    times = []
    bodies = []

    today = datetime.now().weekday()

    tomorrow = datetime.now() + timedelta(test_date)
    ##### ENTER WHICH DAYS YOU WISH TO ENTER IN HERE #####
    ####                USE TIMEDELTA                 ####

    tomorrow_day = tomorrow.weekday()

    for index, row in df.iterrows():
        # title[0] - days[1] - time[2] - desc[3]

        if str(row[3]) == 'nan':
            row[3] = ''

        if str(tomorrow_day) in str(row[1]):
            titles.append(row[0])
            times.append(form_datetime_to_str(str(tomorrow), str(row[2])))
            bodies.append(row[3])

    df = pd.read_excel('C:/Users/kylep/Desktop/PyCharm Projects/toDoProject/references/master.xlsx')
    xtra = {
        'title': titles,
        'due_date': times,
        'body': bodies
    }
    df = df.append(pd.DataFrame(xtra))
    df.to_excel('C:/Users/kylep/Desktop/PyCharm Projects/toDoProject/references/master.xlsx', index=False)
# Pushes the tasks for tomorrow into the master excel
# Pulled from "lifestyle.xlsx"
# If I want to update my daily routine I would go to that file and edit there


def form_datetime_to_str(day, time):
    time = time.split(":")
    hour = int(time[0])
    minute = int(time[1])
    day = day.split(" ")
    day = day[0].split("-")
    year = int(day[0])
    month = int(day[1])
    day = int(day[2])

    due_date = datetime(year, month, day, hour, minute)
    return due_date
# Takes a given date and time from excel formatting and turns it into a datetime value
# This value is pushed to the Excel


def day_conv():
    return {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
# Day conversions, for reference


def dump_old_master():
    df = pd.read_excel('C:/Users/kylep/Desktop/PyCharm Projects/toDoProject/references/master.xlsx')

    today = datetime(datetime.now().year, datetime.now().month, datetime.now().day)

    g_title = []
    g_due_date = []
    g_body = []

    for index, row in df.iterrows():
        if row['due_date'] >= today:
            g_title.append(row['title'])
            g_due_date.append(row['due_date'])
            g_body.append(row['body'])

    new_df = {
        'title': g_title,
        'due_date': g_due_date,
        'body': g_body
    }

    pd.DataFrame(new_df).to_excel('C:/Users/kylep/Desktop/PyCharm Projects/toDoProject/references/master.xlsx', index=False)
# Dumps every event that is before today's date


def dump_master():
    df = {
        'title': [],
        'due_date': [],
        'body': []
    }
    pd.DataFrame(df).to_excel('C:/Users/kylep/Desktop/PyCharm Projects/toDoProject/references/master.xlsx', index=False)
# Dumps the entire master, debugging use


def cut_new_tasks(client):
    tasks = client.get_tasks(get_list_id("New Tasks"))

    title = []
    due_date = []
    body = []

    ids = []

    for task in tasks:

        ids.append(task.task_id)

        if task.due_date is None:
            client.create_task(task.title, get_list_id("Long Term"))

        else:
            title.append(task.title)
            due_date.append(str(task.due_date-timedelta(hours=5)))
            body.append(str(task.body_text).strip())

    df = pd.read_excel('C:/Users/kylep/Desktop/PyCharm Projects/toDoProject/references/master.xlsx')
    xtra = {
        'title': title,
        'due_date': due_date,
        'body': body
    }

    df = df.append(pd.DataFrame(xtra))
    df.to_excel('C:/Users/kylep/Desktop/PyCharm Projects/toDoProject/references/master.xlsx', index=False)

    empty_list("New Tasks", client)
# Takes every task with a due date in "New Tasks" and adds it to the master Excel with proper formatting.
# If there is no due date it adds it to "Long Term" per description
# Deletes every single task afterwards


def empty_list(keyword, client):
    lid = get_list_id(keyword)
    tasks = client.get_tasks(lid)
    ids = []
    for task in tasks:
        ids.append(task.task_id)
    for id in ids:
        client.delete_task(id, lid)
# Removes all the contents of a list with a given Keyword


def push_master(client):
    df = pd.read_excel('C:/Users/kylep/Desktop/PyCharm Projects/toDoProject/references/master.xlsx')
    df = df.sort_values(by=['due_date'])

    today = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59, 59)
    tomorrow = today + timedelta(1)

    for index, row in df.iterrows():
        if row['due_date'] < today:
            create_task(client, str(row['title']), (row['due_date']), str(row['body']), 'Tasks')
        elif row['due_date'] < tomorrow:
            create_task(client, str(row['title']), (row['due_date']), str(row['body']), 'Tomorrow')


def create_task(client, title, due_date, body, keyword):
    if body == 'nan':
        body = ''
    client.create_task(title=title + " - " + form_time(due_date), due_date=due_date, body_text=body, list_id=get_list_id(keyword))


def form_time(dt):
    return str(dt.strftime("%I:%M %p"))


def reset(client):
    dump_master()
    empty_list("Tasks", client)
    empty_list("Tomorrow", client)
    prep()


def push(client):
    push_tomorrow_tasks(1)
    # Adds tomorrow's tasks to the master

    cut_new_tasks(todo_client)
    # Adds New Tasks to the master
    # Also Empties "New Tasks"

    empty_list("Tasks", todo_client)
    empty_list("Tomorrow", todo_client)
    # Empties the lists

    dump_old_master()
    # Dumps the tasks which have passed

    push_master(todo_client)
    # Pushes Master to the To-Do client


def prep():
    push_tomorrow_tasks(-1)
    push_tomorrow_tasks(0)
    # Adds yesterday's and todays tasks for debugging



if __name__ == '__main__':
    todo_client = establish()
    # Establishes connection

    # reset(todo_client)
    # populate(todo_client)
    ##### DEBUGGING ONLY #####

    push(todo_client)