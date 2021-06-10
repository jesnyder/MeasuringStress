from c0101_retrieve_ref import retrieve_ref
from c0102_build_path import build_path
from c0103_save_meta import save_meta
from c0104_retrieve_meta import retrieve_meta
from c0105_record_to_summary import record_to_summary

from c0107_timestamp_source import timestamp_source
from c0107_timestamp_source import build_timestamps



import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def define_records():
    """
    define each record
    set the beginning of the record
    set the end of the record
    record the length of the record
    """

    print("begin define_record")

    # define the original start time, end time, and length
    # record to the metadata
    # remove any records shorter than the minimum lemgth requirements
    define_original()

    # define the record's start time, end time, and length
    define_record()

    # check for multiple records
    # if found define the embedded record
    find_embedded_records()
    add_embedded_to_meta()




def define_original():
    """
    define the original start time, end time, and length
    record to the metadata
    remove any records shorter than the minimum lemgth requirements
    """

    study_list = retrieve_ref('study_list')
    min_record_time = retrieve_ref('min_record_time')

    # check each study
    for study in study_list:

        # retrieve the list of records from the metadata.csv file
        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])

        # add the columns to define the original record
        df_meta['recordName'] = source_path
        df_meta['originalBegin'] = [None] * len(source_path)
        df_meta['originalEnd'] = [None] * len(source_path)
        df_meta['originalLength'] = [None] * len(source_path)

        # define the original length of the record
        # remove records that are too short
        for record in source_path:

            format_type, segment, sensor = 'source', 'All', 'TEMP'
            df_timestamped = timestamp_source(study, format_type, segment, record, sensor)

            originalBegin = int(min(list(df_timestamped['timeUnix'])))
            originalEnd = int(max(list(df_timestamped['timeUnix'])))
            originalLength = (originalEnd - originalBegin) / 60

            i = df_meta[ df_meta['source_path']== record].index.values[0]

            df_meta.loc[i, 'originalBegin' ] = originalBegin
            df_meta.loc[i, 'originalEnd' ] = originalEnd
            df_meta.loc[i, 'originalLength' ] = round(originalLength, 4)

        # save the metadata file
        save_meta(study, df_meta)
        df_meta = df_meta.drop(df_meta[df_meta['originalLength'] < min_record_time].index)
        save_meta(study, df_meta)



def define_record():
    """
    define the original start time, end time, and length
    record to the metadata
    remove any records shorter than the minimum lemgth requirements
    """

    study_list = retrieve_ref('study_list')
    min_record_time = retrieve_ref('min_record_time')
    max_record_time = retrieve_ref('max_record_time')

    # check each study
    for study in study_list:

        # retrieve the list of records from the metadata.csv file
        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])

        df_meta['recordBegin'] = [None] * len(source_path)
        df_meta['recordEnd'] = [None] * len(source_path)
        df_meta['recordLength'] = [None] * len(source_path)

        # define the original length of the record
        # remove records that are too short
        for record in source_path:

            i = df_meta[ df_meta['source_path']== record].index.values[0]
            originalBegin = df_meta.loc[i, 'originalBegin' ]
            originalEnd = df_meta.loc[i, 'originalEnd' ]
            originalLength = df_meta.loc[i, 'originalLength' ]

            format_type, segment, sensor = 'source', 'All', 'TEMP'
            source = os.path.join('studies', study, 'formatted', format_type, record, segment, sensor + '.csv')
            df = pd.read_csv(source)

            timeEndUnix = find_record_end_using_temp(df)
            recordBegin = originalBegin
            recordEnd = timeEndUnix
            recordLength = (timeEndUnix - recordBegin) / 60

            df_meta.loc[i, 'recordBegin' ] = recordBegin
            df_meta.loc[i, 'recordEnd' ] = recordEnd
            df_meta.loc[i, 'recordLength' ] = round(recordLength, 4)

        # save the metadata file
        save_meta(study, df_meta)



def find_record_end_using_temp(df):
    """
    Find the record end
    by searching for the drop in the temperature
    If the temperature drops 2 deg C in 3 seconds and there is <5 minutes left - end the record
    If there is <5 minutes left, check if the temperature stays low
    """

    max_record_time = float(retrieve_ref('max_record_time'))
    min_record_time = float(retrieve_ref('min_record_time'))

    timeUnix = list(df['timeUnix'])
    timeMinutes = list(df['timeMinutes'])
    measurements = list(df['measurement'])

    time_end = timeMinutes[-12]
    timeEndUnix = timeUnix[-12]

    for i in range(len(measurements) - 12):

        # the record has to be a minimum length
        if float(timeMinutes[i]) > float(min_record_time) + timeMinutes[0]:

            # look for a drop of at least 2 deg C over 3 seconds
            # the TEMP sensor takes 4 measurements each seconds,
            # which means the measurement 12 steps ahead is 3 seconds later
            if float(measurements[i]) - 2  > float(measurements[i+12]):
                # print('measurement[i] &  measurements[i+12] =' + str(measurements[i]), ' & ', str(measurements[i+12]))
                # print('timeMinutes[i] &  timeMinutes[i+12] =' + str(timeMinutes[i]), ' & ', str(timeMinutes[i+12]))

                if timeMinutes[-1] - timeMinutes[i] > 5:

                    if float(measurements[i]) - 2  > float(measurements[i+100]):

                        if float(measurements[i]) - 2  > float(measurements[i+200]):

                            if float(measurements[i]) - 3  > float(measurements[i+300]):

                                time_end = timeMinutes[i - 12]
                                timeEndUnix = timeUnix[i - 12]
                                break


                else:
                    time_end = timeMinutes[i - 12]
                    timeEndUnix = timeUnix[i - 12]
                    break

    # trim the record back to a maximum
    if timeEndUnix - timeUnix[0]  > 60*max_record_time:
        timeEndUnix = timeUnix[0] + 60*max_record_time


    return(int(timeEndUnix - 1))




def find_embedded_records():
    """
    check for long records
    look for second sudden increase in temperature
    define the record begin, end, and duration
    log in the metadata file
    """

    study_list = retrieve_ref('study_list')
    min_record_time = float(retrieve_ref('min_record_time'))

    # check each study
    for study in study_list:

        # retrieve the list of records from the metadata.csv file
        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])

        df_meta['embeddedRecord'] = [0] * len(source_path)

        print('df_meta = ')
        print(df_meta)

        # define the original length of the record
        # remove records that are too short
        for record in source_path:

            print('record = ' + str(record))

            i = df_meta[ df_meta['source_path']== record].index.values[0]
            originalLength = float(df_meta.loc[i, 'originalLength' ])
            recordLength = float(df_meta.loc[i, 'recordLength' ])

            print('originalLength = ' + str(originalLength))
            print('recordLength = ' + str(recordLength))

            if recordLength + min_record_time < originalLength:

                format_type, segment, sensor = 'source', 'All', 'TEMP'
                source = os.path.join('studies', study, 'formatted', format_type, record, segment, sensor + '.csv')
                df = pd.read_csv(source)

                print('df = ')
                print(df)

                timeUnix = list(df['timeUnix'])
                timeMinutes = list(df['timeMinutes'])
                measurements = list(df['measurement'])

                for j in range(len(measurements) - 12):

                    if timeMinutes[j] > recordLength + 1:

                        if timeMinutes[j] + min_record_time < originalLength:

                            if measurements[j] + 2 < measurements[j+12]:

                                if measurements[j] + 2 < measurements[j+100]:

                                    if measurements[j] + 3 < measurements[j+200]:

                                        secondRecordBegin = int(timeUnix[j+12])
                                        print('secondRecordBegin = ' + str(secondRecordBegin))
                                        df_meta.loc[i, 'embeddedRecord' ] = secondRecordBegin

        save_meta(study, df_meta)




def add_embedded_to_meta():
    """

    """

    study_list = retrieve_ref('study_list')
    min_record_time = float(retrieve_ref('min_record_time'))

    # check each study
    for study in study_list:

        # retrieve the list of records from the metadata.csv file
        df_meta = retrieve_meta(study)
        source_path = list(df_meta['source_path'])

        # define the original length of the record
        # remove records that are too short
        for record in source_path:

            print('record = ' + str(record))
            print('df_meta = ')
            print(df_meta)

            i = df_meta[ df_meta['source_path']== record].index.values[0]
            embeddedRecord = float(df_meta.loc[i, 'embeddedRecord' ])

            if embeddedRecord > 0:

                format_type, segment, sensor = 'source', 'All', 'TEMP'
                source = os.path.join('studies', study, 'formatted', format_type, record, segment, sensor + '.csv')
                df = pd.read_csv(source)

                recordBegin = int(embeddedRecord)
                df = df[df['timeUnix'] > recordBegin]
                timeEndUnix = find_record_end_using_temp(df)
                recordLength = (timeEndUnix - recordBegin ) / 60

                df_row = df_meta[ df_meta['source_path'] == record]

                record_split = record.split('_')
                recordName = str( str(recordBegin) + '_' + str(record_split[1]))
                print('embedded recordName = ' + recordName)

                df_row.loc[i, 'recordName' ] = recordName
                df_row.loc[i, 'recordBegin' ] = int(embeddedRecord)
                df_row.loc[i, 'recordEnd' ] = int(timeEndUnix)
                df_row.loc[i, 'recordLength' ] = round(recordLength , 4)

                print('df_row = ')
                print(df_row)

                df_meta = df_meta.append(df_row)
                # print(df_meta)

                format_type, segment, sensor = 'source', 'All', 'TEMP'
                source = os.path.join('studies', study, format_type, record, sensor + '.csv')
                df_source = pd.read_csv(source)
                df_timestamped = build_timestamps(df_source, sensor)


                path = build_path(['studies', study, 'formatted', format_type, recordName, segment])
                file = os.path.join(path, sensor + ".csv")
                df_timestamped.to_csv(file)
                print('formatted source file = ' + str(file))


        df_meta = df_meta.sort_values(by = 'recordName')
        save_meta(study, df_meta)
