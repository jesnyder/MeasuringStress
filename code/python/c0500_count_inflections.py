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
import re
import statistics
import sympy as sym


def count_inflections():
    """

    """

    print('count inflections')

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    segment_list = retrieve_ref('segment_list')

    searchRange = retrieve_ref('searchRange')
    searchRange = [int(x) for x in searchRange]
    searchRange.reverse()

    for study in study_list:

        format_type = 'clean'
        clean_path = os.path.join('studies', study, 'formatted', format_type)
        recordNames = os.listdir(clean_path)
        recordNames.reverse()

        for sensor in sensor_list:

            if sensor == 'ACC' or sensor == 'BVP':
                continue

            for record in recordNames:

                segment = 'All'
                for range in searchRange:

                        path = ['studies', study, 'analyzed', 'inflections', 'all_times', str(range), record, segment]
                        pathJoined = os.path.join(*path)
                        file = os.path.join(pathJoined, sensor + ".csv")
                        print('inflection file = ' + file)

                        if os.path.isfile(file):
                            print('file already found')
                            continue

                        find_inflections(path, file, study, format_type, record, sensor, segment, range)
                        unique_inflections(study, format_type, record, sensor, segment)
                        plot_inflections(study, record, sensor, segment)

                for segment in segment_list:
                    for range in searchRange:
                        segment_inflections(study, record, sensor, segment, range)

                segment = 'All'
                unique_inflections(study, format_type, record, sensor, segment)
                plot_inflections(study, record, sensor, segment)




def  find_inflections(path, file, study, format_type, record, sensor, segment, range):
    """

    """

    source = os.path.join('studies', study, 'formatted', format_type, record, segment, sensor + '.csv')
    print('source = ' + source)
    df = pd.read_csv(source)
    print('df = ')
    print(df)

    for colName in df.columns:

        # remove extra columns because the dataframe will be saved
        if 'Unnamed' in str(colName):
            del df[colName]

        # save the timestamps as a list
        elif 'Minutes' in str(colName):
            timeMinutes = list(df[colName])

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
                x = sym.Symbol('x')
                f = coef[0]*x*x+coef[1]*x+coef[2]
                dff = sym.diff(f,x)
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

    """

    searchRange = retrieve_ref('searchRange')
    searchRange = [int(x) for x in searchRange]
    searchRange.append('unique')

    row_num, col_num, plot_num = len(searchRange)+2, 2, 0
    row_width_mulp, col_width_mulp = 12, 5
    plot_width, plot_height = col_num*row_width_mulp, row_num*col_width_mulp
    plt.figure(figsize=(plot_width, plot_height))

    for range in searchRange:

        plot_num += 1
        plt.subplot(row_num, col_num, plot_num)

        path = ['studies', study, 'analyzed', 'inflections', 'all_times', str(range), record, segment]
        file = os.path.join(*path, sensor + ".csv")

        if not os.path.isfile(file):
            return

        df = pd.read_csv(file)

        for colName in df.columns:

            if 'Minutes' in colName:
                timeMinutes = list(df[colName])

            if 'measurement' in colName:

                measList = list(df[colName])
                measMin = min(measList)
                measMax = max(measList)
                plt.scatter(timeMinutes, measList, label = str(colName))

            if 'inflectionDecision' in colName or 'unique' in colName:

                if 'inflectionDecision' in colName:
                    dfInflections = df.drop(df[(df[colName] != 'Yes')].index)
                    timeInflections = list(dfInflections['timeMinutes'])

                if 'unique' in colName:
                    plt.scatter(timeMinutes, measList)
                    timeInflections = list(df[colName])

                for time in timeInflections:

                    # multp = searchRange.index(range)/len(searchRange)
                    # colorScatter = [multp*x for x in [0,1,.5]]
                    colorScatter = [0, .9, .6]

                    xx = np.linspace( time, time, 100)
                    yy = np.linspace( measMin, measMax, 100)
                    plt.plot(xx, yy, color=colorScatter, linestyle='--')

                    plt.title('Record = ' + str(record) + ' Range = ' + str(range) + ' seconds ' + ' Inflections Found = ' + str(len(timeInflections)) )
                    plt.xlabel('Time (Minutes)')
                    sensor_unit = retrieve_sensor_unit(sensor)
                    plt.ylabel(sensor + ' ' + sensor_unit )
                    # plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')

            if 'polyfitEquation' in colName:

                polyfitCoeff = list(dfInflections[colName])

                coeffPolyList = []
                for coeff in polyfitCoeff:

                    # print('coeff = ' + str(coeff))
                    coeff = str(coeff)
                    coeff = coeff.replace("x", ",")
                    coeff = coeff.replace("*", "")
                    coeff = coeff.replace("**2", "")
                    coeff = coeff.replace("**", "")
                    coeff = coeff.replace("  ", "")
                    coeff = coeff.replace(" ", "")
                    coeff = coeff.replace("+", "")
                    # print('coeff = ' + str(coeff))
                    coeffList = coeff.split(',')
                    coeffPoly = float(coeffList[0])
                    # print('coeffPoly = ' + str(coeffPoly))
                    coeffPolyList.append(coeffPoly)

                plot_num += 1
                plt.subplot(row_num, col_num, plot_num)

                plt.scatter(timeInflections, coeffPolyList)

                plt.title('Time Infletions vs Coefficients' )
                plt.xlabel('Time (Minutes)')
                sensor_unit = retrieve_sensor_unit(sensor)
                plt.ylabel(sensor + ' ' + sensor_unit )
                # plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')


    path = ['studies', study, 'plotted', 'inflection', 'each_record', record]
    path = build_path(path)
    file = os.path.join(path, sensor + ".png")
    plt.savefig(file, bbox_inches='tight')
    print('inflection plot saved ' + file)


def unique_inflections(study, format_type, record, sensor, segment):
    """

    """

    uniqueList = []

    searchRange = retrieve_ref('searchRange')
    searchRange = [int(x) for x in searchRange]

    for range in searchRange:

        path = ['studies', study, 'analyzed', 'inflections', 'all_times', str(range), record, segment]
        file = os.path.join(*path, sensor + ".csv")

        if not os.path.isfile(file):
            continue

        df = pd.read_csv(file)

        recordLength = max(list(df['timeMinutes']))

        for colName in df.columns:
            if 'Decision' in colName:
                dfInflections = df.drop(df[(df[colName] != 'Yes')].index)

        listInflections = list(dfInflections['timeMinutes'])

        # uniqueList = [uniqueList.append(x) for x in listInflections]
        for time in listInflections:
            if time not in uniqueList:
                uniqueList.append(float(time))

    if len(uniqueList) == 0:
        return

    uniqueList.sort()
    uniqueListBuffer = []
    for time in uniqueList:
        if len(uniqueListBuffer) == 0 or time > max(uniqueListBuffer) + 10/60:
            uniqueListBuffer.append(time)

    uniqueList = uniqueListBuffer
    print('uniqueList = ')
    print(uniqueList)
    print('length of uniqueList = ' + str(len(uniqueList)))

    inflectionRate = len(uniqueList) / recordLength

    df = pd.DataFrame()
    df['uniqueList'] = uniqueList
    df['inflectionRate'] = [inflectionRate]*len(uniqueList)

    path = ['studies', study, 'analyzed', 'inflections', 'all_times', 'unique', record, segment]
    path = build_path(path)
    file = os.path.join(path, sensor + ".csv")
    df.to_csv(file)


def segment_inflections(study, record, sensor, segment, range):
    """

    """
    segmentRef = 'All'
    path = ['studies', study, 'analyzed', 'inflections', 'all_times', str(range), record, segmentRef]
    file = os.path.join(*path, sensor + ".csv")

    if not os.path.isfile(file):
        return

    df = pd.read_csv(file)
    df_segmented = segment_df(segment, df)

    path = ['studies', study, 'analyzed', 'inflections', 'all_times', str(range), record, segment]
    path = build_path(path)
    file = os.path.join(path, sensor + ".csv")
    df_segmented.to_csv(file)
