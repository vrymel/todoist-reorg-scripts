import os
import todoist

api = todoist.TodoistAPI(os.environ.get('TOKEN'))
api.reset_state()
todoist_data = api.sync()

if 'error_tag' in todoist_data:
    print('Could not get data from Todoist: ' + todoist_data['error_tag'])
    exit(1)

# P1 is actually priority 4 in the API
# P2 is actually priority 3 in the API
PRIORITY_MAP = {
    '1': 4,
    '2': 3
}


def get_project(project_name):
    projects = todoist_data['projects']

    for p in projects:
        if p['name'] == project_name:
            return p

    return None


def get_project_items(project):
    project_tasks = []

    for item in todoist_data['items']:
        if item['project_id'] == project['id']:
            project_tasks.append(item)

    return project_tasks


def purge_other_p1_items(items):
    p1_tasks = []

    for item in items:
        if item['priority'] == PRIORITY_MAP['1']:
            p1_tasks.append(item)

    # pop latest so we wont include it in our update
    p1_tasks.pop()

    for item in p1_tasks:
        item_model = api.items.get_by_id(item['id'])
        item_model.update(priority=PRIORITY_MAP['2'])
        api.commit()


def promote_p2_to_p1_item(items):
    p2_tasks = []

    for item in items:
        if item['priority'] == PRIORITY_MAP['2']:
            p2_tasks.append(item)

    latest_p2_item = p2_tasks.pop()

    if latest_p2_item:
        item_model = api.items.get_by_id(latest_p2_item['id'])
        item_model.update(priority=PRIORITY_MAP['1'])
        ret = api.commit()


# todo: pass project name as argument from Alfred
target_project = get_project('Concentrix')
tasks = get_project_items(target_project)
# purge_other_p1_items(tasks)
# promote_p2_to_p1_item(tasks)
