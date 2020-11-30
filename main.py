import sys
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

    if len(p1_tasks) == 0:
        return False

    # pop latest so we wont include it in our update
    latest_item = p1_tasks.pop()

    for item in p1_tasks:
        item_model = api.items.get_by_id(item['id'])
        item_model.update(priority=PRIORITY_MAP['2'])
        api.commit()

    return latest_item


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

        return latest_p2_item

    return False


def replace_p1_item(item_description, project):
    api.items.add(item_description, project_id=project['id'], priority=PRIORITY_MAP['1'])
    api.commit()

    api.reset_state()
    data = api.sync()

    items = get_project_items(project, data['items'])
    force_one_p1_item(items)

    return True


def complete_current_p1_item(items):
    p1_tasks = filter_p1_only(items)
    if len(p1_tasks) == 0:
        return False, False

    p1_item = p1_tasks.pop()

    item_model = api.items.get_by_id(p1_item['id'])
    item_model.close()
    api.commit()

    # promote latest p2 to p1
    promoted_item = promote_p2_to_p1_item(items)

    return p1_item, promoted_item


api = todoist.TodoistAPI(os.environ.get('TOKEN'))
api.reset_state()
todoist_data = api.sync()

if 'error_tag' in todoist_data:
    print('Could not get data from Todoist: ' + todoist_data['error_tag'])
    exit(1)


project_name = sys.argv[1]
action = sys.argv[2]

target_project = get_project(project_name, todoist_data['projects'])


if action == 'do':
    task_description = sys.argv[3]
    if replace_p1_item(task_description, target_project):
        print('P1 item added: ' + task_description)
else:
    tasks = get_project_items(target_project, todoist_data['items'])

    if action == 'next':
        promoted_item = promote_p2_to_p1_item(tasks)
        if promoted_item:
            print('Next: ' + promoted_item['content'])
        else:
            print('No item left in queue')
    elif action == 'done':
        completed_item, promoted_item = complete_current_p1_item(tasks)
        if completed_item:
            print('Completed: ' + completed_item['content'])
        if promoted_item:
            print('Next: ' + promoted_item['content'])
    elif action == 'force':
        retained_item = force_one_p1_item(tasks)
        if retained_item:
            print('Item: ' + retained_item['content'])
        else:
            print('P1 queue is empty')

