import argparse
from models.user import User
from models.project import Project
from models.task import Task
from utils.io import load_data, save_data
from rich.console import Console
console = Console()

#load persistent state
db = load_data()

users = db.get("users", {})

def add_user(args):
    name = args.name
    email = args.email
    users[name] = {"email": email, "projects": []}
    console.print(f"[bold green]✅ User '{args.name}' added.[/bold green]")
    save_data({"users": users})

def add_project(args):
    user = users.get(args.user)
    if user:
        project = {"title": args.title, "description": args.description, "due": args.due, "tasks": []}
        user["projects"].append(project)
        console.print(f"[bold blue]📁 Project '{args.title}' added to {args.user}.[/bold blue]")
        save_data({"users": users})
    else:
        print("❌ User not found.")

def add_task(args):
    user = users.get(args.user)
    if user:
        for project in user["projects"]:
            if project["title"] == args.project:
                task = {"title": args.title, "status": "Incomplete", "assigned_to": args.assigned}
                project["tasks"].append(task)
                console.print(f"[bold yellow]📝 Task '{args.title}' added to project '{args.project}'.[/bold yellow]")
                save_data({"users": users})
                return
        print("❌ Project not found.")
    else:
        print("❌ User not found.")

def list_users(args):
    for name, data in users.items():
        console.print(f"[cyan]{name}[/cyan] ([dim]{data['email']}[/dim])")

def list_projects(args):
    user = users.get(args.user)
    if user:
        for p in user["projects"]:
            print(f"{p['title']} - {p['due']}")
    else:
        print("❌ User not found.")

def list_tasks(args):
    user = users.get(args.user)
    if not user:
        print("❌ User not found.")
        return

    for project in user["projects"]:
        if project["title"] == args.project:
            if not project["tasks"]:
                print("📭 No tasks found.")
                return
            console.print(f"\n[bold underline]📋 Tasks for project '{args.project}':[/bold underline]")
            for task in project["tasks"]:
                icon = "✅" if task["status"] == "Complete" else "🕒"
                color = "green" if task["status"] == "Complete" else "yellow"
                console.print(f"[{color}]{icon} {task['title']}[/] (Assigned to {task['assigned_to']})")
            return

    print("❌ Project not found.")

def complete_task(args):
    user = users.get(args.user)
    if not user:
        print("❌ User not found.")
        return

    for project in user["projects"]:
        if project["title"] == args.project:
            for task in project["tasks"]:
                if task["title"] == args.title:
                    task["status"] = "Complete"
                    save_data({"users": users})
                    console.print(f"[bold green]✅ Task '{args.title}' marked as complete.[/bold green]")
                    return
            print("❌ Task not found in project.")
            return

    print("❌ Project not found for user.")

parser = argparse.ArgumentParser(description="Project Management CLI Tool")
subparsers = parser.add_subparsers()

#add user
add_user_cmd = subparsers.add_parser("add-user", help="Add a new user")
add_user_cmd.add_argument("--name", required=True)
add_user_cmd.add_argument("--email", required=True)
add_user_cmd.set_defaults(func=add_user)

#add project
add_project_cmd = subparsers.add_parser("add-project")
add_project_cmd.add_argument("--user", required=True)
add_project_cmd.add_argument("--title", required=True)
add_project_cmd.add_argument("--description", default="")
add_project_cmd.add_argument("--due", required=True)
add_project_cmd.set_defaults(func=add_project)

#add task
add_task_cmd = subparsers.add_parser("add-task")
add_task_cmd.add_argument("--user", required=True)
add_task_cmd.add_argument("--project", required=True)
add_task_cmd.add_argument("--title", required=True)
add_task_cmd.add_argument("--assigned", required=True)
add_task_cmd.set_defaults(func=add_task)

#list users
list_users_cmd = subparsers.add_parser("list-users")
list_users_cmd.set_defaults(func=list_users)

#list projects
list_projects_cmd = subparsers.add_parser("list-projects")
list_projects_cmd.add_argument("--user", required=True)
list_projects_cmd.set_defaults(func=list_projects)

#list tasks
list_tasks_cmd = subparsers.add_parser("list-tasks", help="List all tasks for a project")
list_tasks_cmd.add_argument("--user", required=True, help="User who owns the project")
list_tasks_cmd.add_argument("--project", required=True, help="Project title")
list_tasks_cmd.set_defaults(func=list_tasks)

#complete tasks
complete_task_cmd = subparsers.add_parser("complete-task", help="Mark a task as complete")
complete_task_cmd.add_argument("--user", required=True, help="User who owns the project")
complete_task_cmd.add_argument("--project", required=True, help="Project title")
complete_task_cmd.add_argument("--title", required=True, help="Task title to complete")
complete_task_cmd.set_defaults(func=complete_task)

args = parser.parse_args()
if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()