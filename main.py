import todoist
from datetime import datetime

api = todoist.TodoistAPI('')

# todo: get projects and store ID

def get_todays_tasks(email, password):
    """
    Get tasks due on the current utc day
    :return: list of task dicts
    """
    # user = api.user.login(email, password)
    api.user.login(email, password)
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

get_todays_tasks()
