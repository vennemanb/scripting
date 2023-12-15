#!/usr/bin/python3

# Brady Venneman vennemanb1
# Hunter Perry perryh2

import argparse
import csv
import subprocess
import time

# Function to get unique user groups from the employee file
def get_unique_groups(file_path):
    groups = set()
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            groups.add(row[2])  # Assuming the user group is in the third column
    return groups

# Function to create a username for an employee
def generate_username(first_name, last_name, existing_usernames):
    base_username = (last_name + first_name).lower()
    username = base_username
    suffix = 1
    while username in existing_usernames:
        username = base_username + str(suffix)
        suffix += 1
    return username

# Function to create user groups
def create_user_groups(groups):
    for group in groups:
        # use subprocess to execute 'groupadd' command
        subprocess.run(["groupadd", group])


# Function to create user accounts
def create_user_accounts(e_file_path, output_file_path, log_file):
    # get unique user groups from the employee file
    unique_groups = get_unique_groups(e_file_path)
    # create user groups
    create_user_groups(unique_groups)
    existing_usernames = set()
    user_details = []
    with open(e_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            first_name, last_name, user_group, email = row
            # Make a unique username for each employee
            username = generate_username(first_name, last_name, existing_usernames)
            existing_usernames.add(username)
            # Append user details for writing to the output file
            user_details.append([first_name, last_name, username, "Password"])
            # Use subprocess to execute 'useradd' command
            subprocess.run(["useradd", "-c", f"{first_name} {last_name}", "-G", user_group, username])
            if log_file:
                with open(log_file, 'a') as log:
                    # Log the timestamp when user accounts were created
                    log.write(f"User account for {username} created at {time.ctime()}\n")

    with open(output_file_path, 'w', newline='') as file:
        # Write user details to the output file
        writer = csv.writer(file)
        writer.writerow(['First Name', 'Last Name', 'Username', 'Password'])
        writer.writerows(user_details)

# Argument parsing
parser = argparse.ArgumentParser(description='User Account Creation Script')
parser.add_argument('E_FILE_PATH', help='The path to the employee file')
parser.add_argument('OUTPUT_FILE_PATH', help='The path to the output file')
parser.add_argument('-l', '--log', help='The name of the log file')
parser.add_argument('-H', '-Help', action='help', help='Show this help message and exit')
args = parser.parse_args()

# Main function
def main():
    # call the function to create user accounts
    create_user_accounts(args.E_FILE_PATH, args.OUTPUT_FILE_PATH, args.log)

# check if the script is being run as the main program
if __name__ == '__main__':
    # call the main function
    main()
