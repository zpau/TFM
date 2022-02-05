def read_CTD(data_dirs):
    """Open and read CTD files in format .cnv
    Deletes the next columns: 'CStarAt0','CStarTr0','nbf','scan','sfdSM','turbWETntu0','nbin','flag'
    Renames the variables as: ['density','sigma','depth','fluorescence','oxygen','pot_temperature','salinity','temperature','latitude','longitude']
    arguments:
    data_dirs = path that contains the .cnv files"""
    #Imports
    import ctd #must be in version 1.1.1
    import os
    filenames = []
    for data_dir in data_dirs:
        items = os.listdir(data_dir)
        for names in items:
            if names.endswith('.cnv'):
                filenames.append(os.path.join(data_dir, names))
    dataset = {}
    for file in filenames:
        cast_num = file[-19:-17]
        down_, up_ = ctd.from_cnv(file).split()
        dataset[cast_num] = down_
    columnsNOT = ['CStarAt0','CStarTr0','nbf','scan','sfdSM','turbWETntu0','nbin','flag']
    for i in dataset.keys():
        for column in dataset[i].columns:
            if column in columnsNOT:
                del dataset[i][column]
    for i in dataset.keys():
        old_names = list(dataset[i].columns)
        new_names = ['density','sigma','depth','fluorescence','oxygen','pot_temperature','salinity','temperature','latitude','longitude']
        name_columns = dict(zip(old_names, new_names))
        dataset[i].rename(columns=name_columns, inplace=True)
    return dataset