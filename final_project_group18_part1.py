#!/usr/bin/python3

# Brady Venneman vennemanb1
# Hunter Perry perryh2

import paramiko
import os
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import subprocess
from getpass import getpass

# Insert your email and password to the sender
sender_email = "autoemail1.3@gmail.com"
sender_password = "pljo isun jxnw necn"

smtp_server = 'smtp.gmail.com'
smtp_port = 587

def find_compromised_files(ip_address, username, password):
    # Build the find command to identify compromised files
    find_command = f'find /home/{username} -type f -ctime -30 -mtime -7'

    # Execute the find command remotely using SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username=username, password=password)
    
    stdin, stdout, stderr = ssh.exec_command(find_command)
    
    # Check if the command was successful
    if not stderr.read().decode():
        # Read the output of the find command
        compromised_files = stdout.read().decode().splitlines()
        return compromised_files
    else:
        print(f"Error executing find command: {stderr.read().decode()}")
        return []

def send_email(sender_email, sender_app_password, recipient_email, compromised_files, username):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'File Monitoring Report'

    body = f"Dear CTO,\n\nThe following files have been compromised for user {username}:\n\n{', '.join(compromised_files)}\n\nBest regards,\nYour File Monitoring Script"
    msg.attach(MIMEText(body, 'plain'))

    for file_path in compromised_files:
        with open(file_path, 'rb') as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(file_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            msg.attach(part)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_app_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

def download_files_ssh(compromised_files, download_path, ip_address, username, password):
    for file_path in compromised_files:
        file_name = os.path.basename(file_path)
        local_file_path = os.path.join(download_path, file_name)

        # Use SCP to copy files from the remote server to the local machine
        scp_command = f'scp {username}@{ip_address}:{file_path} {local_file_path}'

        try:
            # Execute the SCP command locally
            result = subprocess.run(scp_command, shell=True, check=True, capture_output=True)
            print(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            if "Permission denied" in e.stderr.decode():
                print(f"Permission denied for {file_name}. Skipping...")
                continue
            else:
                print(f"Error downloading {file_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description='File Monitoring Script')
    parser.add_argument('ip_address', help='IP address of the target computer')
    parser.add_argument('username', help='Username for the account on the target computer')
    parser.add_argument('recipient_email', help='Email address of the CTO')
    parser.add_argument('-d', '--disp', action='store_true', help='Display the contents of affected files')
    parser.add_argument('-e', '--email', required=True, help='Email address of the CTO')
    parser.add_argument('-p', '--path', help='Download path for affected files')
    parser.add_argument('-H', '--help', action='help', help='Show this help message and exit')

    args = parser.parse_args()

    ip_address = args.ip_address
    username = args.username
    password = getpass("Enter your SSH password: ")  # Securely get the password
    recipient_email = args.recipient_email
    display_files_flag = args.disp
    download_path = args.path

    compromised_files = find_compromised_files(ip_address, username, password)

    if display_files_flag:
        print("Affected Files:")
        for file_path in compromised_files:
            print(file_path)

    send_email(sender_email, sender_password, recipient_email, compromised_files, username)

    if download_path:
        download_files_ssh(compromised_files, download_path, ip_address, username, password)
    else:
        # If no download path is given, download the smallest compromised file
        smallest_file = min(compromised_files, key=os.path.getsize)
        download_files_ssh([smallest_file], '.', ip_address, username, password)

if __name__ == "__main__":
    main()
