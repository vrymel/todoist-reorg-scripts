# todoist-reorg

todoist-reorg is a helper script to manage priority items in Todoist.

## Input Args

`sys.argv[1]` - Project Name

`sys.argv[2]` - Action to perform

`sys.argv[3]` - Task description (if action is `do`)

**Actions available**

`do` - To create a P1 task

`next` - Promotes a P2 task to P1

`done` - Tags current P1 task as done

`force` - Purge P1 tasks if there are multiple
 

## Alfred

An Alfred workflow is used to interface this script.

## Requirements

- Install `todoist-python` globally
- Set a `TOKEN` environment variable
    - Since the Todoist authentication process is a bit tedious, utilizing 
    the "Test token" in the [Todoist App Management](https://developer.todoist.com/appconsole.html) will do for now.

