

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
       stokes='I',
       field='PER_FIELD_*, J0336+3218',
       phasecenter='J2000 03:36:30.200000 +32.18.28.00000',
       mosweight=True,
       specmode='mfs',
       deconvolver='mtmfs',
       imsize=[5000], 
       cell= '2.5arcsec', 
       weighting='briggs', 
       robust=0.5,
       niter=300, 
       threshold='1e-1', 
       weighting="briggs",
       gridder='awproject',
       savemodel='modelcolumn',        
       parallel=True,
       psterm=True,
       nterms=2,
       rotatepastep=5.0,
       interactive=False,
       mask='../../masks/totat1.mask')


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
gaincal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_calibrated_working.ms/',
        caltable='mpcal1',
        field='J0336+3218, PER_FIELD_*',
        gaintype='G',
        calmode='p',
        solint='int')

rmtables('bpcal1')
bandpass(vis='19B-053.sb37659292.eb37739287.58869.013119236115_calibrated_working.ms/',
        caltable='bpcal1',
        gaintable='pcal2'
        field='J0336+3218, PER_FIELD_*',
        bandtype='B',
        solint='int')

applycal(vis='19B-053.sb37659292.eb37739287.58869.013119236115_calibrated_working.ms/',
         field='J0336+3218, PER_FIELD_*',
         gaintable=['mpcal1'])


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