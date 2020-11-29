import todoist

api = todoist.TodoistAPI('68df7a8351bb221682350ce1f745eb2c86471ac7')
api.reset_state()
todoist_data = api.sync()


def get_project_tasks(project):
    project_tasks = []

    for item in todoist_data['items']:
        if item['project_id'] == project['id']:
            project_tasks.append(item)

    return project_tasks


def get_project(project_name):
    projects = todoist_data['projects']

    for p in projects:
        if p['name'] == project_name:
            return p

    return None


# todo: pass project name as argument from Alfred
project = get_project('PSE Lookup')
tasks = get_project_tasks(project)
if tasks:
    pass