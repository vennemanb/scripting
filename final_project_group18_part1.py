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
from datetime import datetime, timedelta
import subprocess
import getpass

#insert your email and password to the sender 
sender_email = "autoemail1.3@gmail.com"
sender_password = "pljo isun jxnw necn"
# SMTP server details 
smtp_server = 'smtp.gmail.com'
smtp_port = 587

def find_compromised_files(username):
    # Build the find command to identify compromised files
    find_command = f'find /home/{username} -type f -ctime -30 -mtime -7'

    # Execute the find command locally
    result = subprocess.run(find_command, shell=True, capture_output=True, text=True)
    
    # Check if the command was successful
    if result.returncode == 0:
        # Read the output of the find command
        compromised_files = result.stdout.splitlines()
        return compromised_files
    else:
        print(f"Error executing find command: {result.stderr}")
        return []

# Dislpay compromised files to command prompt
def display_files(compromised_files):
    for file_path in compromised_files:
        print(file_path)

def send_email(sender_email, sender_app_password, recipient_email, compromised_files, username):
   #create a MIME multipart message for the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'File Monitoring Report'

#compose the email body
    body = f"Dear CTO,\n\nThe following files have been compromised for user {username}:\n\n{', '.join(compromised_files)}\n\nBest regards,\nYour File Monitoring Script"
    msg.attach(MIMEText(body, 'plain'))
#attach comopromised files to the email
    for file_path in compromised_files:
        with open(file_path, 'rb') as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(file_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            msg.attach(part)
            

#connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_app_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

def download_files_sftp(compromised_files, download_path, ip_address, username, password):
    transport = paramiko.Transport((ip_address, 22))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        for file_path in compromised_files:
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(download_path, file_name) if download_path else file_name

            # Download the file using SFTP
            sftp.get(file_path, destination_path)
    finally:
        sftp.close()
        transport.close()

def main():
#parse command-line arguments 
    parser = argparse.ArgumentParser(description='File Monitoring Script')
    parser.add_argument('ip_address', help='IP address of the target computer')
    parser.add_argument('username', help='Username for the account on the target computer')
    parser.add_argument('recipient_email', help='Email address of the CTO')
    parser.add_argument('-d', '--disp', action='store_true', help='Display the contents of affected files')
    parser.add_argument('-e', '--email', required=True, help='Email address of the CTO')
    parser.add_argument('-p', '--path', help='Download path for affected files')
    parser.add_argument('-H', '--hlp', action='help', help='Show this help message and exit')  

    args = parser.parse_args()

    ip_address = args.ip_address
    username = args.username
    recipient_email = args.recipient_email
    display_files_flag = args.disp
    download_path = args.path
# find compromised files based on the provided username
    compromised_files = find_compromised_files(username)
# display compromised files if the displayed flag is set
    if display_files_flag:
        display_files(compromised_files)
# send an email with the list of compromised files to the CTO
    send_email(sender_email, sender_password, recipient_email, compromised_files, username)
# download compromised files if the download path is provided 
    if download_path:
        download_files_sftp(compromised_files, download_path, ip_address, username, getpass.getpass(prompt='Enter your password: '))

if __name__ == "__main__":
    main()