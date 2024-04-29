#!usr/bin/python3

import shutil
import os
import zipfile
import time


# Prompt user for a file to backup and will create a backup of that folder
def backupDirectory(sourceDir, destinationDir):
    try:
        shutil.copytree(sourceDir, destinationDir)
        print(f"Backup successful: {sourceDir} copied to {destinationDir}")
    except FileNotFoundError:
        print("Source or destination directory does not exist.")

# Prompts the user for a directory and then an archive type and will copy it to another archive type
def createArchive(directoryName, archiveType):
    userHome = os.path.expanduser("~")
    dirPath = os.path.join(userHome, directoryName)

    if os.path.exists(dirPath):
        if archiveType in ["zip", "gztar", "tar", "bztar", "xztar"]:
            archiveName = os.path.basename(dirPath)
            shutil.make_archive(archiveName, archiveType, userHome, directoryName)
            print(f"Archive created: {archiveName}.{archiveType}")
        else:
            print("Invalid archive type.")
    else:
        print(f"Directory '{directoryName}' does not exist in the user's home directory.")


# Prompts user to give a zip path and a KB threshold to check and see if any files exceed that threshold
def displayLargeFilesInfo(zipFilePath, thresholdKB):
    with zipfile.ZipFile(zipFilePath, "r") as archive:
        comment = archive.comment.decode().split('|')
        if len(comment) == 2:
            os_info, creationDate = comment
            print(f"Archive created on {creationDate}")
            print(f"OS Info: {os_info}")

        large_files = False
        for fileInfo in archive.infolist():
            if fileInfo.fileSize > thresholdKB * 1024:
                print(f"File: {fileInfo.filename}, Size: {fileInfo.fileSize / 1024} KB")
                large_files = True
        if not large_files:
            print("No files exceed the specified threshold.")


# Prompts a user for a directory and then will check to see if any of the files within have been modified in the last month
def displayRecentlyModifiedFiles(directory="."):
    oneMonthAgo = time.time() - 30 * 24 * 60 * 60 
    filesModified = False
    for root, _, files in os.walk(directory):
        for file in files:
            filePath = os.path.join(root, file)
            if os.path.getmtime(filePath) > oneMonthAgo:
                print(f"Modified in the last month: {filePath}")
                filesModified = True
    if not filesModified:
        print("No files modified in the last month.")

# Prompts the user to pick an option, either backup, archive, file info, or modified files and will display
# or create the respective option and will loop through until the user enters 5 to exit
def main():
    while True:
        print("\nMenu:")
        print("1. Backup a directory")
        print("2. Create an archive")
        print("3. Display OS info and large files in a zip file")
        print("4. Display recently modified files")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            sourceDir = input("Enter the source directory: ")
            destinationDir = input("Enter the destination directory: ")
            backupDirectory(sourceDir, destinationDir)
        elif choice == "2":
            directoryName = input("Enter the directory name: ")
            archiveType = input("Enter the archive type: ")
            createArchive(directoryName, archiveType)
        elif choice == "3":
            zipFilePath = input("Enter the path to the zip file: ")
            thresholdKB = int(input("Enter the threshold in KB: "))
            displayLargeFilesInfo(zipFilePath, thresholdKB)
        elif choice == "4":
            directory = input("Enter the directory path (default is current working directory): ")
            displayRecentlyModifiedFiles(directory)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
