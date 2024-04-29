#!/usr/bin/python3
import os

# creates x number of files with a name
def createFiles(fileNamePrefix, numOfFiles):
    for i in range(1, numOfFiles + 1):
        file_name = f'{fileNamePrefix}_{i}.txt'
        if not os.path.exists(file_name):
            with open(file_name, 'w') as file:
                file.write(f'This is file number {i}.')

# tells wether a file is a directory or a file
def getType(fileOrDirectoryPath):
    if os.path.isfile(fileOrDirectoryPath):
        print("This is a file")
    else:
        print("This is a directory")

# renames a file and will send an error if the file is not found and makes sure only the allowed extensions are allowed
def renameFile(filename: str, newName: str):
    allowedExtensions = {".txt", ".png", ".doc", ".dat"}

    _, fileExtension = os.path.splitext(filename)

    if fileExtension.lower() in allowedExtensions:
        try:
            os.rename(filename, newName)
            print(f"File '{filename}' renamed to '{newName}'.")
        except FileNotFoundError:
            print(f"File '{filename}' does not exist.")
    else:
        print(f"Invalid file extension. Only '.txt', '.png', '.doc', and '.dat' extensions are allowed.")

# creates a directory and if one already exists it will print already exists
def createDir(nameOfDirectory):
    if os.path.isdir(nameOfDirectory):
        print ("Directory already exists")
    else:
        os.mkdir(nameOfDirectory)

# creates subdirectories and has input validation to make sure the number is greater than 0
def createSubDirectories(directoryName:str, numberToCreate:int):
    if numberToCreate <= 0:
        print("Number has to be greater than 0")
    else:
        for i in range(1, numberToCreate + 1):
            subdir = os.path.join(directoryName, f"subdir_{i}")
            try:
                os.mkdir(subdir)
                print(f"Created Subdirectory: {subdir}")
            except OSError as e:
                print(f"Error creating subdirectory {subdir}: {str(e)}")

# renames all files in a directory and makes sure only the allowed extension are able to be created
def renameFiles(targetDirectory, currentExt, newExt):
    allowedExtensions = {".txt", ".png", ".doc", ".dat"}

    if not os.path.exists(targetDirectory):
        print(f"Target directory '{targetDirectory}' does not exist.")
        return
    
    files = os.listdir(targetDirectory)
    
    for filename in files:
        _, fileExtension = os.path.splitext(filename)

        if fileExtension.lower() in allowedExtensions:
            newName = os.path.splitext(filename)[0] + newExt
            currentPath = os.path.join(targetDirectory, filename)
            newPath = os.path.join(targetDirectory, newName)
            try:
                os.rename(currentPath, newPath)
                print(f"Renamed '{filename}' to '{newName}'.")
            except Exception as e:
                print(f"Error renaming '{filename}': {str(e)}")
        else:
            print(f"Skipped '{filename}' because its extension is not allowed.")
            
# displays the contents of a directory and says whether or not it is a directory or file
def displayContents(direcotryName):
    print(f"{'Name':<30} {'type':<10}")
    print("-" * 40)
    
    for item in os.listdir(direcotryName):
        path = os.path.join(direcotryName, item)
        type = "File" if os.path.isfile(path) else "Directory"
        print(f"{item:<30} {type:<10}")


def main():
    # print the name of your current directory to the console
    current_directory = os.getcwd()

    # Create the CITFall2023<username> directory
    username = os.getlogin()
    cit_directory_name = f'CITFall2023{username}'
    os.makedirs(cit_directory_name, exist_ok=True)

    # Print the name of the current directory again
    print(f'Current directory: {current_directory}')

    # Prompt for and create files
    num_files = int(input('Enter the number of files to create: '))
    extension = input('Enter the file extension (txt, png, doc, dat): ').lower()
    createFiles(os.path.join(cit_directory_name, "file"), num_files)

    # Prompt for and create subdirectories
    num_subdirectories = int(input('Enter the number of subdirectories to create: '))
    createSubDirectories(cit_directory_name, num_subdirectories)

    # Display contents of the current directory
    displayContents(current_directory)

    #  Prompt for and rename files
    new_extension = input('Enter a new extension for the files: ').lower()
    renameFiles(cit_directory_name, extension, new_extension)

    #   Display contents of the current directory again
    displayContents(current_directory)

if __name__ == '__main__':
    main()