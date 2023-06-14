#Script to convert WCS -- in Casa

import os

def j2000_to_gal(input_file, input_dir = '', remove_image = True, remove_image_gal = True):

    # No file extenstion needed
    if '.fits' in input_file:
        print 'Please remove extension .fits from '+input_file
        break

    input_file = input_dir+input_file+'.fits'
    input_image = input_dir+input_file+'.image'
    output_image = input_dir+input_file+'.gal.image'
    output_file = input_dir+input_file+'.gal.fits'

    importfits(fitsimage = input_file,
               imagename = input_image,
               zeroblanks = False,
               overwrite = True)

    imregrid(imagename = input_file,
             template = 'GALACTIC',
             output =  output_image,
             interpolation = 'cubic',
             overwrite = True)

    exportfits(imagename = output_image,
               fitsimage = output_file,
               dropstokes = True,
               overwrite = True,
               velocity = True)

    if remove_image:
        os.system('rm -rf '+input_image)
    if remove_image_gal:
        os.system('rm -rf '+output_image)


def gal_to_j2000(input_file, input_dir = '', remove_image = True, remove_image_gal = True):

    # No file extenstion needed
    if '.fits' in input_file:
        print 'Please remove extension .fits from '+input_file
        break

    input_file = input_dir+input_file+'.fits'
    input_image = input_dir+input_file+'.image'
    output_image = input_dir+input_file+'.j2000.image'
    output_file = input_dir+input_file+'.j2000.fits'

    importfits(fitsimage = input_file,
               imagename = input_image,
               zeroblanks = False,
               overwrite = True)

    imregrid(imagename = input_file,
             template = 'J2000',
             output =  output_image,
             interpolation = 'cubic',
             overwrite = True)

    exportfits(imagename = output_image,
               fitsimage = output_file,
               dropstokes = True,
               overwrite = True,
               velocity = True)

    if remove_image:
        os.system('rm -rf '+input_image)
    if remove_image_gal:
        os.system('rm -rf '+output_image)
