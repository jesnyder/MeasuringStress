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

def plot_segment():
    """
    Clean the data
    """

    print("plot segment data")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    segment_list = retrieve_ref('segment_list')
    timePreStudy = retrieve_ref('timePreStudy')
    timePostStudy = retrieve_ref('timePostStudy')

    for study in study_list:
        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])

        for record in source_path:

            row_num, col_num, plot_num = 6, 1, 0
            row_width_mulp, col_width_mulp = 14, 5
            plot_width, plot_height = col_num*row_width_mulp, row_num*col_width_mulp
            plt.figure(figsize=(plot_width, plot_height))

            for sensor in sensor_list:

                # plot the timestamp in unix of timestamped record
                plot_num += 1
                plt.subplot(row_num, col_num, plot_num)

                for segment in segment_list[0:-1]:

                    # print('segment_list')
                    # print(segment_list)

                    analysis_type = segment
                    df = retrieve_analyzed(study, analysis_type, record, sensor)

                    # print(df)

                    valueColor = retrieve_ref_color(str('color_' + str(segment)))
                    plt.scatter(df['timeMinutes'], df['measurement'], color = valueColor, label = str(segment))
                    plt.title( analysis_type + ' ' + record + ' ' + sensor)
                    plt.xlabel('Measurement Count - Before Timestamp')
                    sensor_unit = retrieve_sensor_unit(sensor)
                    plt.ylabel(str(sensor) + ' ( ' + str(sensor_unit) + ' )')
                    plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')


            # save the plot
            plot_path = os.path.join(study, 'plot')
            if not os.path.isdir(plot_path): os.mkdir(plot_path)
            plot_path = os.path.join(study, 'plot', 'segment')
            if not os.path.isdir(plot_path): os.mkdir(plot_path)
            plot_path = os.path.join(study, 'plot', 'segment', record)
            if not os.path.isdir(plot_path): os.mkdir(plot_path)
            plot_file = os.path.join(plot_path, sensor + '.png')
            plt.savefig(plot_file, bbox_inches='tight')
