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

# Python version

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import scipy
import sklearn
import statistics
import sys

from scipy.cluster.hierarchy import dendrogram
from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering


def machineLearningBasic():
    """
    Statistics
    """

    print("begin machine learning basic")


    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')

    for study in study_list:
        analyzed_path = os.path.join(study, 'analyzed', 'statistics')
        analyzed_file = os.path.join(analyzed_path, 'statistics.csv')
        df = pd.read_csv(analyzed_file)

        for name in list(df.columns):
            if 'Unnamed' in name:
                del df[name]

        print(df)




    print("end machine learning basic")
