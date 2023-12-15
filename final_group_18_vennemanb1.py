#!/usr/bin/python3

# Brady Venneman vennemanb1
# Hunter Perry perryh2

import argparse
import csv
import subprocess
import time
from email.message import EmailMessage
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


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

# Function to force password expiration for odd-numbered rows
def force_password_expiration(e_file_path):
    with open(e_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for i, row in enumerate(reader, start=1):
            if i % 2 != 0:  # Check if the row is odd-numbered
                username = row[2]  # Assuming the username is in the third column
                # Use subprocess to execute 'chage' command to force password expiration
                subprocess.run(["chage", "-d", "0", username])

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
            # Email username and temporary password if -q option is present
            # This will involve sending an email to the specified user with the username and temporary password
            # The implementation will depend on the email service or library being used

    with open(output_file_path, 'w', newline='') as file:
        # Write user details to the output file
        writer = csv.writer(file)
        writer.writerow(['First Name', 'Last Name', 'Username', 'Password'])
        writer.writerows(user_details)


def email_temp_password(username, temp_password, user_email, sender_email, sender_password):
    msg = MIMEMultipart()
    msg.attach(MIMEText(f"Hello, your username is: {username} and your temporary password is: {temp_password}"))
    msg['Subject'] = 'Your Temporary Credentials'
    msg['From'] = sender_email
    msg['To'] = user_email

    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.starttls()
        s.login(sender_email, sender_password)
        s.send_message(msg)

def piped_commands(command1: str, command2: str):
    # Combine the two commands with a pipe
    piped_command = f"{command1} | {command2}"

    # Get NKU username
    nku_username = "vennemanb1"  # Replace with your NKU username or retrieve dynamically

    # Create a subdirectory with NKU username
    subdirectory = os.path.join(os.getcwd(), nku_username)
    os.makedirs(subdirectory, exist_ok=True)

    # Name of the result file
    result_file = os.path.join(subdirectory, f"{nku_username}_question2_result.txt")

    # Execute the piped command and save the result to the file
    with open(result_file, 'w') as file:
        subprocess.run(piped_command, shell=True, stdout=file)

# Argument parsing
parser = argparse.ArgumentParser(description='User Account Creation Script')
parser.add_argument('E_FILE_PATH', help='The path to the employee file')
parser.add_argument('OUTPUT_FILE_PATH', help='The path to the output file')
parser.add_argument('-l', '--log', help='The name of the log file', type=str)  # Specify type=str
parser.add_argument('-q', action='store_true', help='Email the username and temporary password to the specified user')
parser.add_argument('-t', '--temporary', action='store_true', help='Force password expiration for odd-numbered rows')
parser.add_argument('-c', '--command', action='store_true', help='Perform tasks specified in question 2')
parser.add_argument('-H', '--Help', action='help', help='Show this help message and exit')
args = parser.parse_args()

# Main function
def main():
    create_user_accounts(args.E_FILE_PATH, args.OUTPUT_FILE_PATH, args.log)
    if args.q:
        sender_email = ''
        sender_password = ''
        with open(args.OUTPUT_FILE_PATH, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                username = row[2]
                temp_password = row[3]
                user_email = row[3]
                email_temp_password(username, temp_password, user_email, sender_email, sender_password)

    if args.temporary:
        force_password_expiration(args.E_FILE_PATH)

    if args.command:
            # Get two commands from the user
            command1 = input("Enter the first Linux command: ")
            command2 = input("Enter the second Linux command: ")
    
            # Call the function to execute the piped commands
            piped_commands(command1, command2)
# check if the script is being run as the main program
if __name__ == '__main__':
    # call the main function
    main()
