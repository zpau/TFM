def transsect_distances(data, transsects):
    """
    function to compute the distances of 
    the stations of a transsect
    data -> dict of the CTD data of all the stations
    transsects -> dict of the ncasts that form the different transsects
    
    Returns a dict with the lists of the distances (values) of each transsect (keys)
    """
    #Imports
    import numpy as np
    import pandas as pd
    import sys 
    from shapely.geometry import Point, LineString, MultiPoint
    def path_to_points(path, resolution=False, npoints=False, pin_end=True):
        import numpy as np
        import pandas as pd
        import geopandas as gpd
        from shapely.geometry import Point, LineString, MultiPoint
        lonlat_crs = {'init': 'epsg:4326'}
        proj_crs={'init': 'epsg:3338'}
        if resolution or npoints:
            # in this case, divide the path equally by the value
            if npoints:
                interpolated_path = [path.interpolate((i/(npoints-1)), normalized=True) for i in range(0, npoints)]

            # otherwise, use the value as a distance to increment the path
            if resolution:
                npoints = int(path.length / resolution)
                interpolated_path = [path.interpolate((i*resolution)) for i in range(0, npoints+1)]

                # Add the last point, regardless of distance
                if pin_end:
                    interpolated_path.append(Point(list(path.coords)[-1]))

            points = gpd.GeoDataFrame(crs=proj_crs,geometry=interpolated_path)

            return points

        else:
            return False

    def get_lon(point):
        return point.x

    def get_lat(point):
        return point.y

    def find_nearest(array, value):
        import numpy as np
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    def point_to_index(point):
        import netCDF4
        import numpy as np
        import pandas as pd
        gebco = 'C:/Users/pauab/Universidad/Data/TFM/Bathymetry/GEBCO_16_Feb_2022_8d3ca050bc32/gebco_2021_n44.857177734375_s34.991455078125_w-11.97509765625_e-4.37255859375.nc'

        with netCDF4.Dataset(gebco) as netcdf:
        #     print(netcdf.variables)
            x = np.array(netcdf.variables['lon'][:])
            y = np.array(netcdf.variables['lat'][:])
            z = np.squeeze(np.array(netcdf.variables['elevation'][:]))
        # x
        x_index = find_nearest(x, point.x)

        #y
        y_index = find_nearest(y, point.y)

        return (y_index, x_index)

    def get_bathy_value(point):
        import netCDF4
        import numpy as np
        import pandas as pd
        gebco = 'C:/Users/pauab/Universidad/Data/TFM/Bathymetry/GEBCO_16_Feb_2022_8d3ca050bc32/gebco_2021_n44.857177734375_s34.991455078125_w-11.97509765625_e-4.37255859375.nc'
        with netCDF4.Dataset(gebco) as netcdf:
        #     print(netcdf.variables)
            x = np.array(netcdf.variables['lon'][:])
            y = np.array(netcdf.variables['lat'][:])
            z = np.squeeze(np.array(netcdf.variables['elevation'][:]))
        return z[point_to_index(point)]

    def get_distance(points):
        import numpy as np
        import pandas as pd
        # fast!
        xs = np.array([points['geometry'].iloc[i].x for i in range(len(points))])
        ys = np.array([points['geometry'].iloc[i].y for i in range(len(points))])

        distances = np.empty(len(xs))

        for i in range(0, len(xs)):
            distances[i] = np.sqrt((xs[i]-xs[0])**2 + (ys[i]-ys[0])**2)

        # looks better but slooow
        # points['distance'] = 0
        # for i in trange(1, len(points)):
        #     points['distance'].loc[i] = points['geometry'].iloc[i].distance(points['geometry'].iloc[0])

        return distances

    def get_profile(start_profile, end_profile, resolution=False, plot=False, save=False, npoints=False, pin_end=True):
        import geopandas as gpd
        import numpy as np
        import pandas as pd
        from shapely.geometry import Point, LineString, MultiPoint
        lonlat_crs = {'init': 'epsg:4326'}
        proj_crs={'init': 'epsg:3338'}
        # If we want equal distance (in meters) between our profiles, we need to work in projected coords
        # geopandas converts easily

        pathdf = gpd.GeoDataFrame(crs=lonlat_crs, geometry=[start_profile, end_profile])
        pathdf = pathdf.to_crs(proj_crs)

        path = LineString([pathdf['geometry'].loc[0], pathdf['geometry'].loc[1]])

        if not resolution and not npoints:
                npoints=100
                print('Using ' + str(npoints) + ' points')

        points = path_to_points(path, resolution=resolution, npoints=npoints, pin_end=pin_end)
        points['longitude'] = points.to_crs(lonlat_crs)['geometry'].apply(get_lon)
        points['latitude'] = points.to_crs(lonlat_crs)['geometry'].apply(get_lat)

        points['distance'] = get_distance(points)
        points = points.to_crs(lonlat_crs)
        points['bathymetry'] = points['geometry'].apply(get_bathy_value)

        if plot:
            create_plot(points)

        if save:
            points.rename(columns={'distance':'distance (m)', 'bathymetry':'depth (m)'}).drop(columns=['geometry']).to_csv('output.csv', index=False)

        return points

    # Define auxiliary function to compute distance from start point depth wise
    # at the concatenated CTD dataframe for  plotting purposes

    # Coarse resolution, adjust at will

    def dist_aux(start_lat, start_lon, point_lat, point_lon):
        import numpy as np
        import pandas as pd
        from shapely.geometry import Point, LineString, MultiPoint
        temp_profile = pd.DataFrame(get_profile(Point(start_lon, start_lat),
                                            Point(point_lon, point_lat),resolution=10000))
        return temp_profile['distance'].iloc[-1]
    
    
    
    #now, the function
    distances = {}
    for transsect in transsects.keys():
        #Get the lat and lon of the transsect stations
        station_lats = []
        station_longs = []
        for ncast in transsects[transsect]:
            station_lats.append(data[ncast]['latitude'].iloc[-1])
            station_longs.append(data[ncast]['longitude'].iloc[-1])

        # Define temp variable to store results
        tmp_dist = []

        # Iterate over lats and longs and number of stations to compute distances
        for i, j, k in zip(station_lats, station_longs, range(len(station_lats))):

            # First distance from section_start (xoffset) and first ctd station
            if k == 0:
                tmp_dist.append(dist_aux(station_lats[0], station_longs[0], i, j))
                tmp_lat = i
                tmp_lon = j
            else:
                tmp_dist.append(dist_aux(tmp_lat, tmp_lon, i, j))
                tmp_lat = i
                tmp_lon = j

        # Perform cumulative summatory
        tmp_dist = list(np.cumsum(tmp_dist))

        #Add distances to the dictionary
        distances[transsect] = tmp_dist
        
    return distances