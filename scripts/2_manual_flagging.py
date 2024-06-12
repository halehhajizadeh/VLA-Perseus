import sys
sys.path.append('.')
from configs import msfilename, threedigits

if threedigits=='546':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='0:0~8;19~32'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    spw='3:0~5'
    )


    flagdata( 
    vis=msfilename, 
    mode='manual', 
    spw='7,9,11,12'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    field = '0',
    spw='15:7~8;12~27'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    field = '0',
    spw='17:14~15;33~35'
    )
#----------------------------------------------------------------
elif threedigits=='775':
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='1,7,9,11,12,13,14'
    )

#----------------------------------------------------------------  
elif threedigits=='933':
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )

#----------------------------------------------------------------
elif threedigits=='627':
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )

#----------------------------------------------------------------

elif threedigits=='198':
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,14'
    )
    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='35,36'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    field='0521+166=3C138',
    channel='11,14,20~30;36~42,'
    )
 #-------------------------------------------------------------------
elif threedigits=='861':
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )   

 #-------------------------------------------------------------------
elif threedigits=='076':
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12,14'
    )  

 #-------------------------------------------------------------------
elif threedigits=='228':
    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='48'
    )
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )  
    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='8'
    )

 #-------------------------------------------------------------------
elif threedigits=='672':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12,13'
    )  
    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='27,30'
    )  
 #-------------------------------------------------------------------
elif threedigits=='59-933':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )  

 #-------------------------------------------------------------------
elif threedigits=='684':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12,13'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='14, 15'
    )  

#-------------------------------------------------------------------
elif threedigits=='543':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='0, 7, 9, 10, 11, 12, 13, 14'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='5,46,47'
    )

 #-------------------------------------------------------------------
elif threedigits=='447':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,13'
    )
    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='22,27,28,29,30,37'
    )

#-------------------------------------------------------------------
elif threedigits=='362':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )

#-------------------------------------------------------------------
elif threedigits=='102':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='2:7~9;25;59;60,3:6~10;19;20;26,5:14~18;41;51;52,6:49~51',
    )

#-------------------------------------------------------------------
elif threedigits=='263':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7'
    )
  
#-------------------------------------------------------------------
elif threedigits=='208':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='0,1,7,9,10,11,12,13,14'
    )



    flagdata(
    vis=msfilename,
    mode='manual',
    timerange='01:30:42.500~01:30:52.500'
    )

#-------------------------------------------------------------------
elif threedigits=='970':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='0,1,2,7,8,9,10,11,12,13,14'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='3:0~10'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    field='PER_FIELD_39',
    spw='4:14~17, 5:14~17'
    )


#-------------------------------------------------------------------
elif threedigits=='587':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='0,1,7,9,10,11,12,13,14'
    )

    flagdata(
    vis=msfilename, 
    field='PER_FIELD_*',
    mode='manual',
    scan='9'
    )


#-------------------------------------------------------------------
elif threedigits=='482':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12,13,14'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='15:3;4;7;12;14;16;21;42;56;44;25;46;36;28;40;60;59'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='15:5;6;9;10;22;24;45;47;55;57'
    )


#-------------------------------------------------------------------
elif threedigits=='930':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='8:14;20;22;38;39;42;46'
    )


#-------------------------------------------------------------------
elif threedigits=='42.458':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='8:28;36;53;45;52;58;60;53;25;55;27;54'
    )


#-------------------------------------------------------------------
elif threedigits=='838':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='2:10;23;24;27;28;29;53,8:9;14;53,17:23;35;36;37;45,15:41;51;53,6:44;46;48'
    )   
     
#-------------------------------------------------------------------
elif threedigits=='242':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12,13,14'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='2:56~60'
    )  

#-------------------------------------------------------------------
elif threedigits=='458':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='8:16;30;34;42;23;53;54;56;37;60;54'
    )

#-------------------------------------------------------------------
elif threedigits=='458':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='1,7,9,10,11,12,13,14'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='8:16;30;34;42;23;53;54;56;37;60;54'
    )    

#-------------------------------------------------------------------
elif threedigits=='294':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12,13'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='55'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='8:33;32;34;35;38;40;45;50;27;28;22;21;11;49;53;47;16;24;36;37;48;46;17;57,2:25;11'
    )      
#-------------------------------------------------------------------
elif threedigits=='045':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='0,7,9,10,11,12,13'
    ) 

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='15:11;47;48;38;21;41;42;15;22;13;35;36;25;13;35;36;25;13;39;40;51;12;21;25,2:58;43;53;54;41;33;17;21,8:31'
    )     

#-------------------------------------------------------------------
elif threedigits=='010':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12,13,14'
    ) 

    flagdata(
    vis=msfilename,
    mode='manual',
    timerange='22:41:41.500~22:41:41.500'
    )

    flagdata(
    vis=msfilename,
    mode='manual',
    timerange='22:41:52.500~22:41:57.500'
    )
