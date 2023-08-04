import pandas as pd


def push_assignments(client):
    df = pd.read_excel('C:/Users/kylep/Desktop/PyCharm Projects/ToDo(v2)/references/assignments.xlsx')
    # gets the assignments dataframe

    for list_ in client.get_lists():
        # for every list

        if "Assignments" in list_.displayName:
            id_ = list_.list_id
            # mark id for assignments list

    for index, row in df.iterrows():
        time = str(row['due_date'].strftime("%I:%M %p"))
        # format into 12-hour format

        client.create_task(title=row['title'] + " - " + time, due_date=row['due_date'], body_text=row['body'], list_id=id_)
        # creates the task
