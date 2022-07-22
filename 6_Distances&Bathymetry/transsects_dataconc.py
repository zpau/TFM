def transsects_dataconc(data, transsects, distances=False):
    """
    Function that creates a concatenate DF of all the stations of a transsects. Useful to then plot the data.
    data -> dict with the CTD df of the diferent stations
    transsects -> dict with the number of the transsect (key) and a list of ncasts of the transsect stations
    distances -> dict with the distances between the transsect stations are stored according to its transsect number.
            defect = False -> the conc dataframe will not have the distances
    returns -> dict where the concatenate DF of each transsect (value) is stored according to the transsect number (key)
    """
    import numpy as np
    import pandas as pd
    dataconc_transsects = {}
    for n_trans in transsects:
        
        data_conc = pd.DataFrame()
        
        if distances == False:
            for ncast in transsects[n_trans]:
                if data_conc.empty:
                    data_conc = data[ncast]
                else:
                    data_conc = pd.concat([data_conc, data[ncast]])
            dataconc_transsects[n_trans] = data_conc
        
        else:
            for ncast, tmp in zip(transsects[n_trans], distances[n_trans]):
                if data_conc.empty:
                    data[ncast]['distances'] = tmp    # Create new column in dataframe with calculated dists
                    data_conc = data[ncast]
                else:
                    data[ncast]['distances'] = tmp
                    data_conc = pd.concat([data_conc, data[ncast]])
            dataconc_transsects[n_trans] = data_conc
            
    return dataconc_transsects