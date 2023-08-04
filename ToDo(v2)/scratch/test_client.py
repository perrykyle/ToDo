import ast
from pymstodo import ToDoConnection


def establish():
    f = open('C:/Users/kylep/Desktop/PyCharm Projects/ToDo(v2)/references/token.txt')
    # opens the file
    lines = f.readlines()
    # reads the lines
    f.close()
    # closes the file

    client_id = lines[0]
    # first line is the client id
    client_secret = lines[1]
    # second line is the client secret
    token = ast.literal_eval(lines[2])
    # last line is a dictionary of the token, using ast to convert it back to a dictionary

    return ToDoConnection(client_id, client_secret, token)
# returns the newly created connection


if __name__ == "__main__":
    client = establish()
