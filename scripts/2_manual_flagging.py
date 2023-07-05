filename = '../data/19B-053_2019_12_15_T07_36_56.546/products/19B-053.sb37264871.eb37595549.58832.22860825231_calibrated.ms'

flagdata(
vis=filename, 
mode='manual',
spw='0:19~32'
)

flagdata( 
vis=filename, 
mode='manual', 
spw='3:0~5'
)

flagdata( 
vis=filename, 
mode='manual', 
spw='0:0~8'
)

flagdata( 
vis=filename, 
mode='manual', 
spw='9,11,12,7'
)

flagdata( 
vis=filename, 
mode='manual', 
spw='15:12~15'
)