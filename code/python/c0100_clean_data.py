
from c0106_find_records import find_records
from c0112_define_records import define_records
from c0113_format_source import format_source
from c0114_format_truncate import format_truncate
from c0116_coregister_formatted import coregister_formatted
from c0117_clean_save import clean_save
from c0118_segment_formatted import segment_formatted


import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



def clean_data():
    """
    Clean the data so each record only includes information measured from the participant.

    If the wearable is taken off and then turned off - the extra time off-wrist is truncated
    If the wearable is left on between participants, so two records are combined in one - the record is broken into two
    If two wearables were used to (one on the left and one on the right wrist) - the data is coregistered.
    Timestamps are assigned to the measurements.
    Records are broken into segment for comparision - preStudy, Study, postStudy

    Here are some definitions:

    1. source - a description of data, uneditted measurements downloaded from the cloud client
    2. truncate - a description of data, source data only when on the participant's wrist

    3. timestamp - action taken on the data, create the lit of unix and time in minutes corresponding to the measurements
    4. coregister - action taken on the data, pair up records, for some studies two wearables were used for the same patient
    5. segment - action taken on the data, break the entire truncated record into a preStudy, Study, and postStudy period

    6. define record - processing step, establish the beginning and end of the record in unix time
    7. embedded record - type of record, a record that contains two separate recorded session from what could be two people
    embeddd records need to be broken up into two separate records, which is handled in this cleaning process

    How is the end of the record found?
    Use the temperature sensor. The room is significantly colder than the participant's wrist.
    If the temperature drops more than 2 deg C in 3 seconds - the wearable is assummed removed.
    If the temperature rises more than 2 deg C in 3 seconds - the wearable is assummed put on - only used for embedded records.
    """

    print("begin cleaning data")


    # find and list all records
    find_records()

    # define record - find record begin, end, length
    define_records()

    # timestamp the source
    format_source()

    # timestamp the source
    format_truncate()

    # coregister wearables
    coregister_formatted()

    # save processed data as clean
    clean_save()

    # segment clean records
    format_type = 'clean'
    segment_formatted(format_type)

    print("completed cleaning data")
