import healpy as hp
import numpy as np
import matplotlib.pyplot as plt

nside = 32
npix = hp.nside2npix(nside)
thetalim = 5*np.pi/8

n = np.zeros(npix)
m = np.ones(npix)

thetas = np.linspace(thetalim, np.pi, npix)
phis = np.linspace(0, 2*np.pi, npix)

func = 1-(((thetas-np.pi)/(thetalim-np.pi))**2)

for j in phis:
    pixels = hp.ang2pix(nside, thetas, j)
    n[pixels] = func[pixels]

plt.plot(n)
plt.plot(func)
plt.plot(thetas)
plt.savefig("plot.png")

hp.orthview(n, title="test",half_sky=True)
plt.savefig("filter_orthview.png")

hp.mollview(n, title="test")
plt.savefig("filter_mollview.png")

