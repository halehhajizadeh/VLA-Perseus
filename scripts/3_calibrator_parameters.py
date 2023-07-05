import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

data = np.loadtxt('3C147_2019.dat')
reffreq = 1.5166184156 #GHz


def S(f,S,alpha,beta):
        return S*(f/reffreq)**(alpha+beta*np.log10(f/reffreq))

# Fit 1 - 5 GHz data points
popt, pcov = curve_fit(S, data[0:6,0], data[0:6,1])
print('I@3GHz', popt[0], ' Jy')
print('alpha', popt[1])
print('beta', popt[2])
print( 'Covariance')
print(pcov)

plt.plot(data[0:6,0], data[0:6,1], 'ro', label='data')
plt.plot(np.arange(0.7,5,0.1), S(np.arange(0.7,5,0.1), *popt), 'r-', label='fit')

plt.title('3C147')
plt.legend()
plt.xlabel('Frequency (GHz)')
plt.ylabel('Flux Density (Jy)')
plt.show()

#Polarization Angle
def PA(f,a,b,c,d,e):
        return a+b*((f-reffreq)/reffreq)+c*((f-reffreq)/reffreq)**2+d*((f-reffreq)/reffreq)**3+e*((f-reffreq)/reffreq)**4

# Fit 2 - 9 GHz data points
popt, pcov = curve_fit(PA, data[0:6,0], data[0:6,3])
print("Polangle Polynomial: ", popt)
print("Covariance")
print(pcov)

plt.plot(data[0:6,0], data[0:6,3], 'go', label='data')
plt.plot(np.arange(0.7,9,0.1), PA(np.arange(0.7,9,0.1), *popt), 'r-', label='fit')

plt.title('3C147')
plt.legend()
plt.xlabel('Frequency (GHz)')
plt.ylabel('Lin. Pol. Angle (rad)')
plt.show()

#Polarization Fraction
def PF(f,a,b,c,d):
        return a+b*((f-reffreq)/reffreq)+c*((f-reffreq)/reffreq)**2+d*((f-reffreq)/reffreq)**3

# Fit 1 - 5 GHz data points
popt, pcov = curve_fit(PF, data[0:6,0], data[0:6,2])
print("Polfrac Polynomial: ", popt)
print("Covariance")
print(pcov)

plt.plot(data[0:6,0], data[0:6,2], 'bo', label='data')
plt.plot(np.arange(0.7,5,0.1), PF(np.arange(0.7,5,0.1), *popt), 'r-', label='fit')

plt.title('3C147')
plt.legend()
plt.xlabel('Frequency (GHz)')
plt.ylabel('Lin. Pol. Fraction')
plt.show()