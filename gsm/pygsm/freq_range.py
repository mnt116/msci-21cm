from pygsm import GlobalSkyModel, GSMObserver
from datetime import datetime
import numpy as np
import healpy as hp
import matplotlib.pyplot as plt

(latitude, longitude, elevation) = ('-26.69719', '116.63903', 373)
freq = np.linspace(50,99,3)
amp = []
for i in freq:
    gsm = GSMObserver()
    gsm.lon = longitude
    gsm.lat = latitude
    gsm.elev = elevation
    gsm.date = datetime(2018, 1, 1, 3, 0)
    g = gsm.generate(i)
    gsm.view(logged=False,filename='freq_%i'%i)
