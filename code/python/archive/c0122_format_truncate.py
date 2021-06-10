from c0101_retrieve_ref import retrieve_ref
from c0102_timestamp import timestamp_source
from c0103_trim_record_to_max import trim_record_to_max
from c0104_plot_timestamp import plot_timestamp
from c0105_find_records import find_records
from c0106_record_to_summary import record_to_summary
from c0107_decide_inclusion import decide_inclusion
from c0108_save_meta import save_meta
from c0109_retrieve_meta import retrieve_meta
from c0110_find_temp_end import find_temp_end
from c0111_retrieve_analyzed import retrieve_analyzed
from c0112_plot_truncate import plot_truncate
from c0113_plot_acc import plot_acc
from c0114_segment_data import segment_data
from c0115_plot_segment import plot_segment
from c0116_find_pairs import find_pairs
from c0117_find_paired_end import find_paired_end
from c0118_find_paired_duration import find_paired_duration


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def format_truncate():
    """
    timestamp the source
    """

    print("begin format source")

    study_list = retrieve_ref('study_list')
    format_types = retrieve_ref('format_types')
    segment_list = retrieve_ref('segment_list')
    sensor_list = retrieve_ref('sensor_list')


    format_type = 'source'
    segment = 'All'

    for study in study_list:

        # print('study = ' + str(study))

        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])

        for record in source_path:

            i = df_meta[ df_meta['source_path']== record].index.values[0]
            truncatedLength = df_meta.loc[i, 'truncatedLength' ]

            for sensor in sensor_list:

                df = retrieve_analyzed(study, format_type, record, segment, sensor)
                df = df.drop(df[df['timeMinutes'] > truncatedLength].index)


                # create the path to where timestamped data is saved
                timestamped_path = os.path.join(study)
                if not os.path.isdir(timestamped_path): os.mkdir(timestamped_path)

                timestamped_path = os.path.join(timestamped_path, str('formatted'))
                if not os.path.isdir(timestamped_path): os.mkdir(timestamped_path)

                timestamped_path = os.path.join(timestamped_path, str('truncate'))
                if not os.path.isdir(timestamped_path): os.mkdir(timestamped_path)

                timestamped_path = os.path.join(timestamped_path, str(record))
                if not os.path.isdir(timestamped_path): os.mkdir(timestamped_path)

                timestamped_path = os.path.join(timestamped_path, str(segment))
                if not os.path.isdir(timestamped_path): os.mkdir(timestamped_path)

                timestamped_file = os.path.join(timestamped_path, sensor + ".csv")

                # print('timestamped_file = ' + str(timestamped_file))
                df.to_csv(timestamped_file)

                print('format truncate file saved = ' + str(timestamped_file))
