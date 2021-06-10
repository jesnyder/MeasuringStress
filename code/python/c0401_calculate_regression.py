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


def calculate_regression():
    """

    """

    print('analyzing regression. ')

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

            for segment in segment_list:

                df_coef = pd.DataFrame()
                df_coef['recordName'] = recordNames

                for degree in degree_list:

                    for record in recordNames:

                        source = os.path.join('studies', study, 'formatted', format_type, record, segment, sensor + '.csv')
                        print('source = ' + source)
                        df = pd.read_csv(source)

                        if not len(list(df['timeUnix'])) > 0:
                            continue

                        for colName in  list(df.head()):

                            if 'meas' in colName:

                                if colName not in list(df_coef.head()):
                                    df_coef[colName] = [None]*len(recordNames)

                                i = df_coef[df_coef['recordName'] == record].index.values[0]
                                xx = list(df['timeMinutes'])
                                yy = list(df[colName])

                                coef = np.polyfit(xx, yy, degree)
                                print('coef = ' )
                                print(coef)
                                coef_str = [str(x) for x in coef]
                                print(' '.join(coef_str))
                                df_coef.loc[i, colName ] = ' '.join(coef_str)


                    path = ['studies', study, 'analyzed', 'regression', str(degree), segment]
                    path = build_path(path)
                    file = os.path.join(path, sensor + ".csv")
                    df_coef.to_csv(file)
                    print('regression file saved: ' + file)
