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


def retrieve_analysis(study, analysis_type, segment, sensor):
    """

    """

    if 'statistics_mean' == analysis_type:
        file = os.path.join('studies', study, 'analyzed', 'statistics', 'mean', segment, sensor +  '.csv')


    file = os.path.join('studies', study, 'analyzed', 'statistics', 'mean', segment, sensor +  '.csv')
    df = pd.read_csv(file)

    colNames = list(df.head())
    for colName in colNames:
        if 'Unnamed' in colName:
            del df[colName]

    return(df)
