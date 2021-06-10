from c0103_save_meta import save_meta

from datetime import date
from datetime import datetime
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def record_to_summary(study, name, value):
    """
    Clean the data
    """

    metadata_path = os.path.join('studies', study, 'meta')
    summary_file = os.path.join(metadata_path, 'summary.txt')


    if name == "Records found":
        file = open(summary_file, "w")
        file = open(summary_file, "w")

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        file.write('File made on ' + str(date.today()) + ' ' + str(current_time) )
        file.write('\n')

    else:
        file = open(summary_file, "a")

    file.write('\n' + str(name) + ' = ' + str(value) )

    file.close()
