def clear_display(client):
    keywords = ['Tasks', 'Tomorrow', "Assignments", "Text Today"]
    # keywords to select lists "New Tasks" "Tasks" "Text Today" and "Tomorrow"
    for list_ in client.get_lists():
        # for each list

        for keyword in keywords:
            # for each keyword

            if keyword in list_.displayName:
                # if a given keyword is a substring of the list name

                for task in client.get_tasks(list_id=list_.list_id):
                    # for every client in the given list

                    client.delete_task(task_id=task.task_id, list_id=list_.list_id)
                    # delete that task
