import os
import todoist

# P1 is actually priority 4 in the API
# P2 is actually priority 3 in the API
PRIORITY_MAP = {
    '1': 4,
    '2': 3
}


def get_project(project_name, projects):
    for p in projects:
        if p['name'] == project_name:
            return p

    return None


def get_project_items(project, items):
    project_tasks = []

    for item in items:
        if item['project_id'] == project['id']:
            project_tasks.append(item)

    return project_tasks


def force_one_p1_item(items):
    p1_tasks = filter_p1_only(items)

    # pop latest so we wont include it in our update
    p1_tasks.pop()

    for item in p1_tasks:
        item_model = api.items.get_by_id(item['id'])
        item_model.update(priority=PRIORITY_MAP['2'])
        api.commit()


def filter_p1_only(items):
    p1_tasks = []

    for item in items:
        if item['priority'] == PRIORITY_MAP['1']:
            p1_tasks.append(item)

    return p1_tasks


def promote_p2_to_p1_item(items):
    p2_tasks = []

    for item in items:
        if item['priority'] == PRIORITY_MAP['2']:
            p2_tasks.append(item)

    latest_p2_item = p2_tasks.pop()

    if latest_p2_item:
        item_model = api.items.get_by_id(latest_p2_item['id'])
        item_model.update(priority=PRIORITY_MAP['1'])
        api.commit()


def replace_p1_item(item_description, project):
    api.items.add(item_description, project_id=project['id'], priority=PRIORITY_MAP['1'])
    api.commit()

    api.reset_state()
    data = api.sync()

    items = get_project_items(project, data['items'])
    force_one_p1_item(items)


def complete_current_p1_item(items):
    p1_tasks = filter_p1_only(items)
    p1_item = p1_tasks.pop()

    item_model = api.items.get_by_id(p1_item['id'])
    item_model.close()
    api.commit()

    # promote latest p2 to p1
    promote_p2_to_p1_item(items)


api = todoist.TodoistAPI(os.environ.get('TOKEN'))
api.reset_state()
todoist_data = api.sync()

if 'error_tag' in todoist_data:
    print('Could not get data from Todoist: ' + todoist_data['error_tag'])
    exit(1)

# todo: pass project name as argument from Alfred
target_project = get_project('Concentrix', todoist_data['projects'])
tasks = get_project_items(target_project, todoist_data['items'])
# force_one_p1_item(tasks)
# promote_p2_to_p1_item(tasks)
# replace_p1_item('test new p1.2 task', target_project)
complete_current_p1_item(tasks)