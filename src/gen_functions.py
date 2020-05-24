from .imports import *
""" Unit conversion function

"""


def merc_x(lon):
    # convert logitude in degree to mercadian in meter
    # Earth radius in meter
    # from https://wiki.openstreetmap.org/wiki/Mercator
    try:
        lon = float(lon)
    except BaseException:
        pass
    r_major = 6378137.000
    return r_major * np.radians(lon)


def merc_y(lat, shift=False):
    # convert latitude in degree to mercadian in meter
    try:
        lat = float(lat)
    except BaseException:
        pass

    if shift:
        # Add correction to latitude
        lat += 0.08

    if lat > 89.5:
        lat = 89.5
    if lat < -89.5:
        lat = -89.5

    r_major = 6378137.000
    r_minor = 6356752.3142
    temp = r_minor / r_major
    eccent = np.sqrt(1 - temp**2)
    phi = np.radians(lat)
    sinphi = np.sin(phi)
    con = eccent * sinphi
    com = eccent / 2
    con = ((1.0 - con) / (1.0 + con))**com
    ts = math.tan((math.pi / 2 - phi) / 2) / con
    y = 0 - r_major * np.log(ts)
    return y


def get_color(series:(np.array, pd.core.series.Series)=None,color_length:int=None,cmap=cm.Blues):
    """Create a list of hex colormap for a series or for a specified length """
    if series:
        #colormap from a series
        vmin = np.min(series)
        vmax = np.max(series)
    else:
        # colormap for specified lenght
        series = np.arange(color_length)
        vmin=0
        vmax = np.max(series)
    #normalize item number values to colormap
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    #colormap values = viridis, jet, spectral
    color_list = [cmap(norm(value)) for value in series]
    color_list = [str(cm.colors.to_hex(color)) for color in color_list]
    return color_list