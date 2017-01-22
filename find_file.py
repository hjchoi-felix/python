#-*-coding:utf-8-*-

import os
import re
import win32api
import fnmatch

def find_file(root_folder, file_name):
    rex = re.compile(file_name, re.IGNORECASE)
    print( root_folder)
    for root, dirs, files in os.walk(root_folder):
        for extension in ('*.avi', '*.wmv', '*.mp4', '*.mpg', '*.asf', '*.mov', '*.mkv', '*.iso'):
            #for f in files:
            for f in fnmatch.filter(files, extension):
                result = rex.search(f)
                if result:
                    print(os.path.join(root, f))
                    #break

def find_file_in_all_drives(file_name):
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        find_file(drive, file_name)

find_file_in_all_drives( 'star(.*)749' )
#find_file('L:\\새 폴더 (12)', 'ebod')
#find_file('L:\\', 'ebod(.*)4')
