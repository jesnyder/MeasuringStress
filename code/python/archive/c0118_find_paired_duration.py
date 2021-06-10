from c0101_retrieve_ref import retrieve_ref
from c0101_retrieve_ref import retrieve_ref_color
from c0101_retrieve_ref import retrieve_sensor_unit
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

import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def find_paired_duration():
    """
    Find the duration of the record
    Add the end of the coregistered record in the meta file
    """

    print("begin find_paired_duration")

    study_list = retrieve_ref('study_list')

    for study in study_list:

        df_meta = retrieve_meta(study)
        # print(df_meta)
        source_path = list(df_meta['source_path'])

        # add emptyt column
        df_meta['recordDuration'] = [None] * len(source_path)

        for record in source_path:

            # save that value in the dataframe
            i = df_meta[ df_meta['source_path'] == record].index.values[0]
            print('i = ' + str(i))

            recordBegin = int(df_meta.loc[i, 'recordBegin' ] )
            print('recordBegin = ' + str(recordBegin))

            recordEnd = int(df_meta.loc[i, 'recordEnd' ] )
            print('recordEnd = ' + str(recordEnd))

            recordDuration =  round((recordEnd - recordBegin)/60 , 4)

            df_meta.loc[i, 'recordDuration' ] = recordDuration

            print('recordDuration = ' + str(recordDuration))

        save_meta(study, df_meta)
        print('df_meta = ')
        print(df_meta)
