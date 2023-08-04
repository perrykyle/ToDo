# call get_token.py (if necessary)

# call run.py
#   establish()

#   call pull.py
#       pull_assignments.py to references/assignments.xlsx
#       pull_new_tasks.py to references/master.xlsx
#       pull_routine.py to references/master.xlsx

#   call clear.py
#       call clear_old_master.py clears all the passed tasks
#       call clear_display.py clears the ToDo Display

#   call push.py
#       push_assignment.py directly to assignments from client
#       push_to_display.py pushes everything from the master that needs to be pushes to the display

### NOTES ###

# Object orient whatever you can.
# Functions in python scripts that require a connection should be provided from "run.py"
# Long term and Assignments never get deleted
# Assignments are seperated from "Tomorrow" and "Tasks"
# Academic Explorations is manually handles and separate from assignments, more like personal interests
# Tomorrow will always hold the routine and classes for the following day, along with any previously added tasks

import pull.pull as pull
import clear.clear as clear
import push.push as push
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
    # establishes the client

    pull.pull(client=client)
    clear.clear(client=client)
    push.push(client=client)
