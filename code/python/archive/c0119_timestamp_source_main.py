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


def timestamp_source_main():
    """
    timestamp the source
    """

    print("begin timestamp source")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')

    # timestamp temp
    sensor = 'TEMP'
    for study in study_list:

        print('study = ' + str(study))

        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])

        # summarize what has been found so far
        record_to_summary(study, 'Records found', len(source_path))

        for record in source_path:
            # source = os.path.join(study, 'source', record, sensor + '.csv')
            analysis_type = 'timestamp'
            df_timestamped = timestamp_source(analysis_type, study, record, sensor)
