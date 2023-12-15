import paramiko
import os
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from getpass import getpass

# Insert your email and password to the sender
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"

smtp_server = 'smtp.gmail.com'
smtp_port = 587

def find_compromised_files(ip_address, username, password, path):
    # Command to identify compromised files
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

# Send email to CTO with compromised user and the files
def send_email(sender_email, sender_app_password, recipient_email, compromised_files, username):
    # Check if recipient_email is provided
    if recipient_email:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = 'File Monitoring Report'

        body = f"Dear CTO,\n\nThe following files have been compromised for user {username}:\n\n{', '.join(compromised_files)}\n\nBest regards,\nYour File Monitoring Script"
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach files to the email
        for file_path in compromised_files:
            with open(file_path, 'rb') as file:
                part = MIMEApplication (file.read(), Name=os.path.basename(file_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                msg.attach(part)

        # Send email
        try:
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_app_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email sent successfully!")
        except Exception as e:
    print(f"Error sending email: {str(e)}")
    else:
        print("Recipient email not provided. Skipping email notification.")

# Download the compromised files via SSH
def download_files_ssh(compromised_files, download_path, ip_address, username, password):
    # Establish the SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username=username, password=password)

    # if path isnt found create it
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Download the compromised files
    for file_path in compromised_files:
        file_name = os.path.basename(file_path)
        local_file_path = os.path.join(download_path, file_name)

        try:
            # Use SFTP to download files from the remote server to the local machine
            sftp = ssh.open_sftp()
            sftp.get(file_path, local_file_path)
            sftp.close()
            print(f"Downloaded: {file_name}")
        except Exception as e:
            print(f"Error downloading {file_name}: {str(e)}")
            # Continue to the next file even if an error occurs

    # Close the SSH connection
    ssh.close()


def main():
    # Add all command line arguments to use
    parser = argparse.ArgumentParser(description='File Monitoring Script')
    parser.add_argument('ip_address', help='IP address of the target computer')
    parser.add_argument('username', help='Username for the account on the target computer')
    parser.add_argument('-e', '--email', help='Email address of the CTO')
    parser.add_argument('-d', '--disp', action='store_true', help='Display the contents of affected files')
    parser.add_argument('-p', '--path', help='Download path for affected files')
    parser.add_argument('-H', '--Help', action='help', help='Show this help message and exit')

    args = parser.parse_args()

    ip_address = args.ip_address
    username = args.username
    password = getpass("Enter your SSH password: ")
    recipient_email = args.email
    display_files_flag = args.disp
    download_path = args.path

    compromised_files = find_compromised_files(ip_address, username, password, download_path)

    # Display files if -d flag is present
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
