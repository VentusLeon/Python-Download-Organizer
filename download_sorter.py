import os
import shutil
import time

#function attemps to find the downloads folder by starting from default home directory path and joining with "Downloads"
#if downloads directory can't be found that way, it tries alternative approaches appropriate for other common operating systems
def get_downloads_folder():
    home = os.path.expanduser("~")

    if home:
        downloads_folder = os.path.join(home, "Downloads")
        if os.path.exists(downloads_folder) and os.path.isdir(downloads_folder):
            return downloads_folder
        
    system = os.name
    if system == "nt": #Windows
        downloads_folder = os.path.join(os.getenv("USERPROFILE"), "Downloads")
    elif system == "posix": #POSIX (Unix-like) OS
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    else:
        downloads_folder = None

    if downloads_folder and os.path.exists(downloads_folder) and os.path.isdir(downloads_folder):
        return downloads_folder
    
    return None

#creates a folder for sorted downloads to go to on the desktop (if one already exists, simply returns the existing folder's path)
def create_sorted_downloads_folder():
    home = os.path.expanduser("~")

    if home:
        desktop_path = os.path.join(home, "Desktop") 
        if os.path.exists(desktop_path) and os.path.isdir(desktop_path):
            sorted_downloads_folder_path = os.path.join(desktop_path, "Sorted-Downloads")
            if os.path.exists(sorted_downloads_folder_path):
                return sorted_downloads_folder_path
            else:
                os.mkdir(sorted_downloads_folder_path)
                return sorted_downloads_folder_path
            

    system = os.name
    if system == "nt": #Windows
        desktop_path = os.path.join(os.getenv("USERPROFILE"), "Desktop")
    elif system == "posix": #POSIX (Unix-like) OS
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    

    if desktop_path and os.path.exists(desktop_path) and os.path.isdir(desktop_path):
        sorted_downloads_folder_path = os.path.join(desktop_path, "Sorted-Downloads")
        if os.path.exists(sorted_downloads_folder_path):
            return sorted_downloads_folder_path
        else:
            os.mkdir(sorted_downloads_folder_path)
            return sorted_downloads_folder_path
    
    return None
    
    


#function that returns list of all folders in a given path directory
def get_folders(path):
    list_of_folders = []
    try:
        if os.path.exists(path):
            items = os.listdir(path)

            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    list_of_folders.append(item)

        else:
            print("Directory does not exist")

        return list_of_folders

    except Exception as e:
        print(f"An error occurred: {e}")


#function returns list of all new files in download directory
def check_download_files():
    files = os.listdir(download_dir)
    return [file for file in files if not file.startswith(".")]

#moves file from download directory to destination directory
def sort_file(file_name):
    name, file_extension = os.path.splitext(file_name)

    folder_name = file_extension.replace(".", "")

    if folder_name in get_folders(destination_dir):
        shutil.move(os.path.join(download_dir, file_name), os.path.join(destination_dir, folder_name))

    else:
        os.mkdir(os.path.join(destination_dir, folder_name))
        shutil.move(os.path.join(download_dir, file_name), os.path.join(destination_dir, folder_name))

#attempts to automatically find path to default downloads folder
download_dir = get_downloads_folder()

#prompts user in terminal for path to downloads folder if one cannot be found automatically
if download_dir == None:
    download_dir = input("Download folder not found, please copy and paste Downloads folder path: ")

#creates sorted downloads folder on desktop or returns its path if one already exists
destination_dir = create_sorted_downloads_folder()

#infinite loop that checks for new files every 5 seconds and moves newly downloaded files to the destination directory
while True:
    new_files = check_download_files()

    if len(new_files) > 0:
        for file in new_files:
            sort_file(file)

    time.sleep(5)