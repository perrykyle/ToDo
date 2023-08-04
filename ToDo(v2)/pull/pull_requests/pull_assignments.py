import requests
from datetime import datetime, timedelta
import pandas as pd


def fix_date(date):
    if date is None:
        date = '2023-05-31T11:59:59Z'
    return datetime.strptime(str(date), "%Y-%m-%dT%H:%M:%SZ") - timedelta(hours=5)
    # returns datetime value of the due date, accounted for EST


def pull_assignments():
    api_key = '13092~hi5R6YNYac0iwIbaTRngHu6ktSf4lsMv1MCSsQCBMzW0Gd9zqQ1VnlDvucbN3udq'
    # my Canvas API key

    course_ids = {
        'CMSC475': 74903,
        'CMSC312': 70841,
        'CMSC425': 69797,
        'CMSC440': 73911,
        'CMSC452': 74547,
        'ENGR395': 72831
    }
    # Classes and their respective ID's

    task_dict = {
        'title': [],
        'due_date': [],
        'body': []
    }
    # creates the dictionary for the dataframe

    for course, cid in course_ids.items():
        url = f'https://virginiacommonwealth.instructure.com//api/v1/courses/{cid}/assignments'
        # creates the request url for each class

        response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'}).json()
        # get request for each class

        for task in response:
            due_date = fix_date(task['due_at'])
            # grabs the due date in DateTime format

            if due_date > datetime.now():
                task_dict['title'].append(task['name'])
                task_dict['due_date'].append(due_date)
                task_dict['body'].append(course)
            # only adds to the dictionary if the assignments aren't passed due

    df = pd.DataFrame.from_dict(task_dict).sort_values(by=['due_date'])
    df.to_excel('C:/Users/kylep/Desktop/PyCharm Projects/ToDo(v2)/references/assignments.xlsx', index=False)
    # puts to assignments excel


if __name__ == '__main__':
    pull_assignments()