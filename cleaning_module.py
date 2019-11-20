### Note that as for Nov. 2019 this code is completely untested and may not function with the newest version of casa
### Use at own risk! 

execfile('masking_function.py')

def run_cubeclean(vis, imagename, imsize, cell,
                phasecenter='', restfreq='',
                nchan=-1, width=1, start=0,
                datacolumn='data', parallel=False,
                mk_dirty=True, n_cycles=5):

    ''' Code to conduct basic *cube* cleaning of ALMA data in CASA
        Input:
            [Required]
            vis = Input .ms file
            imagename = Output full path imagename, without extension (e.g. without .image)
            imsize = Size of image in pixels
            cell = Size of cell in arcsec
            [optional]
            phasecenter = Phasecenter for imaging; default is nothing, but not sure if will run without
            restfreq = frequency of line to be imaged, default is nothing, but not sure if will run without
            nchan = number of channels to be imaged: default is all,
            width = width of channels to be imaged: default is 1 channel,
            start = start of channels to be imaged: default is channle 0,
            datacolumn = column in .ms to be imaged; default is 'data' column,
            parallel = conduct clean in parallel; default is False,
            mk_dirty = make the dirty image as first step; default is True,
        Return
            None
                    '''

    #multiscale scales
    scales = [0, 7, 21, 63]

    #Makes dirty image
    if mk_dirty:

        dirtyimage = '%s_dirty' %imagename
        print '[INFO] Making dirty image: %s' %outimage

        tclean(vis            = vis,
               datacolumn     = 'data',
               imagename      = dirtyimage,
               imsize         = imsize,
               cell           = cell,
               phasecenter    = phasecenter,
               specmode       = 'cube',
               nchan          = nchan,
               start          = start,
               width          = width,
               outframe       = 'LSRK',
               restfreq       = restfreq,
               gridder        = 'mosaic',
               deconvolver    = 'multiscale',
               scales         = scales,
               niter          = 0,
               interactive    = False,
               parallel       = parallel)

    #Cleaning up the dir
    print '[INFO] Cleaning output dir.'
    os.system('rm -rf %s.weight' %dirtyimage)
    os.system('rm -rf %s.model' %dirtyimage)
    os.system('rm -rf %s.psf' %dirtyimage)
    os.system('rm -rf %s.sumwt' %dirtyimage)

    # define thresholds, from 10 to 1
    threshs = np.linspace(10, 1, 5)

    #Makes mask and cleans
    for cycle in range(n_cycles):

        previmage = '%s_cycle%i' %(imagename, cycle-1)
        outimage = '%s_cycle%i' %(imagename, cycle)
        print '[INFO] Cleaning cycle %i' %cycle
        print '[INFO] Making image: %s' %outimage

        header = imhead(imagename=dirtyimage)
        major = header['restoringbeam']['major']['value']
        minor = header['restoringbeam']['minor']['value']
        beam_area = major*minor
        pixel_area = cell**2
        beam_pixel_ratio = beam_area/pixel_area

        thresh = threshs[cycle]
        print '[INFO] Cycle thresh: %0.2f rms' %thresh

        if cycle == 0:

            dirtyimage = '%s.image' %dirtyimage
            stats = imstat(imagename = dirtyimage_)
            mad = stat['medabsdevmed']
            print '[INFO] Cycle rms: %g Jy/beam' %mad

            mask = make_mask_3d(imagename = dirtyimage,
                                thresh = thresh,
                                fl = False,
                                useimage = True,
                                pixelmin = beam_pixel_ratio*3,
                                major = major,
                                minor = minor,
                                pixelsize = cell,
                                line = True,
                                overwrite_old = False)

            startmodel =  ''
            print '[INFO] No model - okay?'

        else:

            previmage_ = '%s.image' %previmage
            stats = imstat(imagename=previmage_)
            mad = stat['medabsdevmed']
            print '[INFO] Cycle rms: %g Jy/beam' %mad

            mask = make_mask_3d(imagename = previmage,
                                thresh = thresh,
                                fl = True,
                                useimage = False,
                                pixelmin = beam_pixel_ratio*3,
                                major = major,
                                minor = minor,
                                pixelsize = cell,
                                line = True,
                                overwrite_old = False)

            startmodel = '%s.model' %previmage
            print '[INFO] Using model: %s' %startmodel

        tclean(vis            = vis,
               datacolumn     = 'data',
               imagename      = outimage,
               imsize         = imsize,
               cell           = cell,
               phasecenter    = phasecenter,
               specmode       = 'cube',
               nchan          = nchan,
               start          = start,
               width          = width,
               outframe       = 'LSRK',
               restfreq       = restfreq,
               gridder        = 'mosaic',
               deconvolver    = 'multiscale',
               scales         = scales,
               niter          = 1000000,
               threshold      = thresh*mad,
               interactive    = False,
               mask           = mask,
               startmodel     = startmodel,
               parallel       = parallel)

        os.system('rm -rf %s.weight' %outimage)
        os.system('rm -rf %s.model' %outimage)
        os.system('rm -rf %s.psf' %outimage)
        os.system('rm -rf %s.sumwt' %outimage)
        os.system('rm -rf %s.threshmask' %previmage)
        os.system('rm -rf %s.fullmask' %previmage)
        os.system('rm -rf %s.fullmask.nopb' %previmage)

        return
