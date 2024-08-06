
if threedigits=='546':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='0:0~8;19~32'
    )

#----------------------------------------------------------------
elif threedigits=='775':
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='1,7,9,11,12,13,14'
    )

