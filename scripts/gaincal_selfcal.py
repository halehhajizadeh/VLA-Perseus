# Run inside the CASA!!!!!

# There have been reported instances where CASA fails to save the model visibilities when using interactive clean.
# It is crucial that the model is saved correctly, otherwise self-calibration will use the 'default' model of a 1 Jy point source at the phase center.
# The default model may be very different from your target field and we do not want to carry out the selfcal procedure with this incorrect model. 
# Therefore, it is recommended to verify that the model has been saved correctly by inspecting the model visibilities.


plotms(vis=msfilename, xaxis='UVwave', yaxis='amp', ydatacolumn='model', avgchannel='64', avgtime='300')

# in CA11
gaincal(vis='19B-053.sb37659292.eb37728757.58867.005418773144_calibrated_1.ms/',caltable='selfcal_combine_pol_solint_3.tb', field = 'PER_FIELD_*', solint='3s',refant='ea11',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37728757.58867.005418773144_calibrated_1.ms/',caltable='selfcal_combine_pol_solint_6.tb', field = 'PER_FIELD_*', solint='6s',refant='ea11',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37728757.58867.005418773144_calibrated_1.ms/',caltable='selfcal_combine_pol_solint_12.tb', field='PER_FIELD_*', solint='12s',refant='ea11',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37728757.58867.005418773144_calibrated_1.ms/',caltable='selfcal_combine_pol_solint_24.tb', field='PER_FIELD_*', solint='24s',refant='ea11',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37728757.58867.005418773144_calibrated_1.ms/',caltable='selfcal_combine_pol_solint_48.tb', field='PER_FIELD_*', solint='48s',refant='ea11',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37728757.58867.005418773144_calibrated_1.ms/',caltable='selfcal_combine_pol_solint_96.tb', field='PER_FIELD_*', solint='96s',refant='ea11',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37728757.58867.005418773144_calibrated_1.ms/',caltable='selfcal_combine_pol_solint_120.tb', field= 'PER_FIELD_*', solint='120s',refant='ea11',calmode='p',gaintype='T', minsnr=0)
gaincal(vis='19B-053.sb37659292.eb37728757.58867.005418773144_calibrated_1.ms/',caltable='selfcal_combine_pol_solint_180.tb', field= 'PER_FIELD_*', solint='180s',refant='ea11',calmode='p',gaintype='T', minsnr=0)



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

plt.hist( snr_6s, bins=50, normed=True, histtype='step', label='6 seconds' )
plt.hist( snr_12s, bins=50, normed=True, histtype='step', label='12 seconds' )
plt.hist( snr_24s, bins=50, normed=True, histtype='step', label='24 seconds' )
plt.hist( snr_48s, bins=50, normed=True, histtype='step', label='48 seconds' )
plt.hist( snr_96s, bins=50, normed=True, histtype='step', label='96 seconds' )
plt.hist( snr_120s, bins=50, normed=True, histtype='step', label='120 seconds' )
plt.hist( snr_180s, bins=50, normed=True, histtype='step', label='120 seconds' )
plt.legend( loc='upper right' )
plt.xlabel( 'SNR' )

print( 'P(<=6) = {0}  ({1})'.format( stats.percentileofscore( snr_6s, 6 ), '6s' ) )
print( 'P(<=6) = {0}  ({1})'.format( stats.percentileofscore( snr_12s, 6 ), '12s' ) )
print( 'P(<=6) = {0}  ({1})'.format( stats.percentileofscore( snr_24s, 6 ), '24s' ) )
print( 'P(<=6) = {0}  ({1})'.format( stats.percentileofscore( snr_48s, 6 ), '48s' ) )
print( 'P(<=6) = {0}  ({1})'.format( stats.percentileofscore( snr_96s, 6 ), '96s' ) )
print( 'P(<=6) = {0}  ({1})'.format( stats.percentileofscore( snr_120s, 6 ), '120s' ) )
