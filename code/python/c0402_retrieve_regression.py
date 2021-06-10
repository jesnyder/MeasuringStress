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


def retrieve_regression(study, segment, sensor, degree):
    """

    """

    # print('retrieving regression. ')

    path = ['studies', study, 'analyzed', 'regression', str(degree), segment]
    path = build_path(path)

    file = os.path.join(path, sensor +  '.csv')

    df = pd.read_csv(file)

    colNames = list(df.head())
    for colName in colNames:
        if 'Unnamed' in colName:
            del df[colName]


    colNames = list(df.head())
    if pd.isnull(df.loc[1, colNames[-1]]) is True or pd.isnull(df.loc[1, colNames[-2]]):

        df['coefficients'] = [None]*len(list(df['recordName']))

        for record in list(df['recordName']):

            i = df[df['recordName'] == record].index.values[0]

            for colName in colNames:

                if "record" not in colName:

                    if pd.isnull(df.loc[i, colName]) is False:

                        valueCol = df.loc[i, colName]
                        df.loc[i,'coefficients'] = valueCol

        del df[colNames[-1]]
        del df[colNames[-2]]

    print('retrieve_regression df = ')
    print(df)


    return(df)
