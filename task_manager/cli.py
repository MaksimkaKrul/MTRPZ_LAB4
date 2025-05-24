import argparse
from task_manager.storage import get_all_tasks, add_task, delete_task

def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--description")
    
    # List command
    subparsers.add_parser("list")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type=int, required=True)

    args = parser.parse_args()
    
    if args.command == "add":
        add_task({"title": args.title, "description": args.description})
    elif args.command == "list":
        for task in get_all_tasks():
            print(task)
    elif args.command == "delete":
        delete_task(args.id)