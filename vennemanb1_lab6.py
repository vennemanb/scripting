#!/usr/bin/python3
import subprocess
import random
import string
import time


# check if a username already exists
# if username isnt found will return 'name' not found
def checkUser(username):
    result = subprocess.run(["id", username], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0


# create a new user and to create a random password for that user
def createUser(fullName, username):
    if checkUser(username):
        print("User already exists.")
        return False

    # Generate a random password for the user
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    try:
        subprocess.run(["sudo", "useradd", "-m", "-p", password, "-c", fullName, username], check=True)
        # give time for user to be created before checking if it exists
        time.sleep(2)  
        if checkUser(username):
            print(f"User {username} created successfully.")
            return True
        else:
            print(f"Failed to create user {username}.")
            return False
    except subprocess.CalledProcessError as e:
        print(e.output)
        return False


# checks to see if valid user and then will delete the user if it exists
def deleteUser(username):
    if not checkUser(username):
        print("User does not exist.")
        return

    try:
        subprocess.run(["sudo", "userdel", "-r", username], check=True)
        if not checkUser(username):
            print(f"User {username} deleted successfully.")
        else:
            print(f"Failed to delete user {username}.")
    except subprocess.CalledProcessError as e:
        print(e.output)


# modify an existing user account. Can either lock or change the real name of a user
def modifyUser(username, option, newValue=None):
    if not checkUser(username):
        print("User does not exist.")
        return

    if option == "lock":
        try:
            subprocess.run(["sudo", "usermod", "-L", username], check=True)
            print(f"User {username} locked successfully.")
        except subprocess.CalledProcessError as e:
            print(e.output)
    elif option == "change_name":
        try:
            subprocess.run(["sudo", "usermod", "-c", newValue, username], check=True)
            print(f"Real name for {username} changed to {newValue} successfully.")
        except subprocess.CalledProcessError as e:
            print(e.output)


# main function to loop through main menu of program
# has input validation. Continually runs until 5 is entered then program ends
def main():
    while True:
        print("\n1. Check if username exists")
        print("2. Create a new user")
        print("3. Delete a user")
        print("4. Modify an existing user")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username to check: ")
            if checkUser(username):
                print(f"User {username} exists.")
            else:
                print(f"User {username} does not exist.")

        elif choice == '2':
            fullName = input("Enter full name: ")
            username = input("Enter username: ")
            createUser(fullName, username)

        elif choice == '3':
            username = input("Enter username to delete: ")
            deleteUser(username)

        elif choice == '4':
            username = input("Enter username to modify: ")
            option = input("Enter 'lock' to lock the account or 'change_name' to change the real name: ")
            if option == 'change_name':
                newValue = input("Enter the new name: ")
                modifyUser(username, option, newValue)
            elif option == 'lock':
                modifyUser(username, option)
            else:
                print("Invalid option.")

        elif choice == '5':
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
