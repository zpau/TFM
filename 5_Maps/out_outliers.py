def out_outliers(data, ncast, variable, window_size=7):
    """Function that deletes and replace the outliers 
    of a vertical profile using a moving mean calculated
    by exponential weigth (ewm) """
    #Imports
    import scipy.interpolate
    import pandas as pd
    import numpy as np
    #Approach
    mean = data[ncast][variable].ewm(window_size).mean()
    std = data[ncast][variable].ewm(window_size).std()
    std[0]=0 #the first value turns into NaN because of no data
    #Manual calculation of the moving mean non centered for the first values
    for i in range(window_size):
        mean.iloc[i]=data[ncast]['salinity'].iloc[i:i+window_size].mean()
        std.iloc[i]=data[ncast]['salinity'].iloc[i:i+window_size].std()
    std.iloc[0] = mean.iloc[0:0+window_size].std()
    
    #Threshold to detect outliers
    limite_sup = mean + 2*std
    limite_inf = mean - 2*std
    is_outlier = (data[ncast][variable] > limite_sup) | (data[ncast][variable] < limite_inf)
    outliers = data[ncast][variable][is_outlier]
    
    #Index where are located the outliers
    ind_outliers = []
    for press_outlier in outliers.index:
        index = 0
        for pressure in data[ncast].index:
            if press_outlier == pressure:
                ind_outliers.append(index)
            index+=1
            
    #Grouping the consecutive outliers
    ind_outliers_cont=[]
    count=0
    for index in ind_outliers:
        if count==(len(ind_outliers)-1):
            break
        elif index == (ind_outliers[count+1] - 1):
            #print(index, ind_outliers[count+1])
            ind_outliers_cont.append(index)
            ind_outliers_cont.append(ind_outliers[count+1])
        count+=1
        
    #Delete of the duplicate index resulting from the previous step
    result = []
    for item in ind_outliers_cont:
        if item not in result:
            result.append(item)   
    ind_outliers_cont = result
    
    #Delete the consecutive index from the original list
    for index in ind_outliers_cont:
        ind_outliers.remove(index)
        
    #Grouping the consecutive index
    change = []
    diff = np.diff(ind_outliers_cont)
    for i in range(len(diff)):
        #print(i)
        if diff[i] != 1:
            change.append(i)
    ind_cont = []
    if len(change) == 0:
        ind_cont.append(ind_outliers_cont)
    else:
        ind_cont.append(ind_outliers_cont[0:change[0]+1])
        for i in range(len(change)):
            if i == (len(change)-1):
                break
            else:
                ind_cont.append(ind_outliers_cont[change[i]+1:change[i+1]+1])
        ind_cont.append(ind_outliers_cont[change[-1]+1:])
    
    #Interpolation of the individual outliers
    pressure = data[ncast].index
    var = data[ncast][variable].values
    for index in ind_outliers:
        if index == 0:
            var[0] == data[ncast][variable].iloc[0:0+window_size].mean()
        elif pressure[index] == pressure[-1]:
            var[index]= var[index-1]    
        else:
            interp = scipy.interpolate.interp1d((pressure[index-1],pressure[index+1]),(var[index-1], var[index+1]))
            var[index]=interp(pressure[index])
    
    #Interpolation of the consecutive outliers
    for i in ind_cont:
        if 0 in i:
            for index in i:
                var[index] = var[i[-1]+1]
        else:
            for index in i:
                interp = scipy.interpolate.interp1d((pressure[i[0]-1],pressure[i[-1]+1]),(var[i[0]-1], var[i[-1]+1]))
                var[index]=interp(pressure[index])