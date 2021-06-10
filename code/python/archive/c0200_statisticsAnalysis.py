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
from c0201_statisticsCalculation import statisticsCalculation
from c0202_machineLearningBasic import  machineLearningBasic
from c0204_statisticSegments import statisticSegments


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics

def statisticsAnalysis():
    """
    Statistics
    """

    print("begin statistical analysis")

    # statisticsCalculation()

    # run statistics on each segment
    statisticSegments()

    # machineLearningBasic()


    print("end statistical analysis")
