import sys
sys.path.append('.')
import matplotlib.pyplot as plt
import numpy as np
import os

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

f='./phasecenter/phasecenter_results.txt'
l=open(f)
data=l.readlines()

ID=[]
ra_raw=[]
dec_raw=[]

for d in data:
    dat_split=d.split()
    ID.append(dat_split[0])
    ra_raw.append(dat_split[1])
    dec_raw.append(dat_split[2].split('\n')[0])
print(ID)
print(ra_raw)
print(dec_raw)
ra_deg=[]
for r in ra_raw:
    ra_split=r.split(':')
    ra_h=ra_split[0]
    ra_m=ra_split[1]
    ra_s=ra_split[2]
    if float(ra_h) > 0:
        ra=(float(ra_h)+float(ra_m)/60+float(ra_s)/3600)*15
    else:
        ra=(float(ra_h)-float(ra_m)/60-float(ra_s)/3600)*15
    ra_deg.append(ra)
    
dec_deg=[]
for c in dec_raw:
    dec_split=c.split('.', 2)
    dec_d=dec_split[0]
    dec_m=dec_split[1]
    dec_s=dec_split[2]
    if float(dec_d) > 0:
        dec=float(dec_d)+float(dec_m)/60+float(dec_s)/3600
    else:
        dec=float(dec_d)-float(dec_m)/60-float(dec_s)/3600
    dec_deg.append(dec)


plt.rc('text',usetex=True)
plt.rc('font',family='serif')

plt.figure(1)

plt.subplot(111)

plt.plot(ra_deg, dec_deg, 'b.')
plt.xlabel(r'RA (deg)',fontsize=15)
plt.ylabel(r'DEC (deg)',fontsize=15)
# plt.xlim(265.5,262.5)
plt.tick_params(axis='x',labelsize=14)
plt.tick_params(axis='y',labelsize=14)

for i, txt in enumerate(ID):
    plt.annotate(txt, (ra_deg[i], dec_deg[i]))

plt.savefig('./phasecenter/Allmosaic.png')
