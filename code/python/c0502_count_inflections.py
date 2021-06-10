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

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    segment_list = retrieve_ref('segment_list')

    searchRange = retrieve_ref('searchRange')
    searchRange = [int(x) for x in searchRange]
    # searchRange.reverse()

    for study in study_list:

        format_type = 'clean'
        clean_path = os.path.join(study, 'formatted', format_type)
        recordNames = os.listdir(clean_path)

        for sensor in sensor_list:

            for record in recordNames:

                for segment in segment_list:

                    for range in searchRange:

                        if segment == 'All':

                            find_inflections(study, record, sensor, segment, int(range))
                            # list_unique_inflections(study, record, sensor, segment, range)
                            # plot_inflections(study, record, sensor, segment)

                        segment_inflections(study, record, sensor, segment, range)

    print('completed counting inflections')



def find_inflections(study, record, sensor, segment, range):
    """
    Break each set of measurements into a subset - a range of ~30-120 seconds
    Use polyfit to find the best fit second order polynomial
    Find the inflection point of the best fit polynomial
    If the polyfit inflection point is very close to the median time point in the record
    An inflection is found
    """

    # check if the inflections have already been found
    path = [study, 'analyzed', 'inflections', 'all_times', str(range), record, segment]
    pathJoined = os.path.join(*path)
    file = os.path.join(pathJoined, sensor + ".csv")

    if os.path.isfile(file):
        print('file found, not recalculated.')
        return

    print('finding inflections to build : ' + file)

    # retrieve the timestamped measurements for the study - record - sensor - segment
    format_type = 'truncate'
    source = os.path.join(study, 'formatted', format_type, record, segment, sensor + '.csv')
    print('source = ' + source)
    df = pd.read_csv(source)

    for colName in df.columns:

        # remove extra columns because the dataframe will be saved
        if 'Unnamed' in str(colName):
            del df[colName]

        # save the timestamps as a list
        elif 'Minutes' in str(colName):
            timeMinutes = list(df[colName])

        # find the measurement
        elif 'meas' in colName:

            # add new columns to the dataframe to save the new variables
            newColNames = ['inflectionDecision', 'inflectionLocation', 'polyfitCoefficients', 'polyfitEquation', 'polyfitSolution', 'derivativeEquation', 'derivativeSolution']
            colNameSplit = colName.split('_')
            print('colNameSplit[0] = ' + colNameSplit[0])

            for suffix in newColNames:
                label = str(colNameSplit[0] + '_' + suffix)
                print('label = ' + label)
                if label not in df.columns:
                    df[label] = [None]*len((list(df['timeMinutes'])))

            df['timeBegin'] = [None]*len((list(df['timeMinutes'])))
            df['timeEnd'] = [None]*len((list(df['timeMinutes'])))

            for timeMinute in timeMinutes:

                i = df[ df['timeMinutes']== timeMinute].index.values[0]

                timeDif = (float(df.loc[2,'timeMinutes']) - float(df.loc[1,'timeMinutes']))
                timeTolerance = timeDif/2
                iRange = int(range/60*1/(timeDif))
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


                label = str(colNameSplit[0] + '_' + 'inflectionDecision')
                df.loc[int(i+iRange/2), label] = 'No'

                label = str(colNameSplit[0] + '_' + 'inflectionLocation')
                df.loc[int(i+iRange/2), label] = timeMinute

                label = str(colNameSplit[0] + '_' + 'polyfitCoefficients')
                df.loc[int(i+iRange/2), label] = str(''.join([str(x) for x in coef]))

                label = str(colNameSplit[0] + '_' + 'polyfitEquation')
                df.loc[int(i+iRange/2), label] = str(f)

                label = str(colNameSplit[0] + '_' + 'polyfitSolution')
                df.loc[int(i+iRange/2), label] = str(''.join([str(x) for x in solf]))

                label = str(colNameSplit[0] + '_' + 'derivativeEquation')
                df.loc[int(i+iRange/2), label] = str(dff)

                label = str(colNameSplit[0] + '_' + 'derivativeSolution')
                df.loc[int(i+iRange/2), label] = str(soldf)

                if soldf < timeMedian + timeTolerance:

                    if soldf > timeMedian - timeTolerance:

                        print('inflection found at time = ' + str(soldf))
                        label = str(colNameSplit[0] + '_' + 'inflectionDecision')
                        df.loc[int(i+iRange/2), label] = 'Yes'

    path = build_path(path)
    file = os.path.join(path, sensor + ".csv")
    df.to_csv(file)
    print('inflection list saved : ' + file)
    return(file)


def plot_inflections(study, record, sensor, segment):
    """
    plot inflections
    """

    if segment != 'All':
        return

    searchRange = retrieve_ref('searchRange')
    searchRange = [int(x) for x in searchRange]

    format_type, segment, range = 'trunate', 'All', searchRange[0]
    path = [study, 'analyzed', 'inflections', 'all_times', str(range), record, segment]
    file = os.path.join(*path, sensor + ".csv")

    if not os.path.isfile(file):
        return


    row_num, col_num, plot_num = len(searchRange)+2, 1, 0
    row_width_mulp, col_width_mulp = 12, 5
    plot_width, plot_height = col_num*row_width_mulp, row_num*col_width_mulp
    plt.figure(figsize=(plot_width, plot_height))

    for range in searchRange:

        plot_num += 1
        plt.subplot(row_num, col_num, plot_num)

        path = [study, 'analyzed', 'inflections', 'all_times', str(range), record, segment]
        file = os.path.join(*path, sensor + ".csv")

        if not os.path.isfile(file):
            continue

        # source = os.path.join(study, 'formatted', format_type, record, segment, sensor + '.csv')
        # print('source = ' + source)
        df = pd.read_csv(file)

        for colName in df.columns:

            if 'Unnamed' in colName:
                del df[colName]

            elif 'Minutes' in colName:
                timeMinutes = list(df[colName])

            elif 'measurement' in colName and '_' not in colName:
                measList = list(df[colName])
                measMin = min(measList)
                measMax = max(measList)
                plt.scatter(timeMinutes, measList, label = str(colName))

            elif 'inflectionDecision' in colName:
                dfInflections = df.drop(df[(df[colName] != 'Yes')].index)
                timeInflections = list(dfInflections['timeMinutes'])

            print('timeInflections = ')
            print(timeInflections)

            for time in timeInflections:

                xx = np.linspace( time, time, 100)
                yy = np.linspace( measMin, measMax, 100)
                plt.plot(xx, yy, color=[0,.9,.6])

            plt.xlabel('time Unix')
            sensor_unit = retrieve_sensor_unit(sensor)
            plt.ylabel(sensor + ' ' + sensor_unit )
            # plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')
            plt.title('Record = ' + str(record) + ' Range = ' + str(range) + ' seconds ' + ' Inflections Found = ' + str(len(timeInflections)) )

        path = [study, 'plotted', 'inflection', 'each_record', record]
        path = build_path(path)
        file = os.path.join(path, sensor + ".png")
        plt.savefig(file, bbox_inches='tight')
        print('inflection plot saved ' + file)



def segment_inflections(study, record, sensor, segment, range):
    """

    """

    segmentRef = 'All'
    path = [study, 'analyzed', 'inflections', 'all_times', str(range), record, segmentRef]
    file = os.path.join(*path, sensor + ".csv")

    if not os.path.isfile(file):
        return

    df = pd.read_csv(file)

    for colName in df.columns:

        if 'Unnamed' in str(colName):
            del df[colName]

        df = segment_df(segment, df)

        path = [study, 'analyzed', 'inflections', 'all_times', str(range), record, segmentRef]
        path = build_path(path)
        file = os.path.join(path, sensor + ".csv")
        df.to_csv(file)
        print('segmented inflection file saved - ' + file)
