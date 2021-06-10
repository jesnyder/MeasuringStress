
import glob
import os
import pandas as pd

def retrieve_meta(study):
    """
    retrieve metadata
    """

    metadata_path = os.path.join('studies', study, 'meta')
    metadata_file = os.path.join(metadata_path, 'metadata.csv')
    # print('metadata_file = ' + str(metadata_file))
    df = pd.read_csv(metadata_file)

    # remove unnamed columns created from reading in the csv
    col_names = df.head()
    for name in col_names:
        if 'Unnamed' in name:
            del df[name]

    return(df)
