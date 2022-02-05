def mapa(data, ncasts, xoffset=2, yoffset=2, s=30, labels=False, lines=False):
    """Plot a map of the stations (ncasts) indicated 
    ncasts = list of the stations ncast"""
    #Imports
    import matplotlib.pyplot as plt
    import cartopy
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import cmocean
    
    fig = plt.figure(figsize=(10,10))
    m1 = fig.add_subplot(projection=ccrs.PlateCarree())

    #Add features
    m1.add_feature(cfeature.LAND, edgecolor='lightyellow')
    m1.coastlines('10m')

    #Añadimos la batimetria de Natural Earth
    #Codigo de https://nbviewer.org/gist/pelson/626b15ffc411a359381e
    cmap = cmocean.cm.ice_r          #Barra de colores para la batimetria
    norm = plt.Normalize(0, 8000)    #Normalizado de la gama de colores de 0m a 8000m

    #Importamos las capas de batimetria que nos interesan
    for letter, level in [
                          ('L', 0),
                          ('K', 200),
                          ('J', 1000),
                          ('I', 2000),
                          ('H', 3000),
                          ('G', 4000),
                          ('F', 5000)]:
                          #('E', 6000),
                          #('D', 7000)]:
                          #('C', 8000),
                          #('B', 9000),
                          #('A', 10000)]:
        bathym = cfeature.NaturalEarthFeature(name='bathymetry_{}_{}'.format(letter, level),
                                     scale='10m', category='physical')
        m1.add_feature(bathym, facecolor=cmap(norm(level)), edgecolor='face', alpha=0.5)  #alpha=transparencia

    #Establecemos los límites del mapa
    #Margenes del mapa en x i y (xoffset,yoffset) por defecto son 2º
    #Recopilamos las coordenadas de todas las estaciones de interes
    longitudes = []
    latitudes = []
    for ncast in ncasts:
        longitudes.append(data[ncast]['longitude'].iloc[0])
        latitudes.append(data[ncast]['latitude'].iloc[0])
    #Guardamos el mínimo y el máximo de las coordenadas para establecer los límites del mapa
    min_lon = min(longitudes)
    max_lon = max(longitudes)
    min_lat = min(latitudes)
    max_lat = max(latitudes)
    #Definimos los límites del mapa
    m1.set_extent([min_lon-xoffset, max_lon+xoffset, min_lat-yoffset, max_lat+yoffset])

    #Añadimos los puntos de las estaciones de estudio 
    for ncast in ncasts:
        m1.scatter(data[ncast].longitude.iloc[0], data[ncast].latitude.iloc[0], color='red',s=s, transform=ccrs.PlateCarree(),zorder=10)
        if labels == True:
            plt.text(data[ncast].longitude.iloc[0], data[ncast].latitude.iloc[0], ncast)
    
    #Add lines to show the navigation between stations
    if lines == True:
        m1.plot(longitudes, latitudes, color='grey', transform=ccrs.PlateCarree(), zorder=11)
        #Add legend
        m1.legend(['Navigation','CTD stations'], loc='lower right')
        
    #Add legend    
    if lines == False:
        m1.legend(['CTD stations'], loc='lower right')
        
    #Añadimos una color bar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cb = plt.colorbar(sm,
                      orientation='horizontal',
                      shrink=0.65,
                      pad=0.03,
                      label = 'Bathymetry (m)')
    plt.title('TRANSMOW 2021')
    m1.gridlines(crs=ccrs.PlateCarree() ,draw_labels=True, color='lightgrey')
    plt.show()
    
    

    
    
def map_layers(data, layers, extent=False, xoffset=0.5, yoffset=0.5, s=30, colors=['b','g','r','c','m','y','k','w']):
    """ Function that generates a map of the study zone and shows
    the stations classified in base of their number of layers.
    data -> dictionary that store all the DFs of the CTDs stations
    layers -> table that classifies the stations based on the number of layers
    extent -> list of the limits of the map ex: [lon1,lon2,lat1,lat2]"""
    #Imports
    import matplotlib.pyplot as plt
    import cartopy
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import cmocean
    
    #Function to plot de legend without duplicates
    def legend_without_duplicate_labels(ax,loc):
        handles, labels = ax.get_legend_handles_labels()
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        ax.legend(*zip(*unique), loc=loc)

    fig = plt.figure(figsize=(10,10))
    m1 = fig.add_subplot(projection=ccrs.PlateCarree())
    m1.add_feature(cfeature.LAND, edgecolor='lightyellow')
    m1.coastlines('10m')
    cmap = cmocean.cm.ice_r          #Color bar for the bathymetry
    norm = plt.Normalize(0, 8000)    #Normalization of the bathymetry colors from 0 to 8000m
    for letter, level in [
                          ('L', 0),
                          ('K', 200),
                          ('J', 1000),
                          ('I', 2000),
                          ('H', 3000),
                          ('G', 4000),
                          ('F', 5000)]:
        bathym = cfeature.NaturalEarthFeature(name='bathymetry_{}_{}'.format(letter, level),
                                     scale='10m', category='physical')
        m1.add_feature(bathym, facecolor=cmap(norm(level)), edgecolor='face', alpha=0.5)  #alpha=transparency
    longitudes = []
    latitudes = []
    for ncast in data.keys():     #loop of all the stations
        longitudes.append(data[ncast]['longitude'].iloc[0])
        latitudes.append(data[ncast]['latitude'].iloc[0])   
    xoffset = xoffset
    yoffset = yoffset
    min_lon = min(longitudes)
    max_lon = max(longitudes)
    min_lat = min(latitudes)
    max_lat = max(latitudes)    
    #Set extent
    if extent == False:
        m1.set_extent([min_lon-xoffset, max_lon+2*xoffset, min_lat-yoffset, max_lat+yoffset])  #Set the map limits
    if extent != False:
        m1.set_extent([extent[0]-xoffset, extent[1]+2*xoffset, extent[2]-yoffset, extent[3]+yoffset])    
    #Add the stations coordinates as points
    colors = colors
    n=0
    for ncasts in layers:
        for ncast in ncasts:
            m1.scatter(data[ncast].longitude.iloc[0], data[ncast].latitude.iloc[0],label=str(layers.index[n])+' capas' , color=colors[n],s=s, transform=ccrs.PlateCarree(), edgecolors='black',zorder=10)
        n+=1    
    #Adding of a color bar 
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cb = plt.colorbar(sm,
                      orientation='horizontal',
                      shrink=0.65,
                      pad=0.03,
                      label = 'Bathymetry (m)')
    #Add coordinates grid
    m1.gridlines(crs=ccrs.PlateCarree() ,draw_labels=True, color='lightgrey')
    #Add title and legend
    plt.title('TRANSMOW 2021')
    legend_without_duplicate_labels(m1,loc='lower right')
    plt.show()