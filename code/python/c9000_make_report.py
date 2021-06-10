from c0101_retrieve_ref import retrieve_ref


from c9002_latex_report import latex_report
from c9003_study_figures import study_figures

from datetime import date
from datetime import datetime
import os
import pandas as pd
from shutil import copyfile


def make_report():
    """
    Create a comprehensive report
    Compile the text and figures into a single pdf
    """

    latex_path = os.path.join('latex')
    if not os.path.isdir(latex_path): os.mkdir(latex_path)

    comprehensive_report = os.path.join('code', 'latex', 'report' + '.txt')

    dst = open(comprehensive_report, 'w')
    dst.close()

    dst = open(comprehensive_report, 'w')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    dst.write('% File made on ' + str(date.today()) + ' ' + str(current_time) )
    dst.write('\n')
    dst.close()

    # prepare latex code
    latex_report(comprehensive_report)

    # create study_figures
    # study_figures(comprehensive_report)

    # end the document

    dst = open(comprehensive_report, 'a')
    # end the latex file
    dst.write('\n' + '\n')
    dst.write('\\end{document}')
    dst.write('\n' + '\n')

    dst.close()
