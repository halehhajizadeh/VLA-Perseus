cl.addcomponent(flux=1.55, fluxunit='Jy', shape='point', dir='J2000 03:36:30.107600 +32.18.29.34239')
cl.rename('component.cl')
cl.close()
ft(vis='19B-053.sb37659292.eb37664379.58853.92688378472_calibrated.ms/', complist='co')


##########################################################################################

# Example of creating a mask based on a threshold
ia.open('your_image.image')
# Set the threshold; pixels above this value will be included in the mask
thresh = 0.005 # Jy/beam, adjust this value based on your needs
# Create the mask where the image is greater than the threshold
ia.calcmask(mask='"your_image.image" > ' + str(thresh), name='mask0')
ia.close()