from tkinter import Tk
from tkinter import filedialog
import os
import configparser

docs_mods_path =""   
steam_mods_path = ""


def get_saved_paths():
    global docs_mods_path
    global steam_mods_path
    config = configparser.ConfigParser()
    config.read('config.ini')
    steam_mods_path = config.get("PATHS","steam_mods_path")

    if steam_mods_path == "notSet":
        steam_mods_path = user_path_prompt("--SELECT STEAM MODS FOLDER--")
        store_path(steam_mods_path)

    docs_mods_path = config.get("PATHS","docs_mods_path")

    if docs_mods_path == "notSet":
        docs_mods_path = user_path_prompt("--SELECT DOCUMENTS MODS FOLDER--")
        store_path(docs_mods_path)



def user_path_prompt(title):
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title = title)


    return folder_selected


def store_path(path):
    config_variable = ""
    if "Steam" in path:
        config_variable = "steam_mods_path"

    elif "Documents" in path:
        config_variable = "docs_mods_path"

    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set("PATHS", config_variable, path )
    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)




def get_size(directory):
    """Returns the `directory` size in bytes."""
    total = 0
    try:
        # print("[+] Getting the size of", directory)
        for entry in os.scandir(directory):
            if entry.is_file():
                # if it's a file, use stat() function
                total += entry.stat().st_size
            elif entry.is_dir():
                # if it's a directory, recursively call this function
                total += get_size(entry.path)
    except NotADirectoryError:
        # if `directory` isn't a directory, get the file size then
        return os.path.getsize(directory)
    except PermissionError:
        # if for whatever reason we can't open the folder, return 0 
        return 0
    return total


def dir_to_text(path,filename):
    Tk().withdraw()
    dirList = os.listdir(path)
    data = ((fname, str(get_size(path + "/" + fname)))  for fname in dirList)

    outputFile = open(filename, 'w')
    for entry in data:
        outputFile.write(','.join(entry) + '\n')

    outputFile.close()

get_saved_paths()

dir_to_text(docs_mods_path,"client_document_mods.csv")
dir_to_text(steam_mods_path,"client_steam_mods.csv")