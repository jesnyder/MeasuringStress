from c0101_retrieve_ref import retrieve_ref
from c0102_timestamp import timestamp_source
from c0103_trim_record_to_max import trim_record_to_max
from c0104_plot_timestamp import plot_timestamp
from c0105_find_records import find_records
from c0106_record_to_summary import record_to_summary
from c0107_decide_inclusion import decide_inclusion
from c0108_save_meta import save_meta
from c0109_retrieve_meta import retrieve_meta
from c0110_find_temp_end import find_temp_end
from c0111_retrieve_analyzed import retrieve_analyzed
from c0112_plot_truncate import plot_truncate
from c0113_plot_acc import plot_acc
from c0202_machineLearningBasic import  machineLearningBasic


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics

def statisticsCalculation():
    """
    Calculate and save statistics from each record
    """

    print("begin statistical calculation")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')


    analysis_type = 'truncate'

    for study in study_list:

        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])

        dfStatistics = pd.DataFrame()

        for sensor in sensor_list:

            dfMeanList, dfMedianList, dfPvariance, dfStdev = [], [], [], []
            quan_10, quan_20, quan_30, quan_40, quan_50, quan_60, quan_70, quan_80, quan_90 = [], [], [], [], [], [], [], [], []

            for record in source_path:

                df = retrieve_analyzed(study, analysis_type, record, sensor)

                measurement = list(df['measurement'])
                # dfMean = statistics.mean(measurement)
                # print('dfMean = ' + str(dfMean))
                dfMeanList.append(statistics.mean(measurement))
                dfMedianList.append(statistics.median(measurement))
                dfPvariance.append(statistics.pvariance(measurement))
                dfStdev.append(statistics.stdev(measurement))

                quan_10.append(np.quantile(measurement, 0.1))
                quan_20.append(np.quantile(measurement, 0.2))
                quan_30.append(np.quantile(measurement, 0.3))
                quan_40.append(np.quantile(measurement, 0.4))
                quan_50.append(np.quantile(measurement, 0.5))
                quan_60.append(np.quantile(measurement, 0.6))
                quan_70.append(np.quantile(measurement, 0.7))
                quan_80.append(np.quantile(measurement, 0.8))
                quan_90.append(np.quantile(measurement, 0.9))

            colName = str(str(sensor) + '_mean')
            dfStatistics[colName] = dfMeanList
            colName = str(str(sensor) + '_median')
            # dfStatistics[colName] = dfMedianList
            colName = str(str(sensor) + '_pvariance')
            dfStatistics[colName] = dfPvariance
            colName = str(str(sensor) + '_stdev')
            dfStatistics[colName] = dfStdev

            dfStatistics[str(str(sensor) + 'quan_10')] = quan_10
            dfStatistics[str(str(sensor) + 'quan_20')] = quan_20
            dfStatistics[str(str(sensor) + 'quan_30')] = quan_30
            dfStatistics[str(str(sensor) + 'quan_40')] = quan_40
            dfStatistics[str(str(sensor) + 'quan_50')] = quan_50
            dfStatistics[str(str(sensor) + 'quan_60')] = quan_60
            dfStatistics[str(str(sensor) + 'quan_70')] = quan_70
            dfStatistics[str(str(sensor) + 'quan_80')] = quan_80
            dfStatistics[str(str(sensor) + 'quan_90')] = quan_90


        analyzed_path = os.path.join(study, 'analyzed')
        if not os.path.isdir(analyzed_path): os.mkdir(analyzed_path)
        analyzed_path = os.path.join(study, 'analyzed', 'statistics')
        if not os.path.isdir(analyzed_path): os.mkdir(analyzed_path)
        analyzed_file = os.path.join(analyzed_path, 'statistics.csv')
        print('analyzed_file = ' + str(analyzed_file))
        dfStatistics.to_csv(analyzed_file)

        print('statistical analysis for study / sensor complete: ' + str(study) + ' / ' +  str(sensor))



        plt.scatter( dfStatistics['EDA_mean'] , dfStatistics['HR_mean'])
        plt.xlabel('EDA mean')
        plt.ylabel('HR mean')
        plot_path = os.path.join(study, 'plot')
        if not os.path.isdir(plot_path): os.mkdir(plot_path)
        plot_path = os.path.join(study, 'plot', 'analyzed')
        if not os.path.isdir(plot_path): os.mkdir(plot_path)
        plot_file = os.path.join(plot_path, 'summary' + '.png')
        plt.savefig(plot_file, bbox_inches='tight')
        print('saved statistics - ' + str(plot_file))



    print("end statistical calculation")
