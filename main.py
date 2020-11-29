import todoist
from datetime import datetime
import json

api = todoist.TodoistAPI('68df7a8351bb221682350ce1f745eb2c86471ac7')
api.reset_state()
response = api.sync()


# todo: get projects and store ID
def get_sync_token():
    store_file = open('store.json', 'r')

    contents = store_file.read()
    store_file.close()

    store = json.loads(contents)

    if 'sync_token' in store:
        return store['sync_token']

    return None


def get_todays_tasks():
    """
    Get tasks due on the current utc day
    :return: list of task dicts
    """
    # user = api.user.login(email, password)
    api.user.login()
    tasks_today = []

    # Sync (load) data
    response = api.sync()

    # Get "today", only keep Day XX Mon, which Todoist uses
    today = datetime.utcnow().strftime("%a %d %b")

    for item in response['items']:
        # item['project_id']
        # item['priority']
        due = item['due_date_utc']

        # todo: only get items from input project
        # todo: only get items with priority
        # todo: demote old task P1

        if due:
            # Slicing :10 gives us the relevant parts
            if due[:10] == today:
                tasks_today.append(item)

    return tasks_today


def get_project(project_name):

    projects = response['projects']

    for p in projects:
        if p['name'] == project_name:
            return p

    return None



project = get_project('PSE Lookup')
if project:
    pass