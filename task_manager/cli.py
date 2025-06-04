import argparse
from datetime import datetime
from .storage import get_all_tasks, add_task, delete_task, update_task
from .models import TaskNotFoundError 

def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("--title", required=True, help="Title of the task")
    add_parser.add_argument("--description", help="Description of the task")
    add_parser.add_argument("--due-date", help="Due date of the task (YYYY-MM-DDTHH:MM:SS format)")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--status", choices=["todo", "in_progress", "done"], help="Filter tasks by status")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("--id", type=int, required=True, help="ID of the task to update")
    update_parser.add_argument("--status", choices=["todo", "in_progress", "done"], help="New status for the task")
    update_parser.add_argument("--due-date", help="New due date for the task (YYYY-MM-DDTHH:MM:SS format)")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("--id", type=int, required=True, help="ID of the task to delete")

    args = parser.parse_args()
    
    if args.command == "add":
        task_data = {
            "title": args.title,
            "description": args.description,
        }
        if args.due_date:
            try:
                task_data["due_date"] = datetime.fromisoformat(args.due_date)
            except ValueError:
                print("Error: Invalid due-date format. Please use YYYY-MM-DDTHH:MM:SS")
                return
        
        try:
            task = add_task(task_data)
            print(f"Task added: ID={task.id}, Title='{task.title}'")
        except Exception as e:
            print(f"Error adding task: {e}")

    elif args.command == "list":
        tasks = get_all_tasks()
        if args.status:
            tasks = [t for t in tasks if t.status == args.status]
        
        if not tasks:
            print("No tasks found.")
            return

        print(f"{'ID':<4} {'Title':<30} {'Status':<15} {'Due Date':<20} {'Created At':<20}")
        print("-" * 90)
        for task in tasks:
            due_date_str = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "N/A"
            created_at_str = task.created_at.strftime("%Y-%m-%d %H:%M")
            print(f"{task.id:<4} {task.title:<30} {task.status:<15} {due_date_str:<20} {created_at_str:<20}")

    elif args.command == "update":
        update_data = {}
        if args.status:
            update_data["status"] = args.status
        if args.due_date:
            try:
                update_data["due_date"] = datetime.fromisoformat(args.due_date)
            except ValueError:
                print("Error: Invalid due-date format. Please use YYYY-MM-DDTHH:MM:SS")
                return

        if not update_data:
            print("No fields provided for update.")
            return

        try:
            updated_task = update_task(args.id, **update_data)
            updated_due_date_str = updated_task.due_date.strftime("%Y-%m-%d %H:%M") if updated_task.due_date else "None"
            print(f"Task {updated_task.id} updated: Status='{updated_task.status}', Due Date='{updated_due_date_str}'")
        except TaskNotFoundError:
            print(f"Error: Task with ID {args.id} not found.")
        except ValueError as e:
            print(f"Error updating task: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif args.command == "delete":
        try:
            delete_task(args.id)
            print(f"Task with ID {args.id} deleted successfully.")
        except TaskNotFoundError:
            print(f"Error: Task with ID {args.id} not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()