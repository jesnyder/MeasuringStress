from c0101_retrieve_ref import retrieve_ref
from c0101_retrieve_ref import retrieve_ref_color
from c0101_retrieve_ref import retrieve_ref_color_wearable_segment
from c0101_retrieve_ref import retrieve_sensor_unit
from c0102_build_path import build_path
from c0104_retrieve_meta import retrieve_meta

from c0402_retrieve_regression import retrieve_regression

import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


def plot_regression():
    """

    """

    print('plotting regression')



    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    segment_list = retrieve_ref('segment_list')

    degree_list = retrieve_ref('degree_list')
    degree_list = [int(x) for x in degree_list]


    for study in study_list:

        format_type = 'clean'
        clean_path = os.path.join('studies', study, 'formatted', format_type)
        recordNames = os.listdir(clean_path)

        for sensor in sensor_list:

            for degree in degree_list:

                for record in recordNames:

                    row_num, col_num, plot_num = len(segment_list)+2, 1, 0
                    row_width_mulp, col_width_mulp = 14, 5
                    plot_width, plot_height = col_num*row_width_mulp, row_num*col_width_mulp
                    plt.figure(figsize=(plot_width, plot_height))

                    for segment in segment_list:
                        plot_num += 1
                        plt.subplot(row_num, col_num, plot_num)
                        complete = plot_regression_segment(study, record, segment, sensor, degree)

                    plot_num += 1
                    plt.subplot(row_num, col_num, plot_num)
                    for segment in segment_list[:-1]:
                        complete = plot_regression_segment(study, record, segment, sensor, degree)
                        plt.title(' ')


                    plot_num += 1
                    plt.subplot(row_num, col_num, plot_num)
                    complete = plot_coefficient_bar(study, record, sensor, degree)
                    plt.title(' ')


                    path = ['studies', study, 'plotted', 'regression', str(degree), record]
                    path = build_path(path)
                    file = os.path.join(path, sensor + ".png")
                    plt.savefig(file, bbox_inches='tight')
                    print('plotted regression for ' + file)



def plot_regression_segment(study, record, segment, sensor, degree):
    """

    """

    df_coef = retrieve_regression(study, segment, sensor, degree)
    colNamesCoef = list(df_coef.head())

    format_type = 'clean'
    source = os.path.join('studies', study, 'formatted', format_type, record, segment, sensor + '.csv')
    print('source = ' + source)
    df = pd.read_csv(source)

    colNames = list(df.head())
    print('colNames = ')
    print(colNames)
    xx = list(df['timeMinutes'])

    if len(xx) == 0:
        return(0)

    yyReal = list(df[colNames[-1]])
    i = df_coef[df_coef['recordName'] == record].index.values[0]

    coeff = df_coef.loc[i, colNamesCoef[-1]]

    print('coeff = ')
    print(coeff)

    try :
        float(coeff)
        coeff = [coeff]

    except:
        coeff = coeff.split(' ')

    print('coeff = ')
    print(coeff)


    # print('coeff =')
    # print(coeff)

    yy = []
    for x in xx:
        # print('x = ' + str(x))
        # print('len(coeff) = ' + str(len(coeff)))
        y = 0
        coef_equation = []
        for i in range(len(coeff)):
            y = y + float(coeff[i])*math.pow(x, len(coeff) - i -1)
            # y = y + float(coeff[i])*math.pow(x, i)
            coef_equation.append(str(str(round(float(coeff[i]), 4)) + '*x^' + str(len(coeff) - i -1)))
        yy.append(y)
        # explain polyval https://numpy.org/devdocs/reference/generated/numpy.polyval.html


    wearable_num = 1
    colorWearableSegment = retrieve_ref_color_wearable_segment(wearable_num, segment)
    plt.scatter(xx, yyReal, color = colorWearableSegment, label = 'measured')

    wearable_num = 2
    colorWearableSegment = retrieve_ref_color_wearable_segment(wearable_num, segment)
    labelPolyfit = str('polyfit degree = ' + str(degree))
    plt.plot(xx, yy, '--', color = colorWearableSegment, label = labelPolyfit)

    plt.xlabel('Time (Minutes)')
    sensor_unit = retrieve_sensor_unit(sensor)
    plt.ylabel(sensor + ' ' + sensor_unit )
    plt.title(segment + ' polyfit for degree ' + str(degree))

    coef_str = [str(x) for x in coef_equation]
    coef_str = ' '.join(coef_str)
    print('coef_str = ')
    print(coef_str)
    plt.legend(bbox_to_anchor=(1, 0.5, 0.3, 0.2), loc='upper left')
    plt.title(segment + ' polyfit for degree ' + str(degree) + ' ' + str(coef_str))

    return(0)


def plot_coefficient_bar(study, record, sensor, degree):
    """

    """

    segment_list = retrieve_ref('segment_list')

    for segment in segment_list:

        print('bar chart for segment = ' + str(segment))

        df_coef = retrieve_regression(study, segment, sensor, degree)
        print('df_coef = ')
        print(df_coef)

        i = df_coef[df_coef['recordName'] == record].index.values[0]
        print('i = ' + str(i))


        colNames = list(df_coef.head())
        coeff = df_coef.loc[i, colNames[-1]]
        print('coeff = ' + str(coeff))

        a = pd.isnull(df_coef.loc[i, colNames[-1]])
        print('a = ' + str(a))

        if a == 'True' or str(df_coef.loc[i, colNames[-1]]) == 'None':
            print('cell empty a = ' + str(a) + ' coeff = ')
            print(coeff)
            continue

        elif a != 'True':
            print('cell not empty a = ' + str(a) + ' coeff = ')
            print(coeff)


            try :
                float(coeff)
                coeff = [float(coeff)]
                print('try found coeff = ')
                print(coeff)

            except:
                coeff = coeff.split(' ')
                coeff = [float(x) for x in coeff]
                print('except found coeff = ')
                print(coeff)


            xx = [segment_list.index(segment)]
            yy = [coeff[0]]

            wearable_num = 1
            colorSegment = retrieve_ref_color_wearable_segment(wearable_num, segment)
            plt.bar(xx, yy, color = colorSegment )
            plt.xticks(range(len(segment_list)), segment_list)
