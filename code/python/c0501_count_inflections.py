from c0101_retrieve_ref import retrieve_ref
from c0101_retrieve_ref import retrieve_ref_color
from c0101_retrieve_ref import retrieve_ref_color_wearable_segment
from c0101_retrieve_ref import retrieve_sensor_unit
from c0102_build_path import build_path
from c0104_retrieve_meta import retrieve_meta

from c0118_segment_formatted import segment_df

from c0401_calculate_regression import calculate_regression
from c0403_plot_regression import plot_regression


import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import statistics
import sympy as sym


def count_inflections():
    """

    """

    print('begin counting inflections')


    searchRange = retrieve_ref('searchRange')
    searchRange.reverse()

    find_inflections()
    list_unique_inflections()
    segment_inflections()
    plot_inflections()

    print('completed counting inflections')



def find_inflections(range, buffer):
    """

    """

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    segment_list = retrieve_ref('segment_list')
    searchRange = retrieve_ref('searchRange')

    for study in study_list:

        format_type = 'clean'
        clean_path = os.path.join(study, 'formatted', format_type)
        recordNames = os.listdir(clean_path)

        for sensor in sensor_list:

            for record in recordNames:

                segment = "All"
                path = [study, 'analyzed', 'inflections', 'all_times', str(range), record, segment]
                path = build_path(path)
                file = os.path.join(path, sensor + ".csv")

                if os.path.isfile(file):
                    continue

                source = os.path.join(study, 'formatted', format_type, record, segment, sensor + '.csv')
                print('source = ' + source)
                df = pd.read_csv(source)

                # print('df[timeMinutes] = ')
                # print(list(df['timeMinutes']))

                for colName in df.columns:

                    if 'Unnamed' in str(colName):
                        del df[colName]
                        print('deleted ' + colName)
                        continue

                    if 'meas' in colName:

                        colNameSplit = colName.split('_')
                        print('colNameSplit = ')
                        print(colNameSplit)
                        print('colNameSplit[0] = ')
                        print(colNameSplit[0])

                        for suffix in ['inflection', 'coefficients', 'derivativeZero', 'equation', 'derivative']:

                            label = str(colNameSplit[0] + '_' + suffix)
                            print('label = ' + label)
                            if label not in df.columns:
                                df[label] = [None]*len((list(df['timeMinutes'])))

                        df['timeBegin'] = [None]*len((list(df['timeMinutes'])))
                        df['timeEnd'] = [None]*len((list(df['timeMinutes'])))

                        for timeMinute in list(df['timeMinutes']):

                            i = df[ df['timeMinutes']== timeMinute].index.values[0]
                            # print('i = '  + str(i))

                            timeTolerance = (float(df.loc[2,'timeMinutes']) - float(df.loc[1,'timeMinutes'])) / 2
                            iRange = int(range/60*1/(timeTolerance*2))
                            # print('iRange = ' + str(iRange))

                            if len(list(df['timeMinutes'])) - i <= iRange+2:
                                continue

                            timeMedian = df.loc[int(i+iRange/2), 'timeMinutes']
                            timeBegin = df.loc[int(i), 'timeMinutes']
                            timeEnd = df.loc[int(i+iRange), 'timeMinutes']

                            # print('timeMedian = ' + str(timeMedian) + ' timeBegin = ' + str(timeBegin) + ' timeEnd = ' + str(timeEnd))
                            # print('range = ' + str(range/60) +  ' timeEnd-timeBegin = ' + str(timeEnd-timeBegin) + ' % = ' + str(range/60/(timeEnd-timeBegin)))

                            df_truncate = df[df['timeMinutes'] >= timeMinute]
                            df_truncate = df_truncate[df_truncate['timeMinutes'] <= timeMinute + range/60]
                            # df_truncate = df[df['timeMinutes'] >= timeMinute & df_truncate['timeMinutes'] <= timeMinute + range/60]

                            timeTruncate = list(df_truncate['timeMinutes'])
                            df.loc[int(i+iRange/2), 'timeBegin'] = min(timeTruncate)
                            df.loc[int(i+iRange/2), 'timeEnd'] = max(timeTruncate)

                            measTruncate = list(df_truncate[colName])

                            coef = np.polyfit(timeTruncate, measTruncate, 2)
                            # coef = [float(x) for x in coef]

                            x = sym.Symbol('x')

                            f = coef[0]*x*x+coef[1]*x+coef[2]
                            # print('f = ')
                            # print(f)

                            dff = sym.diff(f,x)
                            # print('dff = ')
                            # print(dff)

                            solf = sym.solve(f)
                            soldf = sym.solve(dff)
                            soldf = soldf[0]


                            label = str(colNameSplit[0] + '_' + 'inflection')
                            df.loc[int(i+iRange/2), label] = 'No'

                            label = str(colNameSplit[0] + '_' + 'coefficients')
                            df.loc[int(i+iRange/2), label] = str(''.join([str(x) for x in coef]))

                            label = str(colNameSplit[0] + '_' + 'derivativeZero')
                            df.loc[int(i+iRange/2), label] = soldf

                            label = str(colNameSplit[0] + '_' + 'equation')
                            df.loc[int(i+iRange/2), label] = str(f)

                            label = str(colNameSplit[0] + '_' + 'derivative')
                            df.loc[int(i+iRange/2), label] = str(dff)

                            if soldf > min(timeTruncate):

                                if soldf < max(timeTruncate):

                                    if soldf < timeMedian + timeTolerance:

                                        if soldf > timeMedian - timeTolerance:

                                            print('inflection found at time = ' + str(soldf))
                                            label = str(colNameSplit[0] + '_' + 'inflection')
                                            df.loc[int(i+iRange/2), label] = 'Yes'


                df.to_csv(file)
                print('inflection list saved : ' + file)

                for colName in df.columns:

                    if 'inflection' in colName:

                        colNameSplit = colName.split('_')
                        label = str(colNameSplit[0] + '_' + 'inflection')
                        df = df.drop(df[(df[label] != 'Yes')].index)

                path = [study, 'analyzed', 'inflections', 'inflection_only', str(range), record, segment]
                path = build_path(path)
                file = os.path.join(path, sensor + ".csv")
                df.to_csv(file)



def segment_inflections():
    """

    """

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    segment_list = retrieve_ref('segment_list')
    searchRange = retrieve_ref('searchRange')

    for study in study_list:

        format_type = 'clean'
        clean_path = os.path.join(study, 'formatted', format_type)
        recordNames = os.listdir(clean_path)

        for sensor in sensor_list:

            for record in recordNames:

                for range in searchRange:

                    for segment in segment_list:

                        if segment == 'All':
                            continue

                        segmentRef = 'All'
                        path = [study, 'analyzed', 'inflections', 'all_times', str(range), record, segmentRef]
                        path = build_path(path)
                        file = os.path.join(path, sensor + ".csv")

                        if os.path.isfile(file):

                            df = pd.read_csv(file)

                            for colName in df.columns:
                                if 'Unnamed' in str(colName):
                                    del df[colName]

                            df = segment_df(segment, df)
                            path = [study, 'analyzed', 'inflections', 'all_times', str(range), record, segmentRef]
                            path = build_path(path)
                            file = os.path.join(path, sensor + ".csv")

                            df.to_csv(file)



def plot_inflections():
    """

    """

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    segment_list = retrieve_ref('segment_list')
    searchRange = retrieve_ref('searchRange')

    for study in study_list:

        for sensor in sensor_list:

            format_type = 'clean'
            clean_path = os.path.join(study, 'formatted', format_type)
            recordNames = os.listdir(clean_path)

            for sensor in sensor_list:

                for record in recordNames:

                    row_num, col_num, plot_num = len(searchRange), 2, 0
                    row_width_mulp, col_width_mulp = 7, 5
                    plot_width, plot_height = col_num*row_width_mulp, row_num*col_width_mulp
                    plt.figure(figsize=(plot_width, plot_height))

                    for range in searchRange:

                        plot_num += 1
                        plt.subplot(row_num, col_num, plot_num)

                        format_type = 'clean'
                        segment = 'All'

                        path = [study, 'analyzed', 'inflections', 'all_times', str(range), record, segment]
                        path = build_path(path)
                        file = os.path.join(path, sensor + ".csv")

                        if os.path.isfile(file):

                            source = os.path.join(study, 'formatted', format_type, record, segment, sensor + '.csv')
                            print('source = ' + source)
                            df = pd.read_csv(source)

                            for colName in df.columns:
                                if 'timeMinutes' in colName:
                                    timeMinutes = list(df[colName])

                                if 'meas' in colName:
                                    measList = list(df[colName])
                                    measMin = min(measList)
                                    measMax = max(measList)
                                    plt.scatter(timeMinutes, measList, label = str(colName))


                            df = pd.read_csv(file)
                            for colName in df.columns:

                                if 'inflection' in colName:

                                    df = df.drop(df[(df[colName] != 'Yes')].index)

                            timeInflections = list(df['timeMinutes'])

                            for time in timeInflections:

                                xx = np.linspace( time, time, 100)
                                yy = np.linspace( measMin, measMax, 100)
                                plt.plot(xx, yy, color=[0,.9,.6])

                            plt.xlabel('time Unix')
                            sensor_unit = retrieve_sensor_unit(sensor)
                            plt.ylabel(sensor + ' ' + sensor_unit )
                            # plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')
                            plt.title('Record = ' + str(record) + ' Range = ' + str(range) + ' seconds')


                    path = [study, 'plotted', 'inflection', 'each_record', record]
                    path = build_path(path)
                    file = os.path.join(path, sensor + ".png")
                    plt.savefig(file, bbox_inches='tight')
                    print('inflection plot saved ' + file)
