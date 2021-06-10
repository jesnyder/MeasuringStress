from c0101_retrieve_ref import retrieve_ref

import os
import pandas as pd
from shutil import copyfile


def study_figures(comprehensive_report):
    """
    Create a comprehensive report
    Compile the text and figures into a single pdf
    """

    # retrieve variables needed to find the figures
    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')
    sensor_list.reverse()

    segment_list = retrieve_ref('segment_list')

    degree_list = retrieve_ref('degree_list')
    degree_list = [int(x) for x in degree_list]

    format_types = ['source', 'truncate', 'coregister', 'clean']

    format_types.append('regression0')
    format_types.append('regression1')
    format_types.append('regression2')

    print('format_types = ')
    print(format_types)



    for study in study_list:

        source_path = os.path.join('studies', study, 'formatted', 'truncate')
        format_folders = os.listdir(source_path)

        format_folders.sort()

        for record in format_folders:

            i = format_folders.index(record)

            for format_type in format_types:

                for sensor in sensor_list:

                    source = os.path.join('studies', study, 'plotted', format_type, record, sensor + '.png')

                    if format_type == 'regression0':
                        degree = 0

                        source = os.path.join('studies', study, 'plotted', 'regression', str(degree), record, sensor + '.png')
                    if format_type == 'regression1':
                        degree = 1
                        source = os.path.join('studies', study, 'plotted', 'regression', str(degree), record, sensor + '.png')

                    if format_type == 'regression2':
                        degree = 2
                        source = os.path.join('studies', study, 'plotted', 'regression', str(degree), record, sensor + '.png')

                    if os.path.isfile(source):

                        print('path found: plot_file = ' + str(source))

                        file = open(comprehensive_report, "a")

                        file.write('\n')
                        file.write('\n')
                        file.write('\\begin{figure}[ht]')
                        file.write('\n')
                        file.write('\includegraphics')
                        file.write('[width=\\textwidth]')
                        file.write('{')
                        file.write(source)
                        file.write('}')
                        file.write('\n')
                        file.write('\\caption{' + str(study) + ' (record ' + str(i) + ' of ' + str(len(format_folders)) + ') ' + sensor +  ' ' + format_type + '}' + '\n')
                        file.write('\centering' + ' \n')
                        file.write('\\end{figure}' + ' \n')
                        file.write('\\clearpage' + ' \n' + '\n')

                        file.close()
