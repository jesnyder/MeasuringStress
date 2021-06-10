
import glob
import os
import pandas as pd

from c0102_build_path import build_path

def save_meta(study, df):
    """
    save the metadata to folder
    save a copy to the archive folder in the metadata folder
    """

    print("begin saving metadata")


    # remove unnamed columns created from reading in the csv
    col_names = df.head()
    for name in col_names:
        if 'Unnamed' in name:
            del df[name]

    # metadata_path = os.path.join('studies', study, 'meta')
    metadata_path = build_path(['studies', study, 'meta'])
    metadata_file = os.path.join(metadata_path, 'metadata.csv')
    # print('metadata_file = ' + str(metadata_file))
    df.to_csv(metadata_file)


    # metadata_path = os.path.join('studies', study, 'meta', 'archive')
    metadata_path = build_path(['studies', study, 'meta', 'archive'])

    col_names = list(df.columns)

    # print('col_names ')
    # print(col_names)
    # print('len(col_names) = ' + str(len(col_names)))

    if len(col_names) == 1:
        print('metadata archive deleted. ')

        meta_files_archived = os.listdir(metadata_path)

        for file in meta_files_archived:
            file = os.path.join(metadata_path , file)
            # print('file = ' + str(file))
            os.remove(file)

    if not os.path.isdir(metadata_path): os.mkdir(metadata_path)

    meta_files_archived = os.listdir(metadata_path)
    iteration = int(len(meta_files_archived))+1
    # print('iteration = ' + str(iteration))

    metadata_file = os.path.join(metadata_path, 'metadata' + '_' + str(iteration) + '.csv')
    # print('metadata_file = ' + str(metadata_file))
    df.to_csv(metadata_file)

    print("completed saving metadata")
