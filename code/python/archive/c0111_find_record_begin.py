from c0101_retrieve_ref import retrieve_ref
from c0102_build_path import build_path
from c0103_save_meta import save_meta
from c0104_retrieve_meta import retrieve_meta
from c0105_record_to_summary import record_to_summary

from c0107_timestamp_source import timestamp_source


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def find_record_end():
    """
    timestamp the source
    """

    print("begin timestamp source")

    study_list = retrieve_ref('study_list')
    format_types = retrieve_ref('format_types')
    segment_list = retrieve_ref('segment_list')
    sensor_list = retrieve_ref('sensor_list')

    # timestamp temp
    format_type = 'source'
    segment = 'All'
    sensor = 'TEMP'

    for study in study_list:

        print('study = ' + str(study))

        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])

        df_meta['recordBegin'] = [None] * len(source_path)
        df_meta['recordEnd'] = [None] * len(source_path)
        df_meta['fullLength'] = [None] * len(source_path)

        # summarize what has been found so far
        record_to_summary(study, 'Records found', len(source_path))

        for record in source_path:
            # source = os.path.join(study, 'source', record, sensor + '.csv')
            df_timestamped = timestamp_source(study, format_type, segment, record, sensor)


            # Save the full length of the uneditted record
            i = df_meta[ df_meta['source_path']== record].index.values[0]
            recordSplit = record.split('_')
            df_meta.loc[i, 'recordBegin' ] = int(recordSplit[0])
            df_meta.loc[i, 'recordEnd' ] = int(recordSplit[0]) + 60*(max(df_timestamped['timeMinutes']))
            df_meta.loc[i, 'fullLength' ] = round(max(df_timestamped['timeMinutes']) , 4)


        save_meta(study, df_meta)


    find_temp_end()

    """
    trim_record_to_max()



    decide_inclusion()
    """
