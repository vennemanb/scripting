#!/usr/bin/python3

import argparse
import csv
import subprocess
from email.message import EmailMessage
import smtplib
import os

def get_unique_groups(file_path):
    groups = set()
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            groups.add(row[2])
    return groups

def generate_username(first_name, last_name, existing_usernames):
    base_username = (last_name + first_name).lower()
    username = base_username
    suffix = 1
    while username in existing_usernames:
        username = base_username + str(suffix)
        suffix += 1
    return username

def create_user_groups(groups):
    for group in groups:
        subprocess.run(["groupadd", group])

def force_password_expiration(e_file_path):
    with open(e_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for i, row in enumerate(reader, start=1):
            if i % 2 != 0:
                username = row[2]
                subprocess.run(["chage", "-d", "0", username])

def create_user_accounts(e_file_path, output_file_path, log_file):
    unique_groups = get_unique_groups(e_file_path)
    create_user_groups(unique_groups)
    existing_usernames = set()
    user_details = []
    with open(e_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            first_name, last_name, user_group, email = row
            username = generate_username(first_name, last_name, existing_usernames)
            existing_usernames.add(username)
            user_details.append([first_name, last_name, username, "Password"])
            subprocess.run(["useradd", "-c", f"{first_name} {last_name}", "-G", user_group, username])
            if log_file:
                with open(log_file, 'a') as log:
                    log.write(f"User account for {username} created at {subprocess.getoutput('date')}\n")

    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['First Name', 'Last Name', 'Username', 'Password'])
        writer.writerows(user_details)

def email_temp_password(username, temp_password, user_email, sender_email, sender_password):
    try:
        msg = EmailMessage()
        msg.set_content(f"Hello, your username is: {username} and your temporary password is: {temp_password}", subtype='plain')
        msg['Subject'] = 'Your Temporary Credentials'
        msg['From'] = sender_email
        msg['To'] = user_email

        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(sender_email, sender_password)
            s.send_message(msg)

        print(f"Email sent successfully to {user_email}")
    except Exception as e:
        print(f"Error sending email to {user_email}: {str(e)}")



def piped_commands(command1: str, command2: str):
    piped_command = f"{command1} | {command2}"
    nku_username = "vennemanb1"
    subdirectory = os.path.join(os.getcwd(), nku_username)
    os.makedirs(subdirectory, exist_ok=True)
    result_file = os.path.join(subdirectory, f"{nku_username}_question2_result.txt")
    with open(result_file, 'w') as file:
        subprocess.run(piped_command, shell=True, stdout=file)

parser = argparse.ArgumentParser(description='User Account Creation Script')
parser.add_argument('E_FILE_PATH', help='The path to the employee file')
parser.add_argument('OUTPUT_FILE_PATH', help='The path to the output file')
parser.add_argument('-l', '--log', help='The name of the log file', type=str)
parser.add_argument('-q', action='store_true', help='Email the username and temporary password to the specified user')
parser.add_argument('-t', '--temporary', action='store_true', help='Force password expiration for odd-numbered rows')
parser.add_argument('-c', '--command', action='store_true', help='Perform tasks specified in question 2')
parser.add_argument('-H', '--Help', action='help', help='Show this help message and exit')
args = parser.parse_args()

def main():
    create_user_accounts(args.E_FILE_PATH, args.OUTPUT_FILE_PATH, args.log)
    if args.q:
        sender_email = 'your_email@gmail.com'  # Replace with the actual sender email
        sender_password = 'your_app_password'  # Replace with the actual sender app password

        with open(args.OUTPUT_FILE_PATH, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
           
