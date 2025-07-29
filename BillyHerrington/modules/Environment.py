import os
import config
import shutil

def create():
    if not os.path.isdir(config.tmp_dir_path):
        os.mkdir(config.tmp_dir_path)

    
def check_old_billy():
    if os.path.isdir(config.old_dir_name):
        return 1
    return 0
    

def delete_old_billy():
    try:
        if os.path.isdir(config.old_dir_name):
            shutil.rmtree(config.old_dir_name)
            return "Successfully deleted"   
           
        return "Old Billy not found"
    except Exception as ex:
        return str(ex)