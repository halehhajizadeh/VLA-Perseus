msfile = ''

#ALL

gaincal(vis=msfile,
        caltable='pcal1',
        field='PER_FIELD_*',
        gaintype='G',
        refant='ea25',
        calmode='p',
        solint='2min')

applycal(vis=msfile,
         interp='linear',
         field='PER_FIELD_*',
         gaintable=['pcal1'])


plotms(vis='pcal1',
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

flagdata(mode='tfcrop',datacolumn='CPARAM',vis='pcal1')


gaincal(vis=msfile,
        caltable='pcal2',
        field='PER_FIELD_*',
        gaintype='G',
        refant='ea25',
        calmode='p',
        solint='30s')


applycal(vis=msfile,
         interp='linear',
         field='PER_FIELD_*',
         gaintable=['pcal2'])


gaincal(vis=msfile,
        caltable='pcal3',
        field='PER_FIELD_*',
        gaintype='G',
        refant='ea25',
        calmode='p',
        solint='int')



flagdata(vis=msfile, datacolumn='residual', mode='tfcrop')


gaincal(vis=msfile,
        caltable='ampcal1',
        field='PER_FIELD_*',
        solint='inf',
        calmode='ap',
        refant='ea25',
        gaintype='G',
        gaintable=['pcal3'],
        solnorm=True)


applycal(vis=msfile,
         field='PER_FIELD_*',
         gaintable=['pcal3','ampcal1'],
         interp='linear')


