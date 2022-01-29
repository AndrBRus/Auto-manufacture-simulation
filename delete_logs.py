import os # use for search path to file and delete files in folder
import sys # use to system definitions

# This function clears the log folder before the next modeling run
def delete_logs():
    # catch errors (tesing)
    try: 
        # search path
        path = str(os.path.dirname(os.path.abspath('manufacture.py')))

        # go to directory
        # if Linux or MAC OS system
        if sys.platform == 'darwin' or sys.platform == 'linux':
            os.chdir(path + '/logs/')
        # if Windows system
        elif sys.platform == 'win32':
            os.chdir(path + '\\logs\\')
        
        # delete all files in directory
        for file in os.listdir():
            os.remove(file)

        # return to main folder
        os.chdir(path)
        
    # except all exceptions (testing)
    except Exception as ex:
        print(ex)