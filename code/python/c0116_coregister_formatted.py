from c0101_retrieve_ref import retrieve_ref
from c0102_build_path import build_path
from c0103_save_meta import save_meta
from c0104_retrieve_meta import retrieve_meta
from c0105_record_to_summary import record_to_summary



import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def coregister_formatted():
    """
    for each record
    break the record into a PreStudy, Study, and PostStudy period
    save each segment as a separate .csv
    """

    print("begin coregister_formatted")

    # check all records for pairs using the recordBegin time
    pair_records()

    # establish the beginning and end of the coregistered records
    define_pairedRecords()

    # coregister paired data in a single csv
    format_coregister()


    print("completed segment_formatted")



def pair_records():
    """
    use the record begin time and wearable id to check all studies and records for pairs
    if found, find the latest common start time and earliest end times
    save as new columns in the metadata file
    """

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')

    # check each study
    for study in study_list:

        df_meta = retrieve_meta(study)
        recordNames = list(df_meta['recordName'])

        # create column to list wearableName and coregister records
        df_meta = add_wearableName(df_meta)
        df_meta['coregisterRecords'] = recordNames

        # look for paired records using the unix time stamp for when the record begins
        for recordA in recordNames:

            i = df_meta[ df_meta['recordName']== recordA].index.values[0]
            recordBeginA = df_meta.loc[i, 'recordBegin' ]
            wearableA = df_meta.loc[i, 'wearableName' ]

            for recordB in recordNames:

                j = df_meta[ df_meta['recordName']== recordB].index.values[0]
                recordBeginB = df_meta.loc[j, 'recordBegin' ]
                wearableB = df_meta.loc[j, 'wearableName' ]

                if abs(recordBeginA - recordBeginB) < 300:

                    if recordA != recordB:

                        if wearableA != wearableB:

                            print('coregister record found for ' + recordA + ' + ' + recordB)
                            coregisterList = str(recordA + ' ' + recordB)
                            df_meta.loc[i, 'coregisterRecords' ] = coregisterList

        save_meta(study, df_meta)


def define_pairedRecords():
    """

    """
    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')

    # check each study
    for study in study_list:

        df_meta = retrieve_meta(study)
        recordNames = list(df_meta['recordName'])
        df_meta['coregisterBegin'] = [0] * len(recordNames)
        df_meta['coregisterEnd'] = [0] * len(recordNames)

        # name the wearable used for each record
        for record in recordNames:

            i = df_meta[ df_meta['recordName']== record].index.values[0]
            coregisterRecords = df_meta.loc[i, 'coregisterRecords']


            if len(coregisterRecords) > len(record):
                coregisterRecords = coregisterRecords.split(' ')
                print('coregisterRecords = ')
                print(coregisterRecords)

                print('coregisterRecords[0] = ')
                print(coregisterRecords[0])

            else:
                coregisterRecords = list([coregisterRecords])

            for item in coregisterRecords:

                print('coregisterRecords = ')
                print(coregisterRecords)
                print('item = ' + item)

                format_type, segment, sensor, recordRef = 'truncate', 'All', 'TEMP', item
                source = os.path.join('studies', study, 'formatted', format_type, recordRef, segment, sensor + '.csv')
                df_source = pd.read_csv(source)

                unixMin = int(min(list(df_source['timeUnix'])) + 12)
                unixMax = int(max(list(df_source['timeUnix'])) - 12)

                if df_meta.loc[i, 'coregisterBegin' ] < unixMin or df_meta.loc[i, 'coregisterBegin' ] == 0:
                    df_meta.loc[i, 'coregisterBegin' ] = unixMin

                if df_meta.loc[i, 'coregisterEnd' ] > unixMax or df_meta.loc[i, 'coregisterEnd' ] == 0:
                    df_meta.loc[i, 'coregisterEnd' ] = unixMax


        # sort meta file by record begin and drop duplicates
        df_meta = df_meta.sort_values(by = 'wearableName')
        df_meta = df_meta.drop_duplicates('coregisterRecords', keep='first')
        df_meta = df_meta.drop_duplicates('coregisterBegin', keep='first')
        df_meta = df_meta.sort_values(by = 'recordBegin')
        save_meta(study, df_meta)



def add_wearableName(df_meta):
    """
    add a column for wearable name and sort
    """

    recordNames = list(df_meta['recordName'])
    df_meta['wearableName'] = [None] * len(recordNames)

    # name the wearable used for each record
    for record in recordNames:

        recordSplit = record.split('_')
        wearableName = recordSplit[1]

        i = df_meta[ df_meta['recordName']== record].index.values[0]
        df_meta.loc[i, 'wearableName' ] = wearableName

    # sort meta file by wearbale name
    df_meta = df_meta.sort_values(by = 'wearableName')

    return(df_meta)



def format_coregister():
    """
    combine paired record in a single csv
    save in the coregister folder of formatted data
    """

    study_list = retrieve_ref('study_list')
    sensor_list = retrieve_ref('sensor_list')

    for study in study_list:

        df_meta = retrieve_meta(study)
        recordNames = list(df_meta['recordName'])

        # name the wearable used for each record
        for record in recordNames:

            i = df_meta[ df_meta['recordName']== record].index.values[0]
            print('i = ' + str(i))
            coregisterBegin = df_meta.loc[i, 'coregisterBegin' ]
            coregisterEnd = df_meta.loc[i, 'coregisterEnd' ]
            coregisterRecords = df_meta.loc[i, 'coregisterRecords' ]

            for sensor in sensor_list:

                df_coregister = pd.DataFrame()

                if len(coregisterRecords) == len(record):
                    coregisterRecords = list([coregisterRecords])

                elif len(coregisterRecords) > len(record):
                    coregisterRecords = coregisterRecords.split(' ')

                print('coregisterRecords = ')
                print(coregisterRecords)

                for item in coregisterRecords:

                    format_type, segment, recordRef = 'truncate', 'All', item
                    source = os.path.join('studies', study, 'formatted', format_type, recordRef, segment, sensor + '.csv')
                    df = pd.read_csv(source)

                    assert coregisterEnd > coregisterBegin + 100, 'during coregister format, coregisterBegin >= coregisterEnd'
                    assert coregisterEnd < max(list(df['timeUnix'])), 'possible error with time'

                    print('coregisterEnd = ' + str(coregisterEnd) + ' timeUnixEnd = ' + str(max(list(df['timeUnix']))))
                    print('timeUnixEnd - coregisterEnd = ' + str((max(list(df['timeUnix'])) - coregisterEnd ) / 60))
                    print('coregisterEnd - timeUnixBegin = ' + str((coregisterEnd - min(list(df['timeUnix']))) / 60))

                    assert coregisterEnd > min(list(df['timeUnix']))

                    df = df[df['timeUnix'] > coregisterBegin]
                    df = df[df['timeUnix'] < coregisterEnd]

                    assert len(list(df['timeUnix'])) > 0, 'coregistered df removed'

                    recordSplit = item.split('_')
                    wearableName = recordSplit[1]

                    df_coregister['timeUnix'] = list(df['timeUnix'])
                    df_coregister['timeMinutes'] = list(df['timeMinutes'])

                    colName = str(wearableName + '_' + 'measurement')
                    print('colName = ' + colName)
                    df_coregister[colName] = list(df['measurement'])


                path = ['studies', study, 'formatted', 'coregister', record, segment]
                path = build_path(path)
                file = os.path.join(path, sensor + ".csv")
                df_coregister.to_csv(file)
                print('formatted coregister file = ' + str(file))
