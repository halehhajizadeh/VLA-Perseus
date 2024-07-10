import os
import glob

spw = [
    2,
    3, 
    4, 
    5, 
    6, 
    8, 
    15, 
    16, 
    17
]

base_directory = '../data/concat/total/' 

specific_dirs = [
    '03:23:30.000001_+31.30.00.00000/tclean/',  
    '03:32:04.530001_+31.05.04.00000/tclean/',  
    '03:36:00.000000_+30.30.00.00001/tclean/',  
    '03:25:30.000000_+29.29.59.99999/tclean/',
    # '03:34:30.000000_+31.59.59.99999/tclean/'
]

for i in spw: 
    images_list = []
    pb_list = []

    # Iterate through each specific directory
    for dir_path in specific_dirs:
        # Construct the full path
        full_path = os.path.join(base_directory, dir_path)
        
        # Ensure the directory exists
        if os.path.isdir(full_path):
            # Find all files matching the pattern
            pattern_image = os.path.join(full_path, f'spw{i}*.image.tt0')
            pattern_pb = os.path.join(full_path, f'spw{i}*.pb.tt0')
            images_list.extend(glob.glob(pattern_image))
            pb_list.extend(glob.glob(pattern_pb))
    
    # Print or process the found files
    for file in images_list:
        print(file)

    for file in pb_list:
        print(file)
    
    # Check if we have images to process
    if images_list:
        im.linearmosaic(imagename=images_list,
                        mosaic=os.path.join(base_directory, 'bigmosaic', f'mosaic_spw{i}'),
                        interp='linear')

        # If you have primary beam correction (PB) images, you can apply them separately if needed
        # This may require an additional step outside of linearmosaic, depending on your processing needs.
