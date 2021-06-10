from c0101_retrieve_ref import retrieve_ref


import os
import pandas as pd
from shutil import copyfile


def latex_report(comprehensive_report):
    """
    Create a comprehensive report
    Compile the text and figures into a single pdf
    """

    # retrieve variables needed to find the figures
    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    analysis_list = retrieve_ref('analysis_list')

    # create a fle that has all the text and figures
    dst = open(comprehensive_report, 'a')

    # copy the text of the latex document to the report file
    src = os.path.join('code', 'latex', 'manuscript' + '.txt')
    file = open(src, 'r')
    dst.write(file.read())


    # close the latex file, still a .txt file extension
    dst.close()
