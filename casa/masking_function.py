import numpy as np
from scipy import ndimage

def make_mask(imagename, thresh, fl=False, useimage=False, pixelmin=0, major=0,
              minor=0, pixelsize=0, line=False, overwrite_old=True,
              closing_diameter=6, pbimage=None, myresidual=None, myimage=None,
              extension='.fullmask'):
    """
    Makes a mask on any image you want it to.

    Parameters
    ----------
    imagename : {casa image without file extention}
        Name of image you want to mask, without the file extention.
    thresh : {float}
        Masking thershold in whatever units are using
    fl : {bool}
        If you want to combine the mask with a previous iteration of clean
        (True), if not (i.e. you are using the dirty image) then False.
    useimage : {bool}
        If you want to use the dirty image or the residual for the masking
        (I usually use the residual - so set to False)
    pixelmin : {float}
        Min number of pixels within a masked region to be taken into the final
        mask, i.e. if your beam size is 1arcsec and pixel size is 0.2 arcsec,
        then three beams would be pixelmin = 75
    major : {float}
        beam major axis, in arsec
    minor : {float}
        beam minor axis, in arsec
    pixelsize : {float}
        length of one side of pixel, in arcsec
    line : {bool}
        if the image is a line or continuum

    Returns
    -------
    mask : {ndarray}
        The final mask (hopefully) as the ".fullmask" image
    """

    mymask = imagename + '.mask'
    if myimage is None:
        myimage = imagename + '.image'
    maskim_nopb = imagename + '{}.nopb'.format(extension)
    maskim = imagename + extension
    threshmask = imagename + '.threshmask'
    if myresidual is None:
        myresidual = imagename + '.residual'
    if pbimage is None:
        pbimage = imagename + '.pb'

    if overwrite_old:
        os.system('rm -rf ' + maskim)
        os.system('rm -rf ' + maskim_nopb)
        os.system('rm -rf ' + threshmask)

    if useimage:
        print 'Using Image'
        immath(imagename=[myimage], outfile=threshmask,
            expr='iif(IM0 > ' + str(thresh) + ',1.0,0.0)')
    else:
        immath(imagename=[myresidual], outfile=threshmask,
            expr='iif(IM0 > ' + str(thresh) + ',1.0,0.0)')

    if fl:
        print 'Combining with previous mask..'
        immath(outfile=maskim_nopb, expr='iif(("' + threshmask + '" + "'
            + mymask + '") > 0.1,1.0,0.0)')
    else:
        print 'Making fresh new mask from image/residual'
        os.system('cp -r ' + threshmask + ' ' + maskim_nopb)

    immath(imagename=[pbimage, maskim_nopb], outfile=maskim,
        expr='iif(IM0 > 0.0, IM1, 0.0)')

    print "Using pixelmin=", pixelmin
    beamarea = (major * minor * np.pi / (4. * np.log(2.))) / (pixelsize**2)
    print 'Beam area', beamarea

    ia.open(maskim)
    mask = ia.getchunk()
    diam = closing_diameter  # Change for large beam dilation
    structure = np.ones((diam, diam))
    dist = ((np.indices((diam, diam)) - (diam - 1) / 2.)**2).sum(axis=0)**0.5
    # circularize the closing element
    structure[dist > diam / 2.] = 0

    if line:
        for k in range(mask.shape[3]):
            mask_temp = mask[:, :, 0, k]
            mask_temp = ndimage.binary_closing(mask_temp, structure=structure)
            labeled, j = ndimage.label(mask_temp)
            myhistogram = ndimage.measurements.histogram(labeled, 0, j + 1,
                                                         j + 1)
            object_slices = ndimage.find_objects(labeled)
            threshold = pixelmin

            for i in range(j):
                if myhistogram[i + 1] < threshold:
                    mask_temp[object_slices[i]] = 0.0

            mask[:, :, 0, k] = mask_temp
    else:
        structure = np.ones((6, 6))  # Change for large beam dilation
        mask = ndimage.binary_closing(mask, structure=structure)
        labeled, j = ndimage.label(mask)
        myhistogram = ndimage.measurements.histogram(labeled, 0, j + 1, j + 1)
        object_slices = ndimage.find_objects(labeled)
        threshold = pixelmin

        for i in range(j):
            if myhistogram[i + 1] < threshold:
                mask[object_slices[i]] = 0.0

    ia.putchunk(mask)
    ia.done()

    print 'Mask created.'

def make_mask_3d(imagename, thresh, fl=False, useimage=False, pixelmin=0,
                 major=0, minor=0, pixelsize=0, line=False, overwrite_old=True,
                 closing_diameter=6, pbimage=None, myresidual=None,
                 myimage=None, extension='.fullmask',
                 spectral_closing=3):
    """
    Makes a mask on any image you want it to.

    Parameters
    ----------
    imagename : {casa image without file extention}
        Name of image you want to mask, without the file extention.
    thresh : {float}
        Masking thershold in whatever units are using
    fl : {bool}
        If you want to combine the mask with a previous iteration of clean
        (True), if not (i.e. you are using the dirty image) then False.
    useimage : {bool}
        If you want to use the dirty image or the residual for the masking
        (I usually use the residual - so set to False)
    pixelmin : {float}
        Min number of pixels within a masked region to be taken into the final
        mask, i.e. if your beam size is 1arcsec and pixel size is 0.2 arcsec,
        then three beams would be pixelmin = 75
    major : {float}
        beam major axis, in arsec
    minor : {float}
        beam minor axis, in arsec
    pixelsize : {float}
        length of one side of pixel, in arcsec
    line : {bool}
        if the image is a line or continuum

    Returns
    -------
    mask : {ndarray}
        The final mask (hopefully) as the ".fullmask" image
    """

    mymask = imagename + '.mask'
    if myimage is None:
        myimage = imagename + '.image'
    maskim_nopb = imagename + '{}.nopb'.format(extension)
    maskim = imagename + extension
    threshmask = imagename + '.threshmask'
    if myresidual is None:
        myresidual = imagename + '.residual'
    if pbimage is None:
        pbimage = imagename + '.pb'

    if overwrite_old:
        os.system('rm -rf ' + maskim)
        os.system('rm -rf ' + maskim_nopb)
        os.system('rm -rf ' + threshmask)

    if useimage:
        print 'Using Image'
        immath(imagename=[myimage], outfile=threshmask,
            expr='iif(IM0 > ' + str(thresh) + ',1.0,0.0)')
    else:
        immath(imagename=[myresidual], outfile=threshmask,
            expr='iif(IM0 > ' + str(thresh) + ',1.0,0.0)')

    if fl:
        print 'Combining with previous mask..'
        immath(outfile=maskim_nopb, expr='iif(("' + threshmask + '" + "'
            + mymask + '") > 0.1,1.0,0.0)')
    else:
        print 'Making fresh new mask from image/residual'
        os.system('cp -r ' + threshmask + ' ' + maskim_nopb)

    immath(imagename=[pbimage, maskim_nopb], outfile=maskim,
        expr='iif(IM0 > 0.0, IM1, 0.0)')

    print "Using pixelmin=", pixelmin
    beamarea = (major * minor * np.pi / (4. * np.log(2.))) / (pixelsize**2)
    print 'Beam area', beamarea

    ia.open(maskim)
    mask = ia.getchunk()
    diam = closing_diameter  # Change for large beam dilation
    structure = np.ones((diam, diam))
    dist = ((np.indices((diam, diam)) - (diam - 1) / 2.)**2).sum(axis=0)**0.5
    # circularize the closing element
    structure[dist > diam / 2.] = 0

    if line:
        for k in range(mask.shape[3]):
            mask_temp = mask[:, :, 0, k]
            mask_temp = ndimage.binary_closing(mask_temp, structure=structure)
            labeled, j = ndimage.label(mask_temp)
            myhistogram = ndimage.measurements.histogram(labeled, 0, j + 1,
                                                         j + 1)
            object_slices = ndimage.find_objects(labeled)
            threshold = pixelmin

            for i in range(j):
                if myhistogram[i + 1] < threshold:
                    mask_temp[object_slices[i]] = 0.0

            mask[:, :, 0, k] = mask_temp

        # add an additional closing run, this time with a 3d (4d?) st. element
        structure_3d = np.ones((diam, diam, 1, spectral_closing))
        dist = ((np.indices((diam, diam)) - (diam - 1) / 2.)**2).sum(axis=0)**0.5
        # circularize the closing element
        dist_3d = np.repeat(dist[:, :, None, None], spectral_closing, axis=3)
        structure_3d[dist_3d > diam / 2.] = 0
        mask_closed = ndimage.binary_closing(mask, structure=structure_3d)
    else:
        raise RuntimeError("3D closing operation can only operate on cubes.")

    ia.putchunk(mask_closed.astype(int))
    ia.done()

    print 'Mask created.'
    return maskim
