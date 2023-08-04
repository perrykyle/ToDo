import push.push_requests.push_assignments as push_assignments
import push.push_requests.push_to_display as push_to_display
import push.push_requests.push_text as push_text


def push(client):
    push_assignments.push_assignments(client)
    push_to_display.push_to_display(client)
    push_text.push_text(client)
