#-*-coding:utf-8-*-

import os
import re
import win32api
import fnmatch
import stat
from symlink import *

def get_file_size(file):
    file.seek(0, 2)
    size = file.tell()
    return size

def xcopy(src, dst):
    os.system('xcopy "%s" "%s"' % (src, dst))

def remove_file(path):
    os.chmod(path, stat.S_IWRITE)
    os.remove(path)

def find_file(root_folder, file_name, ignore_path = None):
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
                    #ignore path patterns
                    if not (ignore_path is None) and (ignore_path in full_path):
                        print('ignore path ' + ignore_path)
                        continue
                    if r"C:\Users\hjchoi\Documents" in full_path:   # downloading torrent
                        print('ignore ' + full_path)
                        continue
                    if r"C:\Windows\Sys" in full_path:      # why some files found in system folders? 
                        print('ignore system ' + full_path)
                        continue
                    if full_path.endswith(SYMLINK_SUFFIX):
                        print('ignore symlink file ' + full_path)
                        continue
                    founds.append(full_path)
                    print(full_path + ", size=" + format(os.path.getsize(full_path) / 1000, ','))
    return founds

def find_file_in_all_drives(file_name, ignore_path = None):
    print( 'search : ' + file_name)
    all_founds = []
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        all_founds.extend(find_file(drive, file_name, ignore_path))
    return all_founds

def move_files(file_name, dest_dir):
    if not dest_dir.endswith('\\'):
        print('dest dir needs to be ends with \\')
        return

    founds_in_all_drives = find_file_in_all_drives(file_name, dest_dir)

    print('found results : ' + str(len(founds_in_all_drives)))
    for find_file_path in founds_in_all_drives:
        if dest_dir in find_file_path:
            print(find_file_path + ' is dest dir file. pass')
            continue
        dest_path = dest_dir + os.path.basename(find_file_path)
        print('dest : ' + dest_path)
        if not os.path.isfile(dest_path):
            #print('\tdummy call copy : ' + find_file_path)
            xcopy(find_file_path, dest_dir)
            print('\t' + find_file_path + ' copied')
            if os.path.isfile(dest_path):
                print('\t' + dest_path + ' copied and delete source file')
                remove_file(find_file_path)
        else:
            print('\t' + dest_path + 'is already exists')

def remove_dup_files_in_dest(file_name, dest_dir):
    founds = find_file_in_all_drives(file_name, dest_dir)

    for path in founds:
        dest_path = dest_dir + os.path.basename(path)
        if os.path.isfile(dest_path):
            print('call remove ' + path)
            remove_file(path)
            
def create_symlinks(search_text, dest_dir):
    founds = find_file_in_all_drives(search_text)
    print('founds : ' + str(len(founds)))
    for file_path in founds:
        if dest_dir in file_path:
            continue    #pass if search file is in dest dir
        link_name = os.path.basename(file_path) + symlink.SYMLINK_SUFFIX
        link_path = os.path.join(dest_dir, link_name)
        if os.path.isfile(link_path):
            continue    #pass if already exists
        print('link path : ' + link_path)
        symlink(file_path, link_path)


#===================================================
# run
#===================================================

search_text = 'aso_haruka'
#search_text = 'jux(.*)922'
dest_dir = 'D:\\__collections\\__collection_aso_haruka\\'

#remove_dup_files_in_dest(search_text, dest_dir)
find_file_in_all_drives( search_text )
#find_file('L:\\새 폴더 (12)', search_text)
#move_files(search_text, dest_dir)
#create_symlinks(search_text, dest_dir)

#symlink(r'J:\새 폴더\snis672.avi', r'snis_links\snis672.avi')
