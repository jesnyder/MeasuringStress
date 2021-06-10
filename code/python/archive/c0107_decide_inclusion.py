from c0101_retrieve_ref import retrieve_ref
from c0102_timestamp import timestamp_source
from c0103_trim_record_to_max import trim_record_to_max
from c0104_plot_timestamp import plot_timestamp
from c0105_find_records import find_records
from c0106_record_to_summary import record_to_summary
from c0108_save_meta import save_meta
from c0109_retrieve_meta import retrieve_meta


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def decide_inclusion():
    """
    Determine inclusion based on length of the record
    """

    print("begin decide inclusion")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    max_record_time = retrieve_ref('max_record_time')
    min_record_time = retrieve_ref('min_record_time')

    for study in study_list:

        df_meta = retrieve_meta(study)
        df_meta = df_meta.sort_values(by=['recordLength'])

        records_found = list(df_meta['source_path'])
        recordLength = list(df_meta['recordLength'])

        inclusionList = []
        for i in range(len(recordLength)):

            if recordLength[i] < min_record_time:
                inclusionList.append('excluded')

            else:
                inclusionList.append('included')

        # save the record length to meta file
        df_meta['included'] = inclusionList
        save_meta(study, df_meta)

        df_meta = df_meta.drop(df_meta[df_meta['included'] == 'excluded'].index)
        df_meta = df_meta.sort_values(by=['source_path'])
        save_meta(study, df_meta)

    print("completed decide inclusion")
