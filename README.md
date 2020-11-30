# todoist-reorg

todoist-reorg is a helper script to manage priority items in Todoist. I created this script to help me with my task 
management workflow in Todoist.

There are certain rules I like to follow when handling priority items.

1. There should only be one P1 item at a time for a project.
1. When adding a new P1 item (and there is an existing P1 item in the queue) the existing P1 item should be 
demoted to P2 maintaining rule 1. 
1. When completing a P1 item, a P2 item should automatically be promoted to P1. 

## Input Args

`sys.argv[1]` - Project Name

`sys.argv[2]` - Action to perform

`sys.argv[3]` - Task description (if action is `do`)

**Actions available**

`do` - To create a P1 task. If there is an existing P1 task, it will be demoted to P2.

`next` - Promotes a P2 task to P1

`done` - Tags current P1 task as done and promotes a P2 task to P1.

`force` - Purge P1 tasks if there are multiple. Only the newest P1 task will remain.
 

## Alfred

An Alfred workflow is used to interface this script.

## Requirements

- Install `todoist-python` globally
- Set a `TOKEN` environment variable
    - Since the Todoist authentication process is a bit tedious, utilizing 
    the "Test token" in the [Todoist App Management](https://developer.todoist.com/appconsole.html) will do for now.

