from c0101_retrieve_ref import retrieve_ref
from c0102_timestamp import timestamp_source
from c0104_plot_timestamp import plot_timestamp
from c0105_find_records import find_records
from c0106_record_to_summary import record_to_summary
from c0108_save_meta import save_meta
from c0109_retrieve_meta import retrieve_meta

import glob
import os
import pandas as pd

def trim_record_to_max():
    """
    Input: path to a csv
    Output: list of timestamps
    """

    print("finding the end of the record")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    max_record_time = retrieve_ref('max_record_time')

    sensor = 'TEMP'

    for study in study_list:

        df_meta = retrieve_meta(study)

        source_path = list(df_meta['source_path'])

        df_meta['recordLength'] = [None] * len(source_path)


        for record in source_path:

            # timestamped_file = os.path.join(study, 'timestamp', record, sensor + ".csv")
            timestamped_file = os.path.join(study, 'formatted', 'source', record, 'All' , sensor + ".csv")
            df_timestamped = pd.read_csv(timestamped_file)

            record_length = max(list(df_timestamped['timeMinutes']))
            if record_length > max_record_time:
                record_length = max_record_time

            record_length = round(record_length, 4)
            i = df_meta[ df_meta['source_path'] == record].index.values[0]
            df_meta.loc[i, 'recordLength' ] = record_length


        # save the record length to meta file
        save_meta(study, df_meta)
