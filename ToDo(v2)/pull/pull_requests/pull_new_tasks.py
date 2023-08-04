import warnings
from datetime import timedelta
import pandas as pd


def pull_new_tasks(client):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    # warning filter

    for list_ in client.get_lists():
        if 'New Tasks' in list_.displayName:
            id_new_tasks = list_.list_id
        if 'Long Term' in list_.displayName:
            id_long_term = list_.list_id
    # Grabs the list ids for new tasks and long term

    task_dict = {
        'title': [],
        'due_date': [],
        'body': []
    }
    # creates the dictionary for the dataframe

    for task in client.get_tasks(id_new_tasks):
        if task.due_date is None:
            client.create_task(list_id=id_long_term, title=task.title, body_text=task.body_text)
        # if there is no due date, adds to long term list

        else:
            task_dict['title'].append(task.title)
            task_dict['due_date'].append(task.due_date - timedelta(hours=5))
            task_dict['body'].append(task.body_text)
        # if there is a due date, adds to the dictionary and accounts for UTC to EST

        client.delete_task(task_id=task.task_id, list_id=id_new_tasks)
        # deletes each task upon iteration after it has been registered and processed

    df_append = pd.DataFrame.from_dict(task_dict)
    # creates a dataframe from the dictionary

    df_master = pd.read_excel('C:/Users/kylep/Desktop/PyCharm Projects/ToDo(v2)/references/master.xlsx')
    df_master.append(df_append).sort_values(by=['due_date']).to_excel(
        'C:/Users/kylep/Desktop/PyCharm Projects/ToDo(v2)/references/master.xlsx', index=False)
    # grabs the master task lists and adds these routines to it, adding it back to the Excel file
