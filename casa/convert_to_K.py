#Script to convert brightness units -- in spectral_cube (python)


from astropy import units as u
from astropy.io import fits
from spectral_cube import SpectralCube
import numpy as np


def jy_to_K(input_file, bmaj, bmin, input_dir = ''):

    # No file extenstion needed
    if '.fits' in input_file:
        print 'Please remove extension .fits from '+input_file
        break

    input_file = input_dir+input_file+'.fits'
    output_file = input_dir+input_file+'.K.fits'

    header = fits.getheader(input_file)

    bmaj = bmaj*u.arcsec
    bmin = bmin*u.arcsec

    cube = SpectralCube.read(input_file, format = 'fits', unit = (u.Jy / u.beam), beam_threshold= 0.05)
    cube = cube.with_spectral_unit(u.GHz)

    fwhm_to_sigma = 1. /(8. * np.log(2) )**0.5
    beam_area = 2. * np.pi * ( bmaj * bmin * fwhm_to_sigma**2)

    equiv = u.brightness_temperature(beam_area, restfreq)
    cube.allow_huge_operations = True
    cubeK = cube.to(u.K, equiv)

    cubeK.write(output_file)

def K_to_jy(input_file, bmaj, bmin, input_dir = ''):

    # No file extenstion needed
    if '.fits' in input_file:
        print 'Please remove extension .fits from '+input_file
        break

    input_file = input_dir+input_file+'.fits'
    output_file = input_dir+input_file+'.Jy.fits'

    header = fits.getheader(input_file)

    bmaj = bmaj*u.arcsec
    bmin = bmin*u.arcsec

    cube = SpectralCube.read(input_file, format = 'fits', unit = (u.K / u.beam), beam_threshold= 0.05)
    cube = cube.with_spectral_unit(u.GHz)

    fwhm_to_sigma = 1. /(8. * np.log(2) )**0.5
    beam_area = 2. * np.pi * ( bmaj * bmin * fwhm_to_sigma**2)

    equiv = u.brightness_temperature(beam_area, restfreq)
    cube.allow_huge_operations = True
    cubeK = cube.to(u.Jy, equiv)

    cubeK.write(output_file)
