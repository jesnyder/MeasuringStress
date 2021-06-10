from c0101_retrieve_ref import retrieve_ref
from c0103_save_meta import save_meta
from c0104_retrieve_meta import retrieve_meta
from c0105_record_to_summary import record_to_summary

import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def find_records():
    """
    plot the timestamped data for the temperature
    """

    print("begin find records")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    # sensor_unit_list = retrieve_ref('sensor_unit_list')

    for study in study_list:
        # print('study = ' + str(study))
        source_path = os.path.join('studies', study, 'source')
        # print('source_path = ' + str(source_path))

        source_folders = os.listdir(source_path)
        # print(str(study) + ' source_folders = ')
        # print(source_folders)

        df_meta = pd.DataFrame()
        df_meta['source_path'] = source_folders
        save_meta(study, df_meta)
        record_to_summary(study, 'Records found', str(len(source_folders)))

    print("completed find records")
