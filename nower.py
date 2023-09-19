#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import json

# Function to load and save goals and actions
def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'goals': [], 'actions': []}
    return data

def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Function to add a goal
def add_goal(data, goal, parent_goal=None, due_date=None):
    goal_data = {'name': goal, 'subgoals': [], 'tasks': [], 'due_date': due_date}
    if parent_goal:
        parent_goal_index = next((i for i, item in enumerate(data['goals']) if item['name'] == parent_goal), None)
        if parent_goal_index is not None:
            data['goals'][parent_goal_index]['subgoals'].append(goal_data)
    else:
        data['goals'].append(goal_data)
    save_data(data, data_file)
    print(f'Goal "{goal}" added successfully!')


# Function to add a task/action
def add_task(data, task, goal=None, due_date=None):
    task_data = {'name': task, 'due_date': due_date}
    if goal:
        goal_index = next((i for i, item in enumerate(data['goals']) if item['name'] == goal), None)
        if goal_index is not None:
            data['goals'][goal_index]['tasks'].append(task_data)


# Function to list goals and actions
def list_goals(data, indent=0):
    for goal in data['goals']:
        due_date_info = f" (Due Date: {goal['due_date']})" if goal['due_date'] else ""
        print("  " * indent + f"- {goal['name']}{due_date_info}")
        if goal['subgoals']:
            list_goals({'goals': goal['subgoals']}, indent + 1)
        if goal['tasks']:
            list_tasks(goal['tasks'], indent + 1)
    
def list_tasks(tasks, indent):
    for task in tasks:
        due_date_info = f" (Due Date: {task['due_date']})" if task['due_date'] else ""
        print("  " * indent + f"* {task['name']}{due_date_info}")

# Function to suggest the next action
def suggest_next_action(data):
    if not data['goals']:
        print("Please add goals first.")
        return
    
    current_date = datetime.now().date()
    
    # Iterate through goals, subgoals, tasks, and actions to find the next due item
    for goal in data['goals']:
        if goal['due_date'] and goal['due_date'] >= current_date:
            print(f"Next Due Goal: {goal['name']} (Due Date: {goal['due_date']})")
            return
        for subgoal in goal['subgoals']:
            if subgoal['due_date'] and subgoal['due_date'] >= current_date:
                print(f"Next Due Subgoal: {subgoal['name']} (Due Date: {subgoal['due_date']})")
                return
            for task in subgoal['tasks']:
                if task['due_date'] and task['due_date'] >= current_date:
                    print(f"Next Due Task: {task['name']} (Due Date: {task['due_date']})")
                    return
    print("No upcoming due items found.")

# Function to display the menu
def display_menu():
    print("\n===== Goal and Action Planner Menu =====")
    print("1. Add a new goal")
    print("2. Add a new task/action")
    print("3. List all goals")
    print("4. Suggest the next due item")
    print("0. Quit")
    print("========================================")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Goal and Action Planning Program")
    parser.add_argument('--add_goal', type=str, help='Add a new goal')
    parser.add_argument('--add_task', type=str, help='Add a new task/action')
    parser.add_argument('--list_goals', action='store_true', help='List all goals')
    parser.add_argument('--suggest_next_due', action='store_true', help='Suggest the next due item')
    return parser.parse_args()

data_file = 'goals_actions.json'
data = load_data(data_file)

def main():
    args = parse_arguments()
    
    if args.add_goal:
        parts = args.add_goal.split(" due_date:")
        goal = parts[0].strip()
        due_date = datetime.strptime(parts[1], "%Y-%m-%d").date() if len(parts) == 2 else None
        add_goal(data, goal, due_date=due_date)
    elif args.add_task:
        parts = args.add_task.split(" due_date:")
        task = parts[0].strip()
        due_date = datetime.strptime(parts[1], "%Y-%m-%d").date() if len(parts) == 2 else None
        add_task(data, task, due_date=due_date)
    elif args.list_goals:
        print("List of Goals:")
        list_goals(data)
    elif args.suggest_next_due:
        suggest_next_action(data)
    else:
        #print("Please provide a valid command. Use --help for usage information.")

        while True:
            display_menu()
            choice = input("Enter your choice (0-4): ")
            
            if choice == '0':
                break
            elif choice == '1':
                goal_input = input("Enter a new goal (optional: due_date:YYYY-MM-DD): ")
                add_goal(data, goal_input)
            elif choice == '2':
                task_input = input("Enter a new task/action (optional: due_date:YYYY-MM-DD): ")
                add_task(data, task_input)
            elif choice == '3':
                print("List of Goals:")
                list_goals(data)
            elif choice == '4':
                suggest_next_action(data)
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(1)