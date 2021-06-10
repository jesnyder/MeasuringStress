from c0101_retrieve_ref import retrieve_ref
from c0102_build_path import build_path


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def analyze_records():
    """
    analyze records
    """

    print("begin statistical analysis of records")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    segment_list = retrieve_ref('segment_list')

    quanList = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    format_type = 'clean'

    for study in study_list:

        source_path = os.path.join('studies', study, 'formatted', format_type)
        format_folders = os.listdir(source_path)

        record, segment, sensor = str(format_folders[0]), 'All', 'TEMP'
        source = os.path.join('studies', study, 'formatted', format_type, record, segment, sensor + '.csv')
        df = pd.read_csv(source)

        df_quans = pd.DataFrame()
        df_quans['recordName'] = format_folders

        colNames = list(df.head())
        for colName in colNames:
            if str('measurement') in str(colName):
                colNameSplit = colName.split('_')
                print('colNameSplit = ')
                print(colNameSplit)
                wearableName = colNameSplit[1]

                for quan in quanList:
                    dfColName = str('quan' + str(quan) + '_' + wearableName)
                    df_quans[dfColName] = [None] * len(format_folders)

        print('df_quans = ')
        print(df_quans)

        for sensor in sensor_list:

            for segment in segment_list:

                for record in format_folders:

                    source = os.path.join('studies', study, 'formatted', format_type, record, segment, sensor + '.csv')
                    df = pd.read_csv(source)
                    print('clean file retrieved: ' + source)

                    i = df_quans[ df_quans['recordName']== record].index.values[0]
                    print('i = ' + str(i))

                    colNames = list(df.head())
                    for colName in colNames:

                        if str('measurement') in str(colName):

                            measurement = list(df[colName])
                            print('measurement = ')
                            print(measurement[0:100])

                            for quan in quanList:

                                dfColName = str('quan' + str(quan) + '_' + wearableName)
                                df_quans.loc[i, dfColName ] = np.quantile(measurement, quan)

                path = ['studies', study, 'analyzed', 'statistics', 'quantiles']
                path = build_path(path)
                file = os.path.join(path, sensor + ".csv")
                df_quans.to_csv(file)
                print('quantile file saved: ' + file)

        print("completed statistical analysis of records")
