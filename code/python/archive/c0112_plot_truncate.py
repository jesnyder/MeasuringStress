from c0101_retrieve_ref import retrieve_ref
from c0101_retrieve_ref import retrieve_ref_color
from c0101_retrieve_ref import retrieve_sensor_unit
from c0102_timestamp import timestamp_source
from c0109_retrieve_meta import retrieve_meta
from c0111_retrieve_analyzed import retrieve_analyzed


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_truncate():
    """
    compare the curves to verify the end of the record was properly found
    plot the source measurements for temperature
    plot the timestamped data for the temperature
    plot the truncated data
    plot the timestamped and truncated on the same plot
    """

    print("begin plotting truncated data")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    analysis_list = retrieve_ref('analysis_list')


    analysis_type = 'truncate'

    for study in study_list:

        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])

        for record in source_path:

            row_num, col_num, plot_num = len(sensor_list), 1, 0
            plot_width, plot_height = col_num*25, row_num*6
            plt.figure(figsize=(plot_width, plot_height))

            for sensor in sensor_list:

                # plot the truncated record
                plot_num += 1
                plt.subplot(row_num, col_num, plot_num)
                df = retrieve_analyzed(study, analysis_type, record, sensor)
                valueColor = retrieve_ref_color(str('color_' + str(analysis_type)))
                plt.scatter(df['timeMinutes'], df['measurement'], color = valueColor, label = str(analysis_type))
                plt.title( analysis_type + ' ' + record + ' ' + sensor)
                plt.xlabel('Time (minutes)')
                sensor_unit =retrieve_sensor_unit(sensor)
                plt.ylabel(str(sensor) + ' ( ' + str(sensor_unit) + ' )')
                plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')


            # save the plot
            plot_path = os.path.join(study, 'plot')
            if not os.path.isdir(plot_path): os.mkdir(plot_path)
            plot_path = os.path.join(study, 'plot', analysis_type)
            if not os.path.isdir(plot_path): os.mkdir(plot_path)
            plot_path = os.path.join(study, 'plot', analysis_type, record)
            if not os.path.isdir(plot_path): os.mkdir(plot_path)
            plot_file = os.path.join(plot_path, sensor + '.png')
            plt.savefig(plot_file, bbox_inches='tight')

            print('plotting truncated data for: '  + str(plot_file))

    print("completed plotting truncated data")
