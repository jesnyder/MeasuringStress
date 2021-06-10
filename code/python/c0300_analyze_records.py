from c0101_retrieve_ref import retrieve_ref
from c0101_retrieve_ref import retrieve_ref_color
from c0101_retrieve_ref import retrieve_ref_color_wearable_segment
from c0102_build_path import build_path
from c0104_retrieve_meta import retrieve_meta


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def analyze_records():
    """

    """
    analyze_mean()
    # plot_mean()


def analyze_mean():
    """
    analyze records
    """

    print("begin statistical analysis of records")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    segment_list = retrieve_ref('segment_list')

    for study in study_list:

        df_meta = retrieve_meta(study)



        format_type = 'clean'
        clean_path = os.path.join('studies', study, 'formatted', format_type)
        recordNames = os.listdir(clean_path)

        for sensor in sensor_list:

            for segment in segment_list:

                df_mean = pd.DataFrame()
                df_mean['recordName'] = recordNames

                i = df_meta[ df_meta['recordName']== recordNames[0]].index.values[0]
                coregisterRecords = df_meta.loc[i, 'coregisterRecords' ]

                if len(coregisterRecords) > 2*len(recordNames[0]):
                    colNameSplit = colName.split('_')
                    wearableName = colNameSplit[0]
                    newColName = str(wearableName + '_mean')
                    meanColName = newColName
                    df_mean[newColName] = [None] * len(recordNames)

                    recordRef = recordNames[0]
                    source = os.path.join('studies', study, 'formatted', format_type, recordRef, segment, sensor + '.csv')
                    df = pd.read_csv(source)

                    colNames = list(df.head())
                    for colName in colNames:
                        if str('meas') in str(colName):
                            colNameSplit = colName.split('_')
                            wearableName = colNameSplit[0]
                            newColName = str(wearableName + '_mean')
                            df_mean[newColName] = [None] * len(recordNames)
                            meanColName = newColName

                else:
                    newColName = 'mean'
                    df_mean[newColName] = [None] * len(recordNames)



                for record in recordNames:

                    i = df_meta[ df_meta['recordName']== record].index.values[0]
                    coregisterRecords = df_meta.loc[i, 'coregisterRecords' ]

                    source = os.path.join('studies', study, 'formatted', format_type, record, segment, sensor + '.csv')
                    print('source = ' + str(source))
                    df = pd.read_csv(source)

                    colNames = list(df.head())

                    for colName in colNames:

                        if str('measurement') in str(colName):

                            measurement = list(df[colName])
                            avg = np.mean(measurement)

                            # print('measurement = ')
                            # print(measurement)

                            if len(coregisterRecords) > 2*len(record):
                                colNameSplit = colName.split('_')
                                wearableName = colNameSplit[0]
                                newColName = str(wearableName + '_mean')
                                meanColName = newColName

                            else:
                                newColName = 'mean'

                            j = df_mean[ df_mean['recordName']== record].index.values[0]
                            df_mean.loc[j, newColName ] = round(avg, 4)
                            print('j = ' + str(j) + ' mean = ' + str(avg))


                path = ['studies', study, 'analyzed', 'statistics', 'mean', segment]
                path = build_path(path)
                file = os.path.join(path, sensor + ".csv")
                df_mean.to_csv(file)
                print('mean file saved: ' + file)


        print("completed statistical analysis of records")


def plot_mean():
    """

    """

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    segment_list = retrieve_ref('segment_list')

    for study in study_list:

        row_num, col_num, plot_num = len(sensor_list), 3, 0
        row_width_mulp, col_width_mulp = 6, 6
        plot_width, plot_height = col_num*row_width_mulp, row_num*col_width_mulp
        plt.figure(figsize=(plot_width, plot_height))

        for sensor in sensor_list:

            plot_num += 1
            plt.subplot(row_num, col_num, plot_num)

            for segment in segment_list:

                path = ['studies', study, 'analyzed', 'statistics', 'mean', segment]
                # print('path = ' + path)
                file = os.path.join('studies', study, 'analyzed', 'statistics', 'mean', segment, sensor +  '.csv')
                # file = os.path.join(path, sensor +  '.csv')
                print('file = ' + file)
                df_mean = pd.read_csv(file)

                df_mean = df_mean.dropna()

                colNames = list(df_mean.head())
                for colName in colNames:
                    if 'Unnamed' in colName:
                        del df_mean[colName]

                print('df_mean = ')
                print(df_mean)

                yy = df_mean.iloc[ : , 1]
                print('yy = ')
                print(yy)
                ylabel = colName

                xx = list(range(1, len(yy)+1))
                xlabel = 'Records Num'

                if len(colNames) > 3:
                    xx = df_mean.iloc[ : , 2]
                    xlabel = colNames[-1]

                print('xx = ')
                print(xx)

                assert len(xx) == len(yy)
                assert sum(xx) > -1000000000
                assert sum(yy) > -1000000000


                if segment == 'All':
                    xxsym = np.linspace(min(xx), max(xx), 200)
                    yysym = np.linspace(min(yy), max(yy), 200)
                    plt.scatter(xxsym, yysym, color = [.8, .8, .8])

                wearable_num = 1
                colorWearableSegment = retrieve_ref_color_wearable_segment(wearable_num, segment)

                plt.scatter(xx, yy, color = colorWearableSegment, label = str(segment))

                plt.xlabel(xlabel + ' ' + sensor)
                plt.ylabel(ylabel + ' ' + sensor)

                print('xlabel / ylabel = ' + xlabel + ' ' + ylabel)

                if sensor == sensor_list[-1]:
                    plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')


        path = ['studies', study, 'plotted', 'analysis', 'mean']
        path = build_path(path)
        file = os.path.join(path, sensor + ".png")
        plt.savefig(file, bbox_inches='tight')
        print('plotted mean = ' + file)
