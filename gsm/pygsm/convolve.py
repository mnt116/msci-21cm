# A script to filter, sky-average, and plot the GSM

# Importing Moduules
import healpy as hp
import numpy as np
import matplotlib.pyplot as plt
from pygsm import GlobalSkyModel, GSMObserver
from datetime import datetime, timedelta

# Pixel Count for Healpy
nside = 32
npix = hp.nside2npix(nside)

# Initial Sky Array
n = np.zeros(npix)

# Ranges for Spherical Polar Plotting
thetas = np.linspace(0, np.pi, npix)
phis = np.linspace(0, 2*np.pi, npix)

thetalim = 5*np.pi/8 # 'Aperture Width' of Beam
func = 1-(((thetas-np.pi)/(thetalim-np.pi))**2) # Beam Function
for j in phis:
    pixels = hp.ang2pix(nside, thetas, j)
    n[pixels] = func[pixels]
    n[n<0] = 0 
filter_array = n # This is the filter to apply to GSM

(latitude, longitude, elevation) = ('-32.998370', '148.263659', 100) # Near EDGES site
delta_t = 60 # EDGES antenna takes a number of measurements in 24 hours; this is the time between measurements in minutes
sky_array = []
timer = datetime(2018, 1, 1, 0, 0)
while timer.hour < 23:
    gsm = GSMObserver()
    gsm.lon = longitude
    gsm.lat = latitude
    gsm.elev = elevation
    gsm.date = timer
    g = hp.ud_grade(gsm.generate(78), nside) # 78MHz is the frequency of the 21cm signal absorption feature
    g_filt = g*n
    #g_filt = g_filt*(np.amax(g)/np.amax(g_filt)) # normalisation
    hp.orthview(g_filt, half_sky=True)
    plt.savefig(timer.strftime("%H:%M:%S")+"_filtered.png")
    g_int = np.trapz(g_filt)
    sky_array.append(g_int)
    timer = timer + timedelta(minutes=delta_t)

sky_array = np.array(sky_array)
sky = np.trapz(sky_array)
print(sky)

