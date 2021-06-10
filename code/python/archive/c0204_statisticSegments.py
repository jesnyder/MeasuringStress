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

def statisticSegments():
    """
    Calculate and save statistics from each record
    """

    print("begin statistical calculation")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    segment_list = retrieve_ref('segment_list')


    analysis_type = 'truncate'

    for study in study_list:

        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])

        dfStatistics = pd.DataFrame()

        statistics_types = ['mean', 'median', 'pVariance', 'stdev' 'quan']
        quan_types = [10, 20, 30, 40, 50, 60, 70, 80, 90]

        for record in source_path:
            dfStatistics['source_path'] = source_path
            for sensor in sensor_list:
                for segment in segment_list:
                    for statis in statistics_types:

                        colName = str(sensor + '_' + segment + '_' + statis )

                        if statis == 'quan':
                            for quanNum in quan_types:
                                colName = str(sensor + '_' + segment + '_' + statis + '_' + str(quanNum) )

                        dfStatistics[colName] = [None] * len(source_path)

        analyzed_path = os.path.join(study, 'analyzed')
        if not os.path.isdir(analyzed_path): os.mkdir(analyzed_path)
        analyzed_path = os.path.join(study, 'analyzed', 'statistics')
        if not os.path.isdir(analyzed_path): os.mkdir(analyzed_path)
        analyzed_file = os.path.join(analyzed_path, 'statisticsSegments.csv')
        print('analyzed_file = ' + str(analyzed_file))
        dfStatistics.to_csv(analyzed_file)

        # retrieve statistics file
        df = pd.read_csv(analyzed_file)
        for name in list(df.columns):
            if 'Unnamed' in name:
                del df[name]

        for record in source_path:
            for sensor in sensor_list:
                for segment in segment_list:

                    df = retrieve_analyzed(study, analysis_type, record, sensor)
                    measurement = list(df['measurement'])

                    for statis in statistics_types:

                        colName = str(sensor + '_' + segment + '_' + statis )

                        valueValue = 'None'
                        if statis == "mean": valueValue = statistics.mean(measurement)
                        if statis == 'median': valueValue = statistics.median(measurement)
                        if statis == 'pvariance': valueValue = statistics.pvariance(measurement)
                        if statis == 'stdev': statistics.stdev(measurement)

                        if statis == 'quan':
                            for quanNum in quan_types:
                                colName = str(sensor + '_' + segment + '_' + statis + '_' + str(quanNum))
                                valueValue = np.quantile(measurement, quanNum)

                        i = dfStatistics[ dfStatistics['source_path']== record].index.values[0]
                        # print('i = ' + str(i))
                        dfStatistics.loc[i, colName ] = valueValue

        dfStatistics.to_csv(analyzed_file)

    print("end statistical calculation")
