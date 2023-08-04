import clear.clear_requests.clear_display as clear_display
import clear.clear_requests.clear_old_master as clear_old_master


def clear(client):
    clear_display.clear_display(client=client)
    clear_old_master.clear_old_master()
