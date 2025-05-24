import argparse
import sys
from datetime import datetime
from tabulate import tabulate
from .storage import (
    get_all_tasks, 
    add_task, 
    delete_task, 
    update_task,
    TaskNotFoundError
)
from .models import Task, InvalidStatusError

STATUSES = ["todo", "in_progress", "done"]

def main():
    parser = argparse.ArgumentParser(
        description="Task Manager CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add new task")
    add_parser.add_argument("--title", required=True, help="Task title")
    add_parser.add_argument("--description", help="Task description")
    add_parser.add_argument(
        "--due-date", 
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        help="Due date in YYYY-MM-DD format"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--status", 
        choices=STATUSES,
        help="Filter by status"
    )

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete task")
    delete_parser.add_argument("--id", type=int, required=True, help="Task ID")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update task")
    update_parser.add_argument("--id", type=int, required=True, help="Task ID")
    update_parser.add_argument(
        "--status", 
        choices=STATUSES,
        help=f"New status ({', '.join(STATUSES)})"
    )
    update_parser.add_argument(
        "--due-date", 
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        help="New due date in YYYY-MM-DD format"
    )

    args = parser.parse_args()
    
    try:
        if args.command == "add":
            task = Task(
                id=0,  # Temporary, will be set in storage
                title=args.title.strip(),
                description=args.description,
                due_date=args.due_date
            )
            if not task.title:
                raise ValueError("Title cannot be empty")
            add_task(task)
            print(f"Task added with ID: {task.id}")

        elif args.command == "list":
            tasks = get_all_tasks()
            if args.status:
                tasks = [t for t in tasks if t.status == args.status]
            
            headers = ["ID", "Title", "Status", "Due Date", "Description"]
            table = [
                [t.id, t.title, t.status, t.due_date, t.description[:50] + "..." if t.description else ""]
                for t in tasks
            ]
            print(tabulate(table, headers=headers, tablefmt="grid"))

        elif args.command == "delete":
            delete_task(args.id)
            print(f"Task {args.id} deleted")

        elif args.command == "update":
            fields = {k: v for k, v in vars(args).items() 
                     if k != "id" and v is not None}
            if "status" in fields and fields["status"] not in STATUSES:
                raise InvalidStatusError(f"Invalid status: {fields['status']}")
            
            update_task(args.id, **fields)
            print(f"Task {args.id} updated")

    except (TaskNotFoundError, ValueError, InvalidStatusError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)