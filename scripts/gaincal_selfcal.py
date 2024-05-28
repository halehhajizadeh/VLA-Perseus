# Run inside the CASA!!!!!

# There have been reported instances where CASA fails to save the model visibilities when using interactive clean.
# It is crucial that the model is saved correctly, otherwise self-calibration will use the 'default' model of a 1 Jy point source at the phase center.
# The default model may be very different from your target field and we do not want to carry out the selfcal procedure with this incorrect model. 
# Therefore, it is recommended to verify that the model has been saved correctly by inspecting the model visibilities.


plotms(vis=msfilename, xaxis='UVwave', yaxis='amp', ydatacolumn='model', avgchannel='64', avgtime='300')

# in CA11
gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',caltable='selfcal_combine_pol_solint_3.tb', field = 'PER_FIELD_*', solint='3s',refant='ea16',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',caltable='selfcal_combine_pol_solint_6.tb', field = 'PER_FIELD_*', solint='6s',refant='ea16',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',caltable='selfcal_combine_pol_solint_12.tb', field='PER_FIELD_*', solint='12s',refant='ea16',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',caltable='selfcal_combine_pol_solint_24.tb', field='PER_FIELD_*', solint='24s',refant='ea16',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',caltable='selfcal_combine_pol_solint_48.tb', field='PER_FIELD_*', solint='48s',refant='ea16',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',caltable='selfcal_combine_pol_solint_96.tb', field='PER_FIELD_*', solint='96s',refant='ea16',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',caltable='selfcal_combine_pol_solint_120.tb', field= 'PER_FIELD_*', solint='120s',refant='ea16',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',caltable='selfcal_combine_pol_solint_180.tb', field= 'PER_FIELD_*', solint='180s',refant='ea16',calmode='p',gaintype='T', minsnr=0)



plotms(vis='selfcal_combine_pol_solint_3.tb',yaxis='phase',iteraxis='antenna',gridrows=2, gridcols=2, coloraxis='spw')
plotms(vis='selfcal_combine_pol_solint_6.tb',yaxis='phase',iteraxis='antenna',gridrows=2, gridcols=2, coloraxis='spw')
plotms(vis='selfcal_combine_pol_solint_12.tb',yaxis='phase',iteraxis='antenna',gridrows=2, gridcols=2, coloraxis='spw')
plotms(vis='selfcal_combine_pol_solint_24.tb',yaxis='phase',iteraxis='antenna',gridrows=2, gridcols=2, coloraxis='spw')
plotms(vis='selfcal_combine_pol_solint_48.tb',yaxis='phase',iteraxis='antenna',gridrows=2, gridcols=2, coloraxis='spw')
plotms(vis='selfcal_combine_pol_solint_96.tb',yaxis='phase',iteraxis='antenna',gridrows=2, gridcols=2, coloraxis='spw')
plotms(vis='selfcal_combine_pol_solint_120.tb',yaxis='phase',iteraxis='antenna',gridrows=2, gridcols=2, coloraxis='spw')



import matplotlib.pyplot as plt
from scipy import stats


tb.open( 'selfcal_combine_pol_solint_6.tb' )
snr_6s = tb.getcol( 'SNR' ).ravel()
tb.close()

tb.open( 'selfcal_combine_pol_solint_12.tb' )
snr_12s = tb.getcol( 'SNR' ).ravel()
tb.close()

tb.open( 'selfcal_combine_pol_solint_24.tb' )
snr_24s = tb.getcol( 'SNR' ).ravel()
tb.close()

tb.open( 'selfcal_combine_pol_solint_48.tb' )
snr_48s = tb.getcol( 'SNR' ).ravel()
tb.close()


tb.open( 'selfcal_combine_pol_solint_96.tb' )
snr_96s = tb.getcol( 'SNR' ).ravel()
tb.close()

tb.open( 'selfcal_combine_pol_solint_120.tb' )
snr_120s = tb.getcol( 'SNR' ).ravel()
tb.close()

tb.open( 'selfcal_combine_pol_solint_180.tb' )
snr_180s = tb.getcol( 'SNR' ).ravel()
tb.close()

plt.hist( snr_6s, bins=50, density=True, histtype='step', label='6 seconds' )
plt.hist( snr_12s, bins=50, density=True, histtype='step', label='12 seconds' )
plt.hist( snr_24s, bins=50, density=True, histtype='step', label='24 seconds' )
plt.hist( snr_48s, bins=50, density=True, histtype='step', label='48 seconds' )
plt.hist( snr_96s, bins=50, density=True, histtype='step', label='96 seconds' )
plt.hist( snr_120s, bins=50, density=True, histtype='step', label='120 seconds' )
plt.hist( snr_180s, bins=50, density=True, histtype='step', label='120 seconds' )
plt.legend( loc='upper right' )
plt.xlabel( 'SNR' )

print( 'P(<=6) = {0}  ({1})'.format( stats.percentileofscore( snr_6s, 6 ), '6s' ) )
print( 'P(<=6) = {0}  ({1})'.format( stats.percentileofscore( snr_12s, 6 ), '12s' ) )
print( 'P(<=6) = {0}  ({1})'.format( stats.percentileofscore( snr_24s, 6 ), '24s' ) )
print( 'P(<=6) = {0}  ({1})'.format( stats.percentileofscore( snr_48s, 6 ), '48s' ) )
print( 'P(<=6) = {0}  ({1})'.format( stats.percentileofscore( snr_96s, 6 ), '96s' ) )
print( 'P(<=6) = {0}  ({1})'.format( stats.percentileofscore( snr_120s, 6 ), '120s' ) )

gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/', field='PER_FIELD_*', caltable='phase_120.cal',solint='120s',refant='ea16',calmode='p',gaintype='G')
applycal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/', field='PER_FIELD_*', gaintable=['phase_120.cal'], interp='linear')

split(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/', field='PER_FIELD_*', datacolumn='corrected', outputvis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged_selfcaled1.ms/')


plotms(vis='selfcal_combine_pol_solint_48_6.tb',
       xaxis='time',
       yaxis='phase',
       gridrows=3,
       gridcols=3,
       iteraxis='antenna',
       plotrange=[0,0,-30,30],
       coloraxis='corr',
       titlefont=7,
       xaxisfont=7,
       yaxisfont=7,
       showgui = True)


tclean(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',
       imagename='initial',
       field='PER_FIELD_*',
       phasecenter='J2000 03:36:30.200000 +32.18.28.00000',
       mosweight=True,
       specmode='mfs',
       deconvolver='hogbom',
       imsize=[5000], 
       cell= '2.5arcsec', 
       weighting='briggs', 
       robust=0.5,
       niter=200, 
       threshold='1e-1', 
       interactive=True,
       gridder='awproject',
       savemodel='modelcolumn',
       usepointing=False,
       rotatepastep=5.0)


tclean(vis='test.ms',
       imagename='single_field_initial',
       mosweight=True,
       specmode='mfs',
       deconvolver='hogbom',
       imsize=[1296], 
       cell= '2.5arcsec', 
       weighting='briggs', 
       robust=0.5,
       niter=400, 
       threshold='5e-4', 
       interactive=True,
       gridder='awproject',
       savemodel='modelcolumn',
       usepointing=False,
       rotatepastep=5.0)


tclean(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',
       imagename='single_field_initial',
       mosweight=True,
       specmode='mfs',
       deconvolver='hogbom',
       imsize=[1296], 
       cell= '2.5arcsec', 
       weighting='briggs', 
       robust=0.5,
       niter=400, 
       threshold='5e-4', 
       interactive=True,
       gridder='awproject',
       savemodel='modelcolumn',
       usepointing=False,
       rotatepastep=5.0)

rmtables('pcal1')
gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',
        caltable='pcal1',
        field='PER_FIELD_*, J0336+3218',
        gaintype='G',
        refant='ea16',
        calmode='p',
        solint='inf',
        minsnr=3.0,
        minblperant=6)

applycal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',
         field='PER_FIELD_*,  J0336+3218',
         gaintable=['pcal1'],
         gainfield='',
         calwt=False,
         flagbackup=False)

flagmanager(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',mode='save',versionname='after_pcal1')


rmtables('pcal2')
gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',
        field='PER_FIELD_*,  J0336+3218',
        caltable='pcal2',
        gaintype='G',
        refant='ea16',
        calmode='p',
        solint='96s', 
        minsnr=3.0,
        minblperant=6)

applycal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',
         field='PER_FIELD_*,  J0336+3218',
         gaintable=['pcal2'],
         gainfield='',
         calwt=False,
         flagbackup=False)

flagmanager(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',mode='save',versionname='after_pcal2')


gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',
        field='PER_FIELD_*, J0336+3218',
        caltable='pcal3',
        gaintype='G',
        refant='ea16',
        calmode='p',
        solint='48s',
        minsnr=3.0,
        minblperant=6)

plotms(vis='pcal3',
            xaxis='time',
            yaxis='phase',
            iteraxis='antenna',
            plotrange=[0,0,-80,80],
            gridrows=3,
            gridcols=3)

applycal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',
         field='PER_FIELD_*, J0336+3218', 
         gaintable=['pcal3'],
         gainfield='',
         calwt=False,
         flagbackup=False,)

flagmanager(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',mode='save',versionname='after_pcal3')


gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',
        field='PER_FIELD_*, J0336+3218',
        caltable='pcal4',
        gaintype='G',
        refant='ea16',
        calmode='p',
        solint='12s',
        minsnr=3.0,
        minblperant=6)

plotms(vis='pcal4',
            xaxis='time',
            yaxis='phase',
            iteraxis='antenna',
            plotrange=[0,0,-180,180],
            gridrows=3,
            gridcols=3,
            coloraxis='spw')


applycal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',
         field='PER_FIELD_*, J0336+3218',
         gaintable=['pcal4'],
         gainfield='',
         calwt=False,
         flagbackup=False)

flagmanager(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',mode='save',versionname='after_pcal4')


gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',
        field='PER_FIELD_*, J0336+3218',
        caltable='apcal',
        gaintype='G',
        refant='ea16',
        calmode='ap',
        solint='inf',
        minsnr=3.0,
        minblperant=6,
#        uvrange='>50m', # may need to use to exclude extended emission
        gaintable='pcal4',
        solnorm=True)


applycal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',
         field='PER_FIELD_*, J0336+3218',
         gaintable=['pcal4','apcal'],
         gainfield='',
         calwt=False,
         flagbackup=False)

flagmanager(vis='19B-053.sb37659292.eb37739287.58869.013119236115_flagged.ms/',mode='save',versionname='after_pcal5')