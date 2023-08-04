import pandas as pd
from datetime import datetime, timedelta


def push_to_display(client):
    today = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59, 59)
    tomorrow = today + timedelta(days=1)
    # establish proper date-times for today and tomorrow

    df = pd.read_excel('C:/Users/kylep/Desktop/PyCharm Projects/ToDo(v2)/references/master.xlsx')
    # gets master df

    for list_ in client.get_lists():
        if 'Tasks' in list_.displayName:
            tasks_id = list_.list_id
            break
    # gets tasks ID

    for list_ in client.get_lists():
        if 'Tomorrow' in list_.displayName:
            tomorrow_id = list_.list_id
            break
    # gets tomorrow ID

    for index, row in df.iterrows():
        body = ''
        if str(row['body']) != 'nan':
            body = row['body']
        # replaces nan with nothing

        time = str(row['due_date'].strftime("%I:%M %p"))
        # formats time in 12-hour format


        if row['due_date'] <= today:
            # if the due date is less than the last second of the day

            client.create_task(title=row['title'] + " - " + time, due_date=row['due_date'], body_text=body, list_id=tasks_id)
            # creates task under tasks
        elif row['due_date'] <= tomorrow:
            # if the due date is tomorrow

            client.create_task(title=row['title'] + " - " + time, due_date=row['due_date'], body_text=body, list_id=tomorrow_id)
            # creates task under tomorrow
