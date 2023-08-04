import pandas as pd
from datetime import datetime, timedelta
import warnings


def date_time_to_datetime(time):
    date = datetime.now() + timedelta(days=1)
    # grabs the date

    time = datetime.strptime(str(time), '%H:%M:%S')
    time = datetime(year=date.year, month=date.month, day=date.day, hour=time.hour, minute=time.minute)
    # sets the time to the proper date time
    return time


def pull_routine():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    # warning filter

    df = pd.read_excel('C:/Users/kylep/Desktop/PyCharm Projects/ToDo(v2)/references/lifestyle.xlsx')
    tasks = []
    # reads the Excel sheet and adds the dataframe, creates list of nested lists 'tasks'

    today = str(datetime.now().weekday())
    tomorrow = str((datetime.now() + timedelta(days=1)).weekday())
    # today and tomorrow by number

    for index, row in df.iterrows():
        # for each row

        days_appearing = str(row['Days'])
        if str(row['Desc']) == 'nan':
            body = ''
        else:
            body = str(row['Desc'])
        # setting accurate variables for adding

        if tomorrow in days_appearing:
            due_date = date_time_to_datetime(row['Time'])
            tasks.append([row['Title'], due_date, body])
        # adds task if it falls on tomorrow

    pull_df = {
        'title': [],
        'due_date': [],
        'body': []
    }
    # creates a dictionary with the desired columns

    for task in tasks:
        pull_df['title'].append(task[0])
        pull_df['due_date'].append(task[1])
        pull_df['body'].append(task[2])
    # populates with each task

    df_append = pd.DataFrame.from_dict(pull_df)
    # creates a dataframe from the dictionary

    df_master = pd.read_excel('C:/Users/kylep/Desktop/PyCharm Projects/ToDo(v2)/references/master.xlsx')
    df_master.append(df_append).sort_values(by=['due_date']).to_excel('C:/Users/kylep/Desktop/PyCharm Projects/ToDo(v2)/references/master.xlsx', index=False)
    # grabs the master task lists and adds these routines to it, adding it back to the Excel file and sorting by due date
