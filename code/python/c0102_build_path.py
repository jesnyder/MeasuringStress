
import glob
import os
import pandas as pd

def build_path(path_list):
    """
    build a directory of folders
    from a list of strings
    """

    # print("begin building path for path_list = " + str(path_list))

    path_incremental = []

    for item in path_list:

        path_incremental.append(item)
        path = os.path.join(*path_incremental)
        # print('path = ' + str(path))

        if not os.path.isdir(path):
            os.mkdir(path)
            print('path made: ' + str(path))

    return(path)
