from c0101_retrieve_ref import retrieve_ref

from c8001_modeling_test import modeling_test
from c8002_modeling_mean import modeling_mean



from datetime import date
from datetime import datetime
import math
import os
import pandas as pd
from pytz import reference
from shutil import copyfile


def openscad_modeling():
    """
    Write code for openscad to model parameters of the analysis
    """

    print("openSCAD modeling begin")


    modeling_test()
    modeling_mean()

    """

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')

    for study in study_list:

        metadata_file = os.path.join(study, 'meta', 'metadata.csv')
        df_meta = pd.read_csv(metadata_file)
        df_meta = df_meta.sort_values(by=['recordLength'])

        records_found = list(df_meta['source_path'])
        recordLength = list(df_meta['recordLength'])


        openscad_path = os.path.join(study, 'openSCAD')
        if not os.path.isdir(openscad_path ): os.mkdir(openscad_path)
        openscad_file = os.path.join(openscad_path, str(study) + '_' + 'cleaning_data.scad')
        file = open(openscad_file, "w")
        file = open(openscad_file, "w")

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        file.write('// File made on ' + str(date.today()) + ' ' + str(current_time) )

        file.write('\n' + '// records found = ' +  str(len(records_found)))
        # file.write('\n' + 'd = '  + str(10) + ' ; ' + '\n')

        # file.write('\n' + 'sphere( size = ' + str(d) + ') ;')

        count_xaxis = math.sqrt(len(records_found))

        spacing = round(max(recordLength)*2, 3)
        file.write('\n' + '// spacing = ' + str(spacing))

        for i in range(len(records_found)):

            # print('index = ' + str(i))
            x_num = int((i+1)/count_xaxis)
            y_num = int((i+1)%count_xaxis)
            z_num = 0
            length = round(recordLength[i], 3)

            # print('x_num, y_num = ' + str(x_num) + ' , ' + str(y_num))

            file.write('\n')
            file.write('\n' + 'translate([ ' + str(spacing*x_num)  + ' , ' + str(spacing*y_num) + ' , ' + str(spacing*z_num) + '])')
            file.write('\n' + 'union() {')
            file.write('  ' + 'color([ ' + str(1) + ' , ' + str(0)  +' , ' + str(1) + ' ])')
            file.write('  ' + 'sphere(' + str(length)    +  ' , $fn=60);')
            file.write('  ' + 'color([ ' + str(0.5) + ' , ' + str(0.5)  +' , ' + str(1) + ' ])')
            file.write('  ' + 'cylinder( r= ' + str(length/2) + ', h= ' + str(2*length)   +  ' , $fn=60);')
            file.write(' } ')
            file.write('\n')
            file.write('\n')

        file.close()
    """


    print("openSCAD modeling complete")
