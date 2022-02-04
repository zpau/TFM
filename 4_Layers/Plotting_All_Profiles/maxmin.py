def maxmin(data, ncast, variable='salinity', lamb=500000):
    """Function that determines the layers of a 
    vertical profile according to its relative
    maximums and minimums and returns the number of layers.
    data -> dict that stores the CTD files by 
            their ncast number
    variable -> str of the variable. 'salinity' default
    lamb -> (int) smooth exageration of the profile
            by default 500000
    """
    #Imports
    import statsmodels.api as sm
    import pandas as pd
    import numpy as np
    
    #Smooth the profile with its tendency
    var_cicle, var_tend = sm.tsa.filters.hpfilter(data[ncast][variable],lamb=lamb)
    
    #Calculate the 1st derivative
    der1_var_tend = np.diff(var_tend, n=1)
    
    #Index where are located the relative maxs/mins
    ind_maxmin=[]
    for i in range(len(der1_var_tend)):       
        if i == (len(der1_var_tend)-1):
            break
        elif der1_var_tend[i]*der1_var_tend[i+1] < 0:      
            ind_maxmin.append(i)
            ind_maxmin.append(i+1)        
    ind_maxmin = np.array(ind_maxmin).reshape(len(ind_maxmin)//2, 2)
    
    #Number of layers = the number of maxs/mins plus one
    nlayers = len(ind_maxmin)+1
    
    #Return the numer of layers
    return nlayers


def maxmin_plot(data, ncast, variable='salinity', lamb=500000):
    """Function that determines the layers of a 
    vertical profile according to its relative
    maximums and minimums, plots the profile 
    separated by layers and returns the number of layers.
    data -> dict that stores the CTD files by 
            their ncast number
    variable -> str of the variable. 'salinity' default
    lamb -> (int) smooth exageration of the profile
            by default 500000
    """
    #Imports
    import statsmodels.api as sm
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    
    #Smooth the profile with its tendency
    var_cicle, var_tend = sm.tsa.filters.hpfilter(data[ncast][variable],lamb=lamb)
    
    #Calculate the 1st derivative
    der1_var_tend = np.diff(var_tend, n=1)
    
    #Index where are located the relative maxs/mins
    ind_maxmin=[]
    for i in range(len(der1_var_tend)):       
        if i == (len(der1_var_tend)-1):
            break
        elif der1_var_tend[i]*der1_var_tend[i+1] < 0:      
            ind_maxmin.append(i)
            ind_maxmin.append(i+1)        
    ind_maxmin = np.array(ind_maxmin).reshape(len(ind_maxmin)//2, 2)
    
    #Depths where are located the maxs/mins
    pres_maxmin = []
    for i in ind_maxmin:
        pressure = (data[ncast].index[i[0]]+data[ncast].index[i[1]])/2
        pres_maxmin.append(pressure)
        
    #Number of layers = the number of maxs/mins plus one
    nlayers = len(ind_maxmin)+1
    print('Profile '+ncast+' has '+str(nlayers)+' layers')
    
    #Now we plot the result of the profile with its layers
    fig, (ax0, ax1) = plt.subplots(1,2,figsize=(12,7))
    ax0.plot(data[ncast][variable], data[ncast].index)
    ax0.invert_yaxis()
    for i in pres_maxmin:
        ax0.axhline(y=i, c='grey')
    ax0.set_title(ncast+' '+variable)
    ax1.plot(var_tend, data[ncast].index)
    ax1.invert_yaxis()
    for i in pres_maxmin:
        ax1.axhline(y=i, c='grey')
    ax1.set_title(ncast+' Smooth '+variable)
    plt.show()
    
    #Return the number of layers
    return nlayers



def maxmin_2(data, ncast, variable='salinity', lamb=500000, min_layer=51):
    """Function that determines the layers of a 
    vertical profile according to its relative
    maximums and minimums and returns the number of layers.
    The layers closer than 50m are replaced by just
    one layer centered"""
    #Imports
    import statsmodels.api as sm
    import pandas as pd
    import numpy as np
    
    #Smooth the profile
    var_ciclo, var_tend = sm.tsa.filters.hpfilter(data[ncast][variable],lamb=lamb)

    #Calculate the 1st derivative of the smooth profile
    der1_var_tend = np.diff(var_tend, n=1)

    #Now we find those points where the 1st derivative is 0 (relative maximums and minimums)
    ind_maxmin=[]
    for i in range(len(der1_var_tend)):       
        if i == (len(der1_var_tend)-1):
            break
        elif der1_var_tend[i]*der1_var_tend[i+1] < 0:      
            ind_maxmin.append(i)
            ind_maxmin.append(i+1)        
    ind_maxmin = np.array(ind_maxmin).reshape(len(ind_maxmin)//2, 2)

    #Now we find the depths of those maxs/mins
    pres_maxmin = []
    for i in ind_maxmin:
        pressure = (data[ncast].index[i[0]]+data[ncast].index[i[1]])/2
        pres_maxmin.append(pressure)
    
    #Store the number of layers
    nlayers = len(pres_maxmin) + 1
    
    #Store the maxs/mins closer than 50m
    pres = []
    for i in range(len(pres_maxmin)):
        if i == (len(pres_maxmin)-1):
            break
        elif (pres_maxmin[i+1]-pres_maxmin[i])<min_layer:
            pres.append(pres_maxmin[i])
            pres.append(pres_maxmin[i+1])
    pres = list(set(pres))
    pres.sort()

    #If there are no maxs/mins closer than 50m it ends here
    if len(pres) == 0:
        return nlayers
    
    #Group the maxs/mins closer than 50m
    dif_pres = np.diff(pres)            #calculates the difference between maxs/mins
    groups = []                         #indexs that separate the groups
    for i in range(len(dif_pres)):
        if dif_pres[i] > min_layer:            #if the difference is bigger than 50, get the index
            groups.append(i)
    pres_groups = []
    
    if len(groups) == 0:                #If there is just 1 group all the pressures are stored
        pres_groups.append(pres)
    if len(groups) == 1:                #If there are 2 groups the indexs are separated this way
        pres_i = []
        pres_i = pres[0:groups[0]+1]
        pres_groups.append(pres_i)
        pres_i = []
        pres_i = pres[groups[0]+1:]
        pres_groups.append(pres_i)
    if len(groups) > 1:                     #If there are more than 2 groups, indexs are separated this way
        for i in range(len(groups)):
            if i == 0:
                pres_i = []
                pres_i = pres[0:groups[0]+1]
                pres_groups.append(pres_i)
            elif groups[i] == groups[-1]:
                pres_i = []
                pres_i = pres[groups[i-1]+1:groups[i]+1]
                pres_groups.append(pres_i)
                pres_i = []
                pres_i = pres[groups[-1]+1:]
                pres_groups.append(pres_i)       
            else:
                pres_i = []
                pres_i = pres[groups[i-1]+1:groups[i]+1]
                pres_groups.append(pres_i)
                
    new_pres=[]
    for i in pres_groups:
        pres_i = (i[0]+i[-1])/2
        new_pres.append(pres_i)

    #De la lista de maximos/minimos eliminamos los valores demasiado juntos y añadimos su sustituto
    pres_maxmin2 = []
    for i in pres_maxmin:
        pres_maxmin2.append(i)

    for i in pres_groups:
        for pressure in i:
            pres_maxmin2.remove(pressure)
    for i in new_pres:
        pres_maxmin2.append(i)

    #Guardamos el nuevo numero de capas
    nlayers2 = len(pres_maxmin2) +1
    
    nlayers = nlayers2
    return nlayers




def maxmin_2_plot(data, ncast, variable='salinity', lamb=500000, min_layer=51):
    """Function that determines the layers of a 
    vertical profile according to its relative
    maximums and minimums, plots the result and
    returns the number of layers.
    The layers closer than 50m are replaced by just
    one layer centered """
    #Imports
    import statsmodels.api as sm
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    
    #Smooth the profile
    var_ciclo, var_tend = sm.tsa.filters.hpfilter(data[ncast][variable],lamb=lamb)

    #Calculate the 1st derivative of the smooth profile
    der1_var_tend = np.diff(var_tend, n=1)

    #Now we find those points where the 1st derivative is 0 (relative maximums and minimums)
    ind_maxmin=[]
    for i in range(len(der1_var_tend)):       
        if i == (len(der1_var_tend)-1):
            break
        elif der1_var_tend[i]*der1_var_tend[i+1] < 0:      
            ind_maxmin.append(i)
            ind_maxmin.append(i+1)        
    ind_maxmin = np.array(ind_maxmin).reshape(len(ind_maxmin)//2, 2)

    #Now we find the depths of those maxs/mins
    pres_maxmin = []
    for i in ind_maxmin:
        pressure = (data[ncast].index[i[0]]+data[ncast].index[i[1]])/2
        pres_maxmin.append(pressure)
    
    #Store the number of layers
    nlayers = len(pres_maxmin) + 1
    
    #Store the maxs/mins closer than 50m
    pres = []
    for i in range(len(pres_maxmin)):
        #print(i)
        if i == (len(pres_maxmin)-1):
            break
        elif (pres_maxmin[i+1]-pres_maxmin[i])<min_layer:
            pres.append(pres_maxmin[i])
            pres.append(pres_maxmin[i+1])
    pres = list(set(pres))
    pres.sort()

    #If there are no maxs/mins closer than 50m it ends here
    if len(pres) == 0:
        #print('Profile ncast '+ncast+':')
        #print('There are no maxs/mins too close')
        #print('Number of layers: '+str(nlayers))
        fig, ax0 = plt.subplots(figsize=(5,7))
        ax0.plot(data[ncast][variable], data[ncast].index)
        ax0.invert_yaxis()
        for i in pres_maxmin:
            ax0.axhline(y=i, c='grey')
        ax0.set_title('Profile '+ncast+' - 2nd APROX')
        return nlayers
    
    #Group the maxs/mins closer than 50m
    dif_pres = np.diff(pres)            #calculates the difference between maxs/mins
    groups = []                         #indexs that separate the groups
    for i in range(len(dif_pres)):
        if dif_pres[i] > min_layer:            #if the difference is bigger than 50, get the index
            groups.append(i)
    pres_groups = []
    
    if len(groups) == 0:                #If there is just 1 group all the pressures are stored
        pres_groups.append(pres)
    if len(groups) == 1:                #If there are 2 groups the indexs are separated this way
        pres_i = []
        pres_i = pres[0:groups[0]+1]
        pres_groups.append(pres_i)
        pres_i = []
        pres_i = pres[groups[0]+1:]
        pres_groups.append(pres_i)
    if len(groups) > 1:                     #If there are more than 2 groups, indexs are separated this way
        for i in range(len(groups)):
            if i == 0:
                pres_i = []
                pres_i = pres[0:groups[0]+1]
                pres_groups.append(pres_i)
            elif groups[i] == groups[-1]:
                pres_i = []
                pres_i = pres[groups[i-1]+1:groups[i]+1]
                pres_groups.append(pres_i)
                pres_i = []
                pres_i = pres[groups[-1]+1:]
                pres_groups.append(pres_i)       
            else:
                pres_i = []
                pres_i = pres[groups[i-1]+1:groups[i]+1]
                pres_groups.append(pres_i)
                
    new_pres=[]
    for i in pres_groups:
        pres_i = (i[0]+i[-1])/2
        new_pres.append(pres_i)

    #De la lista de maximos/minimos eliminamos los valores demasiado juntos y añadimos su sustituto
    pres_maxmin2 = []
    for i in pres_maxmin:
        pres_maxmin2.append(i)

    for i in pres_groups:
        #print(i)
        for pressure in i:
            #print(pressure)
            pres_maxmin2.remove(pressure)
    for i in new_pres:
        pres_maxmin2.append(i)

    #Guardamos el nuevo numero de capas
    nlayers2 = len(pres_maxmin2) +1
    #print('Profile ncast ',ncast,':')
    #print('Number of layers 2nd APROX: ',str(nlayers),'                             Number of layers 3rd APROX: ', str(nlayers2))
    
    #Ploteamos el resultado    
    fig, (ax0, ax1) = plt.subplots(1,2,figsize=(10,7))
    ax0.plot(data[ncast][variable], data[ncast].index)
    ax0.invert_yaxis()
    for i in pres_maxmin:
        ax0.axhline(y=i, c='grey')
    ax0.set_title('Profile '+ncast+' - 2nd APROX')
    ax1.plot(data[ncast][variable], data[ncast].index)
    ax1.invert_yaxis()
    for i in pres_maxmin2:
        ax1.axhline(y=i, c='grey')
    ax1.set_title('3rd APROX')
    plt.show()
    print()
    
    nlayers = nlayers2
    return nlayers