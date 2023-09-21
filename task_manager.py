"""
Overview of program:
This is a program for a small business to help them manage tasks assigned 
to each member of the team.
"""

import datetime

signed_in = False

# gets the user's username and passwoclrd
username = input("Enter your username: \n")
password = input("Enter your password: \n")


# returns a list of tasks from the tasks.txt file
def load_tasks():
    tasks_file = open("./data/tasks.txt", "r")
    # splitlines() removes the new line character from each line
    tasks_list = tasks_file.read().splitlines()
    tasks_file.close()
    return tasks_list


# returns a list of users from the user.txt file
def load_users():
    users_file = open("./data/user.txt", "r")
    users_list = users_file.read().splitlines()
    users_file.close()
    return users_list


tasks_list = load_tasks()
users_list = load_users()


# logs the user in depending on the user's credentials
def login():
    global signed_in, username, password, users_list

    login_successful = False

    # loop through the list of users
    for user in users_list:
        # remove the new line character
        user = user.strip().split(", ")

        # if the username and password match
        if username == user[0] and password == user[1]:
            login_successful = True
            break

        # if the username matches but not the password
        elif username == user[0] and password != user[1]:
            print("\nIncorrect password.\n")
            username = input("Enter your username: \n")
            password = input("Enter your password: \n")

    # if the login was successful
    if login_successful:
        print(f"\nLogin successful. \nWelcome, {username}!\n")
        signed_in = True

    # if no credentials match
    else:
        print("\nUsername does not exist.\n")
        username = input("Enter your username: \n")
        password = input("Enter your password: \n")


login()


# registers a new user depending on the user's access level
def reg_user():
    global username

    # NO ADMIN ACCESS:
    if username != "admin":
        print("\nOnly admin can register a new user.\n")
        return

    # ADMIN ACCESS:
    # loop will run until the user enters a new username that does not already exist
    while True:
        new_username = input("\nEnter a new username: \n")

        # loop through the list of users and get the existing usernames
        for line in users_list:
            existing_usernames = line.split(",")[0].strip()

        # if the username already exists
        if new_username in existing_usernames:
            print(
                f"\n{new_username} already exists. Please choose a different username.\n"
            )

        # exit the loop if the username does not exist
        else:
            break

    # get new and confirmed password from the user
    new_password = input("Enter a new password: \n")
    confirm_password = input("Confirm password: \n")

    # if the new and confirmed password are the same
    if new_password == confirm_password:
        # append the new username and password to the user.txt file
        users_file = open("./data/user.txt", "a")
        users_file.write(f"\n{new_username}, {new_password}")
        users_file.close()
        print("\nUser successfully registered!\n")

    # if the passwords do not match
    else:
        print("\nPasswords do not match. Please try again.\n")


# assigns a new task to a user
def add_task():
    # get the task details from the user
    task_username = input(
        "Enter the username of the person the task is assigned to: \n"
    )
    task_title = input("Enter the title of the task: \n")
    task_description = input("Enter the description of the task: \n")
    task_due_date = input(
        "Enter the due date of the task (Format Example: 18 Aug 2023): \n"
    )

    # set the current date as the date assigned to the task
    task_date_assigned = datetime.datetime.now().strftime("%d %b %Y")
    task_completed = "No"

    # open the tasks.txt file, write the new task to the file, and close the file
    tasks_file = open("./data/tasks.txt", "a")
    tasks_file.write(
        "\n"
        + ", ".join(
            [
                task_username,
                task_title,
                task_description,
                task_date_assigned,
                task_due_date,
                task_completed,
            ]
        )
    )
    tasks_file.close()
    print("\nTask successfully added!\n")


# displays all the tasks in the task.txt file
def view_all():
    global tasks_list

    # loop through the list of tasks and print the results in the desired format
    for task in tasks_list:
        task = task.strip().split(", ")
        print(
            "----------------------------------------------------------------------------------------------"
        )
        print(f"Task:               {task[1]}")
        print(f"Assigned to:        {task[0]}")
        print(f"Date assigned:      {task[3]}")
        print(f"Due date:           {task[4]}")
        print(f"Task completed?     {task[5]}")
        print(f"Task description:\n{task[2]}")
        print(
            "----------------------------------------------------------------------------------------------"
        )
        print()


# allows the user to edit a task if they are the assigned user of the task
def edit_task():
    task_to_edit = int(
        input("Enter a task number to edit or enter -1 to go back to the menu: \n")
    )

    # if the user enters -1, return to the menu
    if task_to_edit == -1:
        return

    # get the selected task from the tasks list
    selected_task = tasks_list[task_to_edit - 1].strip().split(", ")
    task_username = selected_task[0]

    # if the user is not the assigned user of the task
    if username != task_username:
        print("\nYou can only edit your own tasks.\n")
        return

    task_option = input(
        "Please select one of the following options:\n m - mark task as complete\n e - edit task\n"
    ).lower()

    # if the user chooses to mark the task as complete
    if task_option == "m":
        if selected_task[5] == "Yes":
            print(
                "\nTask has already been marked as complete. You cannot edit this task.\n"
            )
        else:
            selected_task[5] = "Yes"
            # update the tasks.txt file
            tasks_list[task_to_edit - 1] = ", ".join(selected_task)
            print("\nTask successfully marked as complete!\n")

            # save the updated tasks list to the file
            tasks_file = open("./data/tasks.txt", "r+")
            tasks_file.write("\n".join(tasks_list))
            tasks_file.truncate()  # clear any remaining content in the file
            tasks_file.close()

    # if the user chooses to edit the task
    elif task_option == "e":
        if selected_task[5] == "Yes":
            print("\nTask has been marked as complete. You cannot edit this task.\n")
            return

        edit_option = input(
            "Please select one of the following options:\n u - edit the username of who the task is assigned to\n d - edit the due date of the task\n"
        ).lower()

        if edit_option == "u":
            edited_username = input(
                "\nEnter the username of who you want the task re-assigned to: \n"
            )
            selected_task[0] = edited_username
            print("\nTask username successfully updated!\n")

        elif edit_option == "d":
            edited_due_date = input(
                "\nEnter the new due date of the task (Format Example: 18 Aug 2023): \n"
            )
            selected_task[4] = edited_due_date
            print("\nTask due date successfully updated!\n")

        # update the tasks list with the updated task
        tasks_list[task_to_edit - 1] = ", ".join(selected_task).strip()

        # save the updated tasks list to the file
        tasks_file = open("./data/tasks.txt", "r+")
        tasks_file.write("\n".join(tasks_list))
        tasks_file.truncate()  # clear any remaining content in the file
        tasks_file.close()


# displays the current user's tasks
def view_mine():
    global username, tasks_list
    task_number = 0

    # loop through the list of tasks
    for task in tasks_list:
        task_number += 1
        task = task.strip().split(", ")

        # if the username of the current user matches the username of the task
        if username == task[0]:
            print(f"Task: {task_number}")
            print(
                "----------------------------------------------------------------------------------------------"
            )
            print(f"Task:               {task[1]}")
            print(f"Assigned to:        {task[0]}")
            print(f"Date assigned:      {task[3]}")
            print(f"Due date:           {task[4]}")
            print(f"Task completed?     {task[5]}")
            print(f"Task description:\n{task[2]}")
            print(
                "----------------------------------------------------------------------------------------------"
            )
            print()

    edit_task()


# display statistics from the task_overview.txt and user_overview.txt files
def display_stats():
    # TASK OVERVIEW:
    task_overview_file = open("./overviews/task_overview.txt", "r")
    task_overview = task_overview_file.read()
    print(task_overview)
    task_overview_file.close()

    # USER OVERVIEW:
    user_overview_file = open("./overviews/user_overview.txt", "r")
    user_overview = user_overview_file.read()
    print(user_overview)
    user_overview_file.close()


# writes the required reports to the task_overview.txt and user_overview.txt files
def generate_reports():
    global tasks_list, users_list

    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    for task in tasks_list:
        task = task.strip().split(", ")

        # if the task has been marked as complete
        if task[5] == "Yes":
            completed_tasks += 1

        # if the task has not been marked as complete
        elif task[5] == "No":
            uncompleted_tasks += 1

            # determine if the task is overdue
            task_due_date = datetime.datetime.strptime(task[4], "%d %b %Y")
            current_date = datetime.datetime.now()
            if current_date > task_due_date:
                overdue_tasks += 1

    # percentage of tasks incomplete
    # used if-else statements to avoid division by zero error
    if len(tasks_list) != 0:
        percentage_incomplete = round((uncompleted_tasks / len(tasks_list)) * 100, 2)
    else:
        percentage_incomplete = 0

    # percentage of overdue tasks
    if len(tasks_list) != 0:
        percentage_overdue = round((overdue_tasks / len(tasks_list)) * 100, 2)
    else:
        percentage_overdue = 0

    # write everything to the task_overview.txt file
    task_overview_file = open("./overviews/task_overview.txt", "w")
    task_overview_file.write(
        f"""TASK OVERVIEW:
Total number of tasks generated: {len(tasks_list)}
Total number of completed tasks: {completed_tasks}
Total number of uncompleted tasks: {uncompleted_tasks}
Total number of overdue tasks: {overdue_tasks}
Percentage of tasks that are incomplete: {percentage_incomplete}%
Percentage of tasks that are overdue: {percentage_overdue}%
"""
    )

    # get the total number of users and tasks
    total_users = len(users_list)
    total_tasks = len(tasks_list)

    user_overview = ""

    # Displays the total number of tasks assigned to the user and
    # the percentage of the total tasks assigned that were assigned to the user
    for user in users_list:
        user = user.strip().split(", ")

        user_tasks = 0
        user_completed_tasks = 0
        user_uncompleted_tasks = 0
        user_overdue_tasks = 0

        for task in tasks_list:
            task = task.strip().split(", ")

            # if the username of the user matches the username of the task
            if user[0] == task[0]:
                user_tasks += 1

                # if the task has been marked as complete
                if task[5] == "Yes":
                    user_completed_tasks += 1

                # if the task has not been marked as complete
                elif task[5] == "No":
                    user_uncompleted_tasks += 1

                    # determine if the task is overdue
                    task_due_date = datetime.datetime.strptime(task[4], "%d %b %Y")
                    current_date = datetime.datetime.now()
                    if current_date > task_due_date:
                        user_overdue_tasks += 1

        # used if-else statements to avoid zero division error
        # percentage of the total tasks assigned to the user
        if user_tasks != 0:
            user_percentage = round((user_tasks / total_tasks) * 100, 2)
        else:
            user_percentage = 0

        # percentage of completed tasks assigned to the user
        if user_tasks != 0:
            completed_percentage = round((user_completed_tasks / user_tasks) * 100, 2)
        else:
            completed_percentage = 0

        # percentage of uncompleted tasks assigned to the user
        if user_tasks != 0:
            uncompleted_percentage = round(
                (user_uncompleted_tasks / user_tasks) * 100, 2
            )
        else:
            uncompleted_percentage = 0

        # percentage of overdue tasks assigned to the user
        if user_tasks != 0:
            overdue_percentage = round((user_overdue_tasks / user_tasks) * 100, 2)
        else:
            overdue_percentage = 0

        # add the user's overview information to the user_overview variable
        user_overview += f"""{user[0]}:
Total number of tasks assigned to the user: {user_tasks}
Percentage of the total tasks assigned to the user: {user_percentage}%
Percentage of tasks assigned to the user that have been completed: {completed_percentage}%
Percentage of tasks assigned to the user that have not been completed: {uncompleted_percentage}%
Percentage of tasks assigned to the user that are overdue: {overdue_percentage}% \n
"""
        # write the total number of users, tasks and the user's overview information to the user_overview.txt file
        user_overview_file = open("./overviews/user_overview.txt", "w")
        user_overview_file.write(
            f"""USER OVERVIEW:
Total number of users registered: {total_users}
Total number of tasks generated: {total_tasks}\n
{user_overview}
"""
        )

    load_tasks()
    load_users()

    print(
        "\nReports successfully generated! You can view them from inside the overviews folder.\n"
    )


while signed_in:
    # ADMIN ACCESS MENU:
    if username == "admin":
        menu_option = input(
            """Please select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
gr - generate reports
ds - display statistics
e - exit
: """
        ).lower()

    # NORMAL USER ACCESS MENU:
    else:
        menu_option = input(
            """Please select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
gr - generate reports
e - exit
: """
        ).lower()

    # REGISTER A NEW USER:
    if menu_option == "r":
        reg_user()

    # ADD A NEW TASK:
    elif menu_option == "a":
        add_task()

    # VIEW ALL USERS' TASKS:
    elif menu_option == "va":
        view_all()

    # VIEW THE CURRENT USER'S TASKS:
    elif menu_option == "vm":
        view_mine()

    # GENERATE REPORTS:
    elif menu_option == "gr":
        generate_reports()

    # DISPLAY STATISTICS:
    elif menu_option == "ds":
        generate_reports()
        display_stats()

    # EXIT:
    elif menu_option == "e":
        print("Goodbye!!!")
        break

    else:
        print("You have entered an invalid input. Please try again")


"""
References:
https://www.w3schools.com/python/python_datetime.asp
https://builtin.com/software-engineering-perspectives/pass-vs-continue-python
https://www.programiz.com/python-programming/methods/string/splitlines
"""
