import pandas as pd
from datetime import datetime


def clear_old_master():
    df_master = pd.read_excel('C:/Users/kylep/Desktop/PyCharm Projects/ToDo(v2)/references/master.xlsx')
    # pulls the dataframe from the master excel file

    pull_df = {
        'title': [],
        'due_date': [],
        'body': []
    }
    # prepares the dataframe dictionary

    for index, row in df_master.iterrows():
        if row['due_date'] >= datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0):
            # if the due date is in the future

            pull_df['title'].append(row['title'])
            pull_df['due_date'].append(row['due_date'])
            pull_df['body'].append(row['body'])
            # add to dataframe dictionary

    pd.DataFrame.from_dict(pull_df).sort_values(by=['due_date']).to_excel('C:/Users/kylep/Desktop/PyCharm Projects/ToDo(v2)/references/master.xlsx', index=False)
    # adds to master, sorted by due date, no index
