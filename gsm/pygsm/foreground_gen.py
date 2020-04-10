# A script to generate radio foregrounds using the GSM

# Importing Modules
import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from int_sky import int_sky

# Defining Beam-Effects Filter
nside = 16
npix=hp.nside2npix(nside)
n = np.zeros(npix) # initial sky array
nwindow = 2 # define number of windows

thetas = np.linspace(0, np.pi, npix) 
phis = np.linspace(0, 2*np.pi, npix) # spherical polar values for creating filter

thetalim = 5*np.pi/8 # 'Aperture Width' of Beam
func = 1-(((thetas-np.pi)/(thetalim-np.pi))**2) # Quadratic Beam Function
for j in phis:
    pixels = hp.ang2pix(nside, thetas, j)
    n[pixels] = func[pixels]
    n[n<0] = 0 
filter_array = n # This is the filter to apply to GSM
   
sky_times = [[23/nwindow*i, (23/nwindow)*(i+1)] for i in range(0,nwindow)] # Define intervals to take measurements over
plt.figure()
for i in range(len(sky_times)):
    freqs = np.linspace(50,99,3) # EDGES measures from 50 to 99 MHz and takes 50 measurements
    temps = []
    for j in freqs:
        value = int_sky(freq=j, filter_array=filter_array, location=('-26.69719','116.63903',373), sampling_rate=15, interval=sky_times[i], nside=nside, plot_figs=False)
        temps.append(value)
    plt.plot(freqs,temps,'b-',label='%i_foreground' % sky_times[i][0])
    data = np.array([freqs, temps])
    np.savetxt("%i_foreground_1w_sim_test.txt" % sky_times[i][0], data, delimiter = ",") # save data in the same style as EDGES
plt.legend()
plt.savefig('foreground_1w_sim_test.png')
