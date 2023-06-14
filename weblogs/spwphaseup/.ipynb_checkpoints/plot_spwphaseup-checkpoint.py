import numpy as np
import plotly.express as px

def get_datafromfile(filename='./stage14_casapy.log', str='gaincal::pipeline.extern.PIPE692::casa'):
    myfile = open(filename, 'r')
    data = []
    for line in myfile:
        if str in line:
            data+=[line]
    return(np.array(data))

def get_data():
    
    #Read file and get data
    data = get_datafromfile()
    data_nms = get_datafromfile(str='Working on the MS')
    
    #Organise dictionary
    data_msnames = np.array(['']*len(data_nms), dtype='<U100')
    for i in range(len(data_nms)):
        # print(data_nms[i].split('Working on the MS ')[-1].split('\n')[0])
        data_msnames[i] = data_nms[i].split('Working on the MS ')[-1].split('\n')[0]
    dict_data = dict.fromkeys(data_msnames)
    
    #Oragnise multiple MS in dictionary
    where_ms = np.array(np.where(data_nms == data)[0], dtype=int)
    where_ms = np.append(where_ms, -1)

    data_cropped_array = []

    for i in range(len(where_ms)-1): 
        # print(where_ms[[i,i+1]])
        data_cropped = data[where_ms[i]:where_ms[i+1]]

        for line in data_cropped: 
            if '::casa\t(' in line:
                data_cropped_array += line.split('::casa\t(')[-1].split(')\n')[0].split(', ')

        data_cropped_array = np.array([data_cropped_array[::3], 
                                  data_cropped_array[1::3], 
                                  data_cropped_array[2::3]])

        dict_data[data_msnames[i]] = data_cropped_array
        dict_data[data_msnames[i]] = {'baseline_name':data_cropped_array[0],
                                     'baseline':np.array(data_cropped_array[1], dtype=float),
                                     'phase':np.array(data_cropped_array[2], dtype=float)}
        
    return(dict_data)


data = get_data()
data[list(data.keys())[0]]['phase']

fig = px.scatter(x=data[list(data.keys())[0]]['baseline'], 
                 y=data[list(data.keys())[0]]['phase'],
                 hover_name=data[list(data.keys())[0]]['baseline_name'],
                 width=700,
                 height=500, 
                 labels={'x':'baseline', 'y':'phase'})
fig.show()