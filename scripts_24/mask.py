# scp -r nm-12934@ssh.aoc.nrao.edu:/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/24A-376.sb45258229.eb45299201.60381.83744690972/maskimage2.fits ./Desktop/VLA-Perseus/mask_pybdsf
#scp -r ./Desktop/VLA-Perseus/mask_pybdsf/0972_mask.fits nm-12934@ssh.aoc.nrao.edu:/lustre/aoc/observers/nm-12934/VLA-Perseus/data/new/data/24A-376.sb45258229.eb45299201.60381.83744690972/

inp importfits


imregrid(imagename='mask.image', template='maskimage.model.tt0', output='mask_regrid.image')


makemask(mode='copy', inpimage='maskimage.model.tt0/',
            inpmask='4028_mask_regrid.image',
            output='4028_mask_final.image',
            overwrite=True)
