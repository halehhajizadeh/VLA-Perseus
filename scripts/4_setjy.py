# Reference Frequency for fit values
reffreq = '1.5166184156GHz'
# Stokes I flux density
I =  20.853182595457284
# Spectral Index
alpha =    [-0.7484788628127326, -0.158094395936077]
# Polarization Fraction
polfrac =  [ 2.11100814e-04, -1.90109284e-04,  3.28307299e-05,  2.04595669e-04]
# Polarization Angle
polangle = [-0.01928821,  0.18393654,  0.3659257,  -1.19863784,  0.44004379]

filename = '../data/19B-053_2019_12_15_T07_36_56.546/products/19B-053.sb37264871.eb37595549.58832.22860825231_calibrated.ms'


setjy(vis=filename,
      field='0',
      scan = '2,3',
      spw='',
      selectdata=False, 
      scalebychan=True, 
      standard='Perley-Butler 2017',
      model='3C147_L.im', 
      listmodels=False, 
      fluxdensity=-1, 
      usescratch=True)



setjy(vis=filename,
      field='1',
      spw='',
      selectdata=False, 
      scalebychan=True, 
      standard='Perley-Butler 2017',
      model='3C138_L.im', 
      listmodels=False, 
      fluxdensity=-1, 
      usescratch=True)
