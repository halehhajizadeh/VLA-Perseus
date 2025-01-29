msfile = ''



#ALL

gaincal(vis=msfile,
        caltable='pcal1',
        field='PER_FIELD_*',
        gaintype='G',
        calmode='p',
        solint='int')

applycal(vis=msfile,
         field='PER_FIELD_*',
         gaintable=['pcal1'])


gaincal(vis=msfile,
        caltable='pcal2',
        field='PER_FIELD_*',
        gaintype='G',
        calmode='p',
        solint='int')


bandpass(vis=msfile,
        caltable='bpcal1',
        gaintable='pcal2',
        field='PER_FIELD_*',
        bandtype='B',
        solint='int')

applycal(vis=msfile,
         field='PER_FIELD_*',
         gaintable=['pcal2','bpcal1'])


flagdata(vis=msfile, datacolumn='residual', mode='tfcrop')
