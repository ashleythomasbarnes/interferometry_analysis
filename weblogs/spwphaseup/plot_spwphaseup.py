"""
Interactive Plot Generation for SPW Phase-up

This code generates interactive plots of the SPW phase-up based on data obtained from the 'stage14_casapy.log' file.
The code reads the log file, extracts relevant data, organizes it, and generates scatter plots for each dataset.
The resulting plots are saved as interactive HTML files.

Instructions:
1. Place the 'stage14_casapy.log' file in the same directory as this code.
2. Run the code to generate the interactive plots.

Note: The code includes print statements to provide updates on the processing progress.

"""

import numpy as np
import plotly.express as px


def get_data_from_file(filename='./stage14_casapy.log', keyword='gaincal::pipeline.extern.PIPE692::casa'):
    with open(filename, 'r') as myfile:
        data = [line for line in myfile if keyword in line]
    return np.array(data)


def get_data():
    # Read file and get data
    print("Reading data from file...")
    data = get_data_from_file()
    data_nms = get_data_from_file(keyword='Working on the MS')
    data_msnames = np.array([''] * len(data_nms), dtype='<U100')

    for i, data_nms_ in enumerate(data_nms):
        data_msnames[i] = data_nms_.split('Working on the MS ')[-1].split('\n')[0]

    dict_data = dict.fromkeys(data_msnames)
    where_ms = np.ones(len(data_nms), dtype=int)

    for i, data_nms_ in enumerate(data_nms):
        where_ms[i] = np.array(np.where(data_nms_ == data)[0], dtype=int)

    where_ms = np.append(where_ms, -1)
    data_cropped_array = []

    for i in range(len(where_ms) - 1):
        data_cropped = data[where_ms[i]:where_ms[i + 1]]
        data_cropped_array = []

        for line in data_cropped:
            if '::casa\t(' in line:
                data_cropped_array += line.split('::casa\t(')[-1].split(')\n')[0].split(', ')
                data_cropped_array[-1] = data_cropped_array[-1].replace(') - outlier\n', '')
                data_cropped_array[-1] = data_cropped_array[-1].replace('nan) - flagged\n', '')

        data_cropped_array = np.array([data_cropped_array[::3],
                                       data_cropped_array[1::3],
                                       data_cropped_array[2::3]])
        data_cropped_array = np.array(data_cropped_array)

        for j in range(len(data_cropped_array[-1])):
            if data_cropped_array[-1][j] == '':
                data_cropped_array[-1][j] = np.nan

        dict_data[data_msnames[i]] = {'baseline_name': data_cropped_array[0],
                                       'baseline': np.array(data_cropped_array[1], dtype=float),
                                       'phase': np.array(data_cropped_array[2], dtype=float)}

    print("Data processing complete.")
    return dict_data


data = get_data()

for key in data.keys():
    print(f"Generating interactive plot for {key}...")
    fig = px.scatter(x=data[key]['baseline'],
                     y=data[key]['phase'],
                     hover_name=data[key]['baseline_name'],
                     width=1000,
                     height=800,
                     labels={'x': 'baseline', 'y': 'phase'},
                     title=key,
                     log_x=True)
    fig.write_html("phaserms_%s.html" % key)

print("Plot generation complete.")