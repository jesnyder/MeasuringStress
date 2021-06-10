from c0101_retrieve_ref import retrieve_ref
from c0101_retrieve_ref import retrieve_ref_color
from c0101_retrieve_ref import retrieve_sensor_unit
from c0101_retrieve_ref import retrieve_ref_color_wearable_segment
from c0102_build_path import build_path

import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



def plot_segment(study):
    """

    """

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    segment_list = retrieve_ref('segment_list')
    segment_list.reverse()


    format_type = 'clean'
    source_path = os.path.join('studies', study, 'formatted', format_type)
    format_folders = os.listdir(source_path)

    format_types = ['clean']

    for record in format_folders:

        row_num, col_num, plot_num = len(sensor_list), 1, 0
        row_width_mulp, col_width_mulp = 14, 5
        plot_width, plot_height = col_num*row_width_mulp, row_num*col_width_mulp
        plt.figure(figsize=(plot_width, plot_height))

        for sensor in sensor_list:

            plot_num += 1
            plt.subplot(row_num, col_num, plot_num)

            for format_type in format_types:

                segment = 'All'

                source = os.path.join('studies', study, 'formatted', format_type, record, segment, sensor + '.csv')

                if os.path.isfile(source):

                    print('source = ' + source)

                    df = pd.read_csv(source)

                    colNames = list(df.head())
                    print('colNames = ')
                    print(colNames)

                    for colName in colNames:

                        if str('measurement') in str(colName):

                            colNameSplit = colName.split('_')
                            labelName = str(format_type + ' ' + colNameSplit[0])
                            print('labelName = ' + labelName)
                            index_col = df.columns.get_loc(colName)
                            wearable_num = len(colNames) - index_col
                            print('wearable_num = ' + str(wearable_num))
                            colorWearableSegment = retrieve_ref_color_wearable_segment(wearable_num, segment)

                            plt.scatter(df['timeMinutes'], df[colName], color = colorWearableSegment, label = labelName)


            plt.xlabel('Record Time (minutes)')
            sensor_unit = retrieve_sensor_unit(sensor)
            plt.ylabel(sensor + ' ' + sensor_unit )
            plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')


        path = ['studies', study, 'plotted', 'coregister', record]
        path = build_path(path)
        file = os.path.join(path, sensor + ".png")
        plt.savefig(file, bbox_inches='tight')
