import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

#3C147

# data = np.loadtxt('3C147_2019.dat')
# reffreq = 1.5166184156 #GHz


# def S(f,S,alpha,beta):
#         return S*(f/reffreq)**(alpha+beta*np.log10(f/reffreq))

# # Fit 1 - 5 GHz data points
# popt, pcov = curve_fit(S, data[0:5,0], data[0:5,1])
# print('I@3GHz', popt[0], ' Jy')
# print('alpha', popt[1])
# print('beta', popt[2])
# print( 'Covariance')
# print(pcov)

# plt.plot(data[0:5,0], data[0:5,1], 'ro', label='data')
# plt.plot(np.arange(0.7,5,0.1), S(np.arange(0.7,5,0.1), *popt), 'r-', label='fit')

# plt.title('3C147')
# plt.legend()
# plt.xlabel('Frequency (GHz)')
# plt.ylabel('Flux Density (Jy)')
# plt.show()

# #Polarization Angle
# def PA(f,a,b,c,d,e):
#         return a+b*((f-reffreq)/reffreq)+c*((f-reffreq)/reffreq)**2+d*((f-reffreq)/reffreq)**3+e*((f-reffreq)/reffreq)**4

# # Fit 2 - 9 GHz data points
# popt, pcov = curve_fit(PA, data[0:6,0], data[0:6,3])
# print("Polangle Polynomial: ", popt)
# print("Covariance")
# print(pcov)

# plt.plot(data[0:5,0], data[0:5,3], 'go', label='data')
# plt.plot(np.arange(0.7,9,0.1), PA(np.arange(0.7,9,0.1), *popt), 'r-', label='fit')

# plt.title('3C147')
# plt.legend()
# plt.xlabel('Frequency (GHz)')
# plt.ylabel('Lin. Pol. Angle (rad)')
# plt.show()

# #Polarization Fraction
# def PF(f,a,b,c,d):
#         return a+b*((f-reffreq)/reffreq)+c*((f-reffreq)/reffreq)**2+d*((f-reffreq)/reffreq)**3

# # Fit 1 - 5 GHz data points
# popt, pcov = curve_fit(PF, data[0:6,0], data[0:6,2])
# print("Polfrac Polynomial: ", popt)
# print("Covariance")
# print(pcov)

# plt.plot(data[0:6,0], data[0:6,2], 'bo', label='data')
# plt.plot(np.arange(0.7,5,0.1), PF(np.arange(0.7,5,0.1), *popt), 'r-', label='fit')

# plt.title('3C147')
# plt.legend()
# plt.xlabel('Frequency (GHz)')
# plt.ylabel('Lin. Pol. Fraction')
# plt.show()

#----------------------------------------------------------------------------------
# I@3GHz 20.863910454772533  Jy
# alpha -0.7492244551950094
# beta -0.1721910611532658
# Covariance
# [[ 1.24814069e-03  5.25052348e-05 -4.66427450e-04]
#  [ 5.25052348e-05  1.29605799e-05 -3.33557030e-05]
#  [-4.66427450e-04 -3.33557030e-05  3.39572091e-04]]
# Polangle Polynomial:  [-0.01928821  0.18393654  0.3659257  -1.19863784  0.44004379]
# Covariance
# [[ 1.05489893e-03 -3.77740063e-05 -6.79286212e-03  7.24492685e-03
#   -1.92507312e-03]
#  [-3.77740063e-05  6.03532358e-03 -3.43868885e-03 -2.98404482e-03
#    1.49370858e-03]
#  [-6.79286212e-03 -3.43868885e-03  8.00036788e-02 -8.65709075e-02
#    2.33565258e-02]
#  [ 7.24492685e-03 -2.98404482e-03 -8.65709075e-02  1.03549485e-01
#   -2.91149216e-02]
#  [-1.92507312e-03  1.49370858e-03  2.33565258e-02 -2.91149216e-02
#    8.32611650e-03]]
# Polfrac Polynomial:  [ 1.93699661e-04 -1.96404497e-04  2.35087229e-04  5.98043328e-05]
# Covariance
# [[ 8.36582512e-10  4.21971544e-10 -1.91051975e-09  7.04181611e-10]
#  [ 4.21971544e-10  7.91215056e-09 -1.04659271e-08  3.07190532e-09]
#  [-1.91051975e-09 -1.04659271e-08  1.98699351e-08 -6.71862879e-09]
#  [ 7.04181611e-10  3.07190532e-09 -6.71862879e-09  2.38691276e-09]]
####################################################################################
#3C138

data = np.loadtxt('3C138_2019.dat')
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

plt.title('3C138')
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

plt.title('3C138')
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

plt.title('3C138')
plt.legend()
plt.xlabel('Frequency (GHz)')
plt.ylabel('Lin. Pol. Fraction')
plt.show()

#----------------------------------------------------------------
# I@3GHz 8.113235256440722  Jy
# alpha -0.560574282445902
# beta -0.08445806325204205
# Covariance
# [[ 6.55511179e-05  7.04118079e-06 -3.95782364e-05]
#  [ 7.04118079e-06  5.93489907e-06 -1.41794757e-05]
#  [-3.95782364e-05 -1.41794757e-05  6.23850643e-05]]
# Polangle Polynomial:  [-0.16590935  0.07806315 -0.28490396  0.25707148 -0.06585335]
# Covariance
# [[ 6.48717600e-06 -2.32295207e-07 -4.17731869e-05  4.45531947e-05
#   -1.18383761e-05]
#  [-2.32295207e-07  3.71146571e-05 -2.11464535e-05 -1.83506130e-05
#    9.18567296e-06]
#  [-4.17731869e-05 -2.11464535e-05  4.91988279e-04 -5.32373940e-04
#    1.43632626e-04]
#  [ 4.45531947e-05 -1.83506130e-05 -5.32373940e-04  6.36784949e-04
#   -1.79044304e-04]
#  [-1.18383761e-05  9.18567296e-06  1.43632626e-04 -1.79044304e-04
#    5.12020563e-05]]
# Polfrac Polynomial:  [ 0.07837514  0.05562951 -0.04116294  0.00972373]
# Covariance
# [[ 1.43594913e-06  7.24291424e-07 -3.27930462e-06  1.20868995e-06]
#  [ 7.24291424e-07  1.35807817e-05 -1.79642009e-05  5.27275998e-06]
#  [-3.27930462e-06 -1.79642009e-05  3.41056737e-05 -1.15321643e-05]
#  [ 1.20868995e-06  5.27275998e-06 -1.15321643e-05  4.09700711e-06]]
