from c0101_retrieve_ref import retrieve_ref
from c0101_retrieve_ref import retrieve_ref_color
from c0101_retrieve_ref import retrieve_sensor_unit
from c0102_build_path import build_path


from c0201_plot_source import plot_source
from c0202_plot_acc import plot_acc
from c0203_plot_coregister import plot_coregister
from c0204_plot_segment import plot_segment


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_cleaned():
    """
    check the quality of the clean data by plotting
    compare source / truncate / coregister / clean
    """

    print("begin plotting the clean data ")

    study_list = retrieve_ref('study_list')

    for study in study_list:

        plot_source(study)

        plot_acc(study)

        plot_coregister(study)

        plot_segment(study)

    print("completed plotting the clean data")
