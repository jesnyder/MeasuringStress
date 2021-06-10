from c0101_retrieve_ref import retrieve_ref
from c0101_retrieve_ref import retrieve_ref_color
from c0101_retrieve_ref import retrieve_ref_color_wearable_segment
from c0102_build_path import build_path
from c0104_retrieve_meta import retrieve_meta

from c0401_calculate_regression import calculate_regression
from c0403_plot_regression import plot_regression


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def analyze_regression():
    """

    """

    print('analyzing regression. ')

    calculate_regression()
    # plot_regression()
