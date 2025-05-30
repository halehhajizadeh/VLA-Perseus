import sys
sys.path.append('.')
from configs import msfilename

#3C147
# Reference Frequency for fit values
reffreq = '1.5166184156GHz'
# Stokes I flux density
I =  20.863910454772533
# Spectral Index
alpha =    [-0.7492244551950094, -0.1721910611532658 ]
# Polarization Fraction
polfrac =  [1.93699661e-04, -1.96404497e-04,  2.35087229e-04,  5.98043328e-05]
# Polarization Angle
polangle = [-0.01928821,  0.18393654,  0.3659257,  -1.19863784,  0.44004379]

setjy(vis=msfilename,
      field='0542+498=3C147',
      spw='',
      selectdata=False,
      timerange="",
      scan="",
      intent="",
      observation="",
      scalebychan=True,
      standard="manual",
      listmodels=False,
      fluxdensity=[I,0,0,0],
      spix=alpha,
      reffreq=reffreq,
      polindex=polfrac,
      polangle=polangle,
      rotmeas=0,
      fluxdict={},
      useephemdir=False,
      interpolation="nearest",
      usescratch=True,
      ismms=False,
)

#3C138
# Reference Frequency for fit values
reffreq = '1.5166184156GHz'
# Stokes I flux density
I =  8.113235256440722
# Spectral Index
alpha =    [-0.560574282445902, -0.08445806325204205 ]
# Polarization Fraction
polfrac =  [0.07837514,  0.05562951, -0.04116294,  0.00972373]
# Polarization Angle
polangle = [-0.1659093,  0.07806315, -0.28490396,  0.25707148, -0.06585335]


setjy(vis=msfilename,
      field='0521+166=3C138',
      spw='',
      selectdata=False,
      timerange="",
      scan="",
      intent="",
      observation="",
      scalebychan=True,
      standard="manual",
      listmodels=False,
      fluxdensity=[I,0,0,0],
      spix=alpha,
      reffreq=reffreq,
      polindex=polfrac,
      polangle=polangle,
      rotmeas=0,
      fluxdict={},
      useephemdir=False,
      interpolation="nearest",
      usescratch=True,
      ismms=False,
)
