from c0101_retrieve_ref import retrieve_ref
from c0101_retrieve_ref import retrieve_ref_color
from c0101_retrieve_ref import retrieve_sensor_unit
from c0102_build_path import build_path


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_acc(study):
    """

    """

    print('compare ACC sensors')

    format_type, sensor, segment = 'truncate', 'ACC', 'All'
    source_path = os.path.join('studies', study, 'formatted', format_type)
    format_folders = os.listdir(source_path)

    for record in format_folders:

        row_num, col_num, plot_num = 5, 1, 0
        row_width_mulp, col_width_mulp = 14, 5
        plot_width, plot_height = col_num*row_width_mulp, row_num*col_width_mulp
        plt.figure(figsize=(plot_width, plot_height))

        source = os.path.join('studies', study, 'formatted', format_type, record, segment, sensor + '.csv')

        if os.path.isfile(source):

            print('source = ' + source)

            df = pd.read_csv(source)

            colNames = list(df.head())
            print('colNames = ')
            print(colNames)

            for colName in colNames:

                if str('eas') in str(colName):

                    plot_num += 1
                    plt.subplot(row_num, col_num, plot_num)

                    labelName = colName
                    print('labelName = ' + labelName)

                    valueColor = retrieve_ref_color(str('color_' + str(sensor) + '_' + str(colName)))
                    plt.scatter(df['timeUnix'], df[colName], color = valueColor, label = labelName)

                    plt.xlabel('time Unix')
                    sensor_unit = retrieve_sensor_unit(sensor)
                    plt.ylabel(sensor + ' ' + sensor_unit )
                    plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')


            plot_num += 1
            plt.subplot(row_num, col_num, plot_num)

            for colName in colNames:

                if str('eas') in str(colName):

                    labelName = colName
                    print('labelName = ' + labelName)

                    valueColor = retrieve_ref_color(str('color_' + str(sensor) + '_' + str(colName)))
                    plt.scatter(df['timeUnix'], df[colName], color = valueColor, label = labelName)


            plt.xlabel('time (Unix)')
            sensor_unit = retrieve_sensor_unit(sensor)
            plt.ylabel(sensor + ' ' + sensor_unit )
            plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')


        path = ['studies', study, 'plotted', format_type, record]
        path = build_path(path)
        file = os.path.join(path, sensor + ".png")
        plt.savefig(file, bbox_inches='tight')
        print('acc saved: ' + file)
