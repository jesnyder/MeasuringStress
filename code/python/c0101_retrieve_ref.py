import os
import pandas as pd

def retrieve_ref(valueName):
    """
    Input: value name
    Output: value saved in reference file
    """

    # reference file located
    # cwd = os.getcwd()
    # print("cwd = ")
    # print(str(cwd))

    # specifiy path to reference file
    ref_path = os.path.join( 'ref')
    ref_file = os.path.join(ref_path, 'reference' + '.csv' )
    # print('ref path: ' + str(ref_file))

    # read in all reference values as a dataframe
    df = pd.read_csv(ref_file)
    # del df['Unnamed: 0']

    # print('ref = ')
    # print(df)

    # print(df['valueName'])
    # print(valueName)

    # search the dataframe using string matching
    # looking for the same string as passed into the function
    valueRow = df[df['valueName'].str.match(valueName)]

    # if not match is found
    # then write the value into the reference file to be specified
    if len(list(df['valueName'])) == 0:
        file = open(ref_file, "a")
        file.write('\n')
        file.write(valueName)
        file.write(' , unspecified')
        file.write('\n')
        file.close()
        print('item missing from reference file - ' + str(valueName))

    # print("valueRow = ")
    # print(valueRow)

    #
    valueValue = valueRow.iloc[0,1]
    valueValue = str(valueValue)
    valueValue = valueValue.split(' ')

    valueValue = list(valueValue)

    for i in valueValue:
        if len(i) < 1:
            valueValue.remove(i)

    if len(valueValue) == 1:
        valueValue = float(valueValue[0])

    # print(str(valueName) + ' = ')
    # print(valueValue)

    return(valueValue)



def retrieve_ref_color(valueName):
    """
    for a named variable
    return the color used in scatter plots
    """

    segment_list = retrieve_ref('segment_list')
    if valueName in segment_list:
        valueName = str('color_' + valueName)

    # print('valueName = ' + str(valueName))
    valueValue = retrieve_ref(valueName)

    valueColor = []
    for item in valueValue:
        valueColor.append(float(item))

    valueColor = list(valueColor)
    return(valueColor)


def retrieve_sensor_unit(sensor):
        """
        for a sensor
        return the associated unit
        """

        sensor_list = retrieve_ref('sensor_list')
        sensor_unit_list = retrieve_ref('sensor_unit_list')


        for i in range(len(sensor_list)):

            if sensor == sensor_list[i]:

                sensor_unit = sensor_unit_list[i]

        return(sensor_unit)


def retrieve_ref_color_wearable_segment(wearable_num, segment):
    """

    """

    colorWearable = retrieve_ref_color(segment)

    refName = str('color_modifier_wearable_' + str(wearable_num))
    # print('refName = ' + str(refName))
    modifier = retrieve_ref(refName)

    colorWearableSegment = []

    for item in colorWearable:

        colorWearableSegment.append(modifier * item)

    # print('colorWearableSegment = ')
    # print(colorWearableSegment)

    if max(colorWearableSegment) >= 1:

        for i in range(len(colorWearableSegment)):

            colorWearableSegment[i] = colorWearableSegment[i]/(1.2*max(colorWearableSegment))


    # print('colorWearableSegment = ')
    # print(colorWearableSegment)

    return(colorWearableSegment)
