from c0101_retrieve_ref import retrieve_ref
from c0301_retrieve_analysis import retrieve_analysis



from datetime import date
from datetime import datetime
import math
import os
import pandas as pd
from pytz import reference
from shutil import copyfile


def modeling_mean():
    """
    Write code for openscad to model parameters of the analysis
    """

    print("openSCAD modeling begin")

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')

    for study in study_list:

        analysis_type, segment, sensor = 'statistics_mean', 'All', 'EDA'
        df_EDA = retrieve_analysis(study, analysis_type, segment, sensor)
        df_HR = retrieve_analysis(study, analysis_type, segment, 'HR')
        df_TEMP = retrieve_analysis(study, analysis_type, segment, 'TEMP')


        recordName = list(df_TEMP['recordName'])



        openscad_path = os.path.join('studies', study, 'openSCAD')
        if not os.path.isdir(openscad_path ): os.mkdir(openscad_path)
        openscad_file = os.path.join(openscad_path, str(study) + '_' + 'mean_data.scad')
        file = open(openscad_file, "w")
        file = open(openscad_file, "w")
        file = open(openscad_file, "a")

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        file.write('// File made on ' + str(date.today()) + ' ' + str(current_time))
        file.write('\n' + '// records found = ' +  str(len(recordName)))

        for record in recordName:

            i = df_TEMP[ df_TEMP['recordName']== record].index.values[0]

            colNames = list(df_TEMP.head())
            for colName in colNames:
                if 'mean' in colName:
                    eda_mean = float(df_EDA.loc[i, colName ])
                    allEDA = list(df_EDA[colName])

                    hr_mean = float(df_HR.loc[i, colName ])
                    allHR = list(df_HR[colName])

                    temp_mean = float(df_TEMP.loc[i, colName ])
                    allTEMP = list(df_TEMP[colName])

            count_xaxis = math.sqrt(len(recordName))
            # spacing = round(max(allTEMP)*2, 3)
            spacing = round(60, 3)
            file.write('\n' + '// spacing = ' + str(spacing))

            # print('index = ' + str(i))
            x_num = int((i+1)/count_xaxis)
            y_num = int((i+1)%count_xaxis)
            z_num = 0
            length = round(temp_mean, 4)
            sphere_radius = round(temp_mean, 4)

            # set colors for each sensor as a function of the record value
            meanIntensity = (eda_mean - min(allEDA))  / (max(allEDA) - min(allEDA))
            colorEDA = [round(meanIntensity, 3), 0, 1-round(meanIntensity, 3)]
            edaNormalized = meanIntensity*10+1

            meanIntensity = (hr_mean - min(allHR))  / (max(allHR) - min(allHR))
            colorHR = [round(meanIntensity, 3), 0, 1-round(meanIntensity, 3)]
            HRNormalized = meanIntensity*10+1

            meanIntensity = (temp_mean - min(allTEMP))  / (max(allTEMP) - min(allTEMP))
            colorTEMP = [round(meanIntensity, 3), 0, 1-round(meanIntensity, 3)]
            tempNormalized = meanIntensity*10+1


            file.write('\n')
            file.write('\n' + 'translate([ ' + str(spacing*x_num)  + ' , ' + str(spacing*y_num) + ' , ' + str(spacing*z_num) + '])')
            file.write('\n' + 'union() {')

            file.write('  ' + 'color([ ' + str(colorTEMP[0]) + ' , ' + str(colorTEMP[1])  +' , ' + str(colorTEMP[2]) + ' ])')
            file.write('  ' + 'sphere( r =' + str(tempNormalized)    +  ' , $fn=60);')

            file.write('\n' + 'for ( i=[1:30:360]) {')
            file.write('\n' + 'rotate([0,0,i])')
            file.write('\n' + 'translate([0, ' + str(tempNormalized + edaNormalized) + '])')
            file.write('  ' + 'color([ ' + str(colorEDA[0]) + ' , ' + str(colorEDA[1])  +' , ' + str(colorEDA[2]) + ' ])')
            file.write('\n' + 'sphere( r = ' + str(edaNormalized) + ', $fn=60);')
            file.write('\n' + '}')

            file.write('\n' + 'for ( i=[1:15:360]) {')
            file.write('\n' + 'rotate([0,0,i])')
            file.write('\n' + 'translate([0, ' + str(tempNormalized + 2*edaNormalized + HRNormalized) + '])')
            file.write('  ' + 'color([ ' + str(colorHR[0]) + ' , ' + str(colorHR[1])  +' , ' + str(colorHR[2]) + ' ])')
            file.write('\n' + 'sphere( r = ' + str(HRNormalized) + ', $fn=60);')
            file.write('\n' + '}')

            file.write('\n' + '}')



            """
            file.write('\n' + 'for(i = [0:180]) {')
            file.write('\n' + '     rotate([0,i,0])')
            # file.write('\n' + '     translate([' + str(sphere_radius) + ' , ' + str(sphere_radius) + ' , ' + str(sphere_radius) + ' ])')
            file.write('\n' + '     difference() {')
            file.write('\n' + '     color([ ' + str(colorEDA[0]) + ' , ' + str(colorEDA[1])  +' , ' + str(colorEDA[2]) + ' ])')
            file.write('\n' + '     cylinder(r=' + str(HRNormalized) + ' (0.083 * i), h=.1);')
            file.write('\n' + '     cylinder(r=' + str(0.8*HRNormalized) + ' (0.083 * i), h=.1);')
            file.write('\n' + '}}')
            """


            # file.write(' } ')
            file.write('\n')
            file.write('\n')

        file.close()


    print("openSCAD modeling complete")
