import pull.pull_requests.pull_routine as pull_routine
import pull.pull_requests.pull_new_tasks as pull_new_tasks
import pull.pull_requests.pull_assignments as pull_assignments


def pull(client):
    pull_routine.pull_routine()
    pull_new_tasks.pull_new_tasks(client)
    pull_assignments.pull_assignments()