#-*-coding:utf-8-*-

import os
import re
import win32api
import fnmatch
import stat

def get_file_size(file):
    file.seek(0, 2)
    size = file.tell()
    return size

def find_file(root_folder, file_name):
    founds = []
    rex = re.compile(file_name, re.IGNORECASE)
    print( root_folder)
    for root, dirs, files in os.walk(root_folder):
        for extension in ('*.avi', '*.wmv', '*.mp4', '*.mpg', '*.asf', '*.mov', '*.mkv', '*.iso'):
            #for f in files:
            for f in fnmatch.filter(files, extension):
                result = rex.search(f)
                if result:
                    full_path = os.path.join(root, f)
                    #ignore torrent downloading...
                    if "C:\\Users\\hjchoi\\Documents" in full_path:
                        print('ignore ' + full_path)
                        continue
                    founds.append(full_path)
                    print(full_path + ", size=" + format(os.path.getsize(full_path) / 1000, ','))
                    #break
    return founds

def find_file_in_all_drives(file_name):
    print( 'search : ' + file_name)
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        find_file(drive, file_name)

def move_files(file_name, dest_dir):
    if not dest_dir.endswith('\\'):
        print('dest dir needs to be ends with \\')
        return
    #print( 'search : ' + file_name)
    founds_in_all_drives = []
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        founds_in_all_drives.extend(find_file(drive, file_name))
    for find_file_path in founds_in_all_drives:
        if dest_dir in find_file_path:
            print(find_file_path + ' is dest dir file. pass')
            continue
        dest_path = dest_dir + os.path.basename(find_file_path)
        print('dest : ' + dest_path)
        if os.path.isfile(dest_path):
            print(dest_path + 'is already exists')
            #continue
        else:
            xcopy(find_file_path, dest_dir)
        if os.path.isfile(dest_path):
            print(dest_path + ' copied and delete source file')
            os.chmod(find_file_path, stat.S_IWRITE)
            os.remove(find_file_path)
        
def xcopy(src, dst):
    os.system('xcopy "%s" "%s"' % (src, dst))
    print(src + ' copied')

#find_file_in_all_drives( 'snis(.*)784' )
#find_file_in_all_drives( '농협' )
#find_file('L:\\새 폴더 (12)', 'ebod')
#find_file('L:\\', 'ebod(.*)4')

move_files('ryouka', 'D:\\__collections\\__collection_asakura_ryouka\\')

'''
import os, winshell
from win32com.client import Dispatch

def create_shortcut():
    desktop = winshell.desktop()
    path = os.path.join(desktop, r"D:\new_link.lnk")
    target = r"D:\__collections\__collection_aizawa_haruka\HND-156_aizawa_haruka.mkv"
    w_dir = r"P:path"
    icon = r"P:path"

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = w_dir
    shortcut.IconLocation = icon
    shortcut.save()

create_shortcut()   
'''
