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

def plot_timestamp():
    """
    compare the curves to verify the end of the record was properly found
    plot the source measurements for temperature
    plot the timestamped data for the temperature
    plot the truncated data
    plot the timestamped and truncated on the same plot
    """

    print("begin plotting timestamped data")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    analysis_list = retrieve_ref('analysis_list')

    for study in study_list:

        metadata_path = os.path.join(study, 'meta')
        metadata_file = os.path.join(metadata_path, 'metadata.csv')
        df_meta = pd.read_csv(metadata_file)
        # print(df_meta)

    # timestamp temp
    sensor = 'TEMP'
    for study in study_list:

        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])

        for record in source_path:

            row_num, col_num, plot_num = 4, 1, 0
            row_width_mulp, col_width_mulp = 14, 5
            plot_width, plot_height = col_num*row_width_mulp, row_num*col_width_mulp
            plt.figure(figsize=(plot_width, plot_height))

            # plot the timestamp in unix of timestamped record
            plot_num += 1
            plt.subplot(row_num, col_num, plot_num)
            analysis_type = 'source'
            df = retrieve_analyzed(study, analysis_type, record, sensor)
            valueColor = retrieve_ref_color(str('color_' + str(analysis_type)))
            plt.scatter(df['count'], df['measurement'], color = valueColor, label = str(analysis_type))
            plt.title( analysis_type + ' ' + record + ' ' + sensor)
            plt.xlabel('Measurement Count - Before Timestamp')
            sensor_unit = retrieve_sensor_unit(sensor)
            plt.ylabel(str(sensor) + ' ( ' + str(sensor_unit) + ' )')
            plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')

            # plot the timestamp in unix of timestamped record
            plot_num += 1
            plt.subplot(row_num, col_num, plot_num)
            analysis_type = 'timestamp'
            df = retrieve_analyzed(study, analysis_type, record, sensor)
            valueColor = retrieve_ref_color(str('color_' + str(analysis_type)))
            plt.scatter(df['timeMinutes'], df['measurement'], color = valueColor, label = str(analysis_type))
            plt.title( analysis_type + ' ' + record + ' ' + sensor)
            plt.xlabel('Time (Unix)')
            sensor_unit = retrieve_sensor_unit(sensor)
            plt.ylabel(str(sensor) + ' ( ' + str(sensor_unit) + ' )')
            plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')
            # plot both the original and the truncated record
            plot_num += 1
            plt.subplot(row_num, col_num, plot_num)
            for analysis_type in analysis_list:
                df = retrieve_analyzed(study, analysis_type, record, sensor)
                valueColor = retrieve_ref_color(str('color_' + str(analysis_type)))
                plt.scatter(df['timeMinutes'], df['measurement'], color = valueColor, label = str(analysis_type))
            plt.title( analysis_type + ' ' + record + ' ' + sensor)
            plt.xlabel('Time (minutes)')
            sensor_unit = retrieve_sensor_unit(sensor)
            plt.ylabel(str(sensor) + ' ( ' + str(sensor_unit) + ' )')
            plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')



            # plot the truncated record
            plot_num += 1
            plt.subplot(row_num, col_num, plot_num)
            analysis_type = 'truncate'
            df = retrieve_analyzed(study, analysis_type, record, sensor)
            valueColor = retrieve_ref_color(str('color_' + str(analysis_type)))
            plt.scatter(df['timeMinutes'], df['measurement'], color = valueColor, label = str(analysis_type))
            plt.title( analysis_type + ' ' + record + ' ' + sensor)
            plt.xlabel('Time (minutes)')
            sensor_unit = retrieve_sensor_unit(sensor)
            plt.ylabel(str(sensor) + ' ( ' + str(sensor_unit) + ' )')
            plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')


            # save the plot
            plot_path = os.path.join(study, 'plot')
            if not os.path.isdir(plot_path): os.mkdir(plot_path)
            plot_path = os.path.join(study, 'plot', 'timestamp')
            if not os.path.isdir(plot_path): os.mkdir(plot_path)
            plot_path = os.path.join(study, 'plot', 'timestamp', record)
            if not os.path.isdir(plot_path): os.mkdir(plot_path)
            plot_file = os.path.join(plot_path, sensor + '.png')
            plt.savefig(plot_file, bbox_inches='tight')

    print("completed plotting timestamped data")
