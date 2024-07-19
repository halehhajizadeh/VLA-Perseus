#970
msfile = '19B-053.sb37659292.eb37739287.58869.013119236115_calibrated.ms/'
#208
msfile = '19B-053.sb37659292.eb37728757.58867.005418773144_calibrated.ms/'
#263
msfile = '19B-053.sb37659292.eb37692509.58859.886421828705_calibrated.ms/'

# FIELD
gaincal(vis=msfile,
        caltable='f-pcal1',
        field='J0336+3218',
        gaintype='G',
        calmode='p',
        solint='int')

applycal(vis=msfile,
         field='J0336+3218',
         gaintable=['f-pcal1'])


gaincal(vis=msfile,
        caltable='f-pcal2',
        field='J0336+3218',
        gaintype='G',
        calmode='p',
        solint='int')

bandpass(vis=msfile,
        caltable='f-bpcal1',
        gaintable='f-pcal2',
        field='J0336+3218',
        bandtype='B',
        solint='int')

applycal(vis=msfile,
         field='J0336+3218',
         gaintable=['f-pcal2','f-bpcal1'])


flagdata(vis=msfile, datacolumn='residual', mode='tfcrop')

#ALL

gaincal(vis=msfile,
        caltable='pcal1',
        field='J0336+3218, PER_FIELD_*',
        gaintype='G',
        calmode='p',
        solint='int')

applycal(vis=msfile,
         field='J0336+3218, PER_FIELD_*',
         gaintable=['pcal1'])


gaincal(vis=msfile,
        caltable='pcal2',
        field='J0336+3218, PER_FIELD_*',
        gaintype='G',
        calmode='p',
        solint='int')


bandpass(vis=msfile,
        caltable='bpcal1',
        gaintable='pcal2',
        field='J0336+3218, PER_FIELD_*',
        bandtype='B',
        solint='int')

applycal(vis=msfile,
         field='J0336+3218, PER_FIELD_*',
         gaintable=['pcal2','bpcal1'])


flagdata(vis=msfile, datacolumn='residual', mode='tfcrop')
