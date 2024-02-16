import os
import re
import win32api


def find_file(root_folder, rex):
    results = []
    for root, dirs, files in os.walk(root_folder):
        for f in files:
            result = rex.search(f)
            if result:
                print(os.path.join(root, f))
                results.append(os.path.join(root, f))
                return results


def find_file_in_all_drives(file_name):
    # create a regular expression for the file
    rex = re.compile(file_name)
    for drive in win32api.GetLogicalDriveStrings().split("\000")[:-1]:
        print(drive)
        find_file(drive, rex)
