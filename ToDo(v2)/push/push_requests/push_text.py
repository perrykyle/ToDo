import pandas as pd
import random as r


def push_text(client):
    freq_list = [5, 4, 2, 1]
    # amount pulled from lists in L->R order (crucial, high, medium, low)

    for list_ in client.get_lists():
        if "Text Today" in list_.displayName:
            id_ = list_.list_id
    # gets list id for "Text Today"

    df = pd.read_excel('C:/Users/kylep/Desktop/PyCharm Projects/ToDo(v2)/references/names.xlsx')
    txt_list = []
    # established return list

    for x in range(4):
        # for x in range 4

        temp = df[df.columns[x]].values.tolist()
        ret = [element for element in temp if str(element) != "nan"]
        # takes a list of each column without NaN

        for y in range(freq_list[x]):
            # for each element in the list

            name = r.choice(ret)
            while name in txt_list:
                name = r.choice(ret)
            txt_list.append(name)
            # append a unique name that isn't in the list yet

    for person in txt_list:
        client.create_task(title='Text ' + person + ' Today', list_id=id_)
    # creates each task in 'Text Today'
