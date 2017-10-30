execfile('masking_function.py')

def run_clean(cycle_list, vis, imagename, imsize, cell, phasecenter, niter_list, tc_list, restfreq, threshold_list, rms_list, fl_list, useimage_
list, pixelmin_list, major, minor, pixelsize, overwrite_old = False,
              datacolumn = 'data', field = '', stokes = 'I', projection = 'SIN', specmode = 'cube', nchan = -1, width = 1, start = 0, outframe =
 'LSRK',
              veltype = 'radio', interpolation = 'linear', gridder = 'mosaic', pblimit = 0.2, normtype = 'flatnoise', deconvolver = 'multiscale'
, scales = [0, 7, 21, 63], restoringbeam  = [], outlierfile = '', weighting = 'natural',
              uvtaper = [], gain = 0.1, cycleniter = -1, cyclefactor = 1.0, minpsffraction = 0.05, maxpsffraction = 0.8, interactive = False, sa
vemodel = 'none', calcres = True, calcpsf = True, parallel = False):

    #Makes dirty image
    if 0 in cycle_list:
        print 'Making dirty'
        cycle = 0; mask = ''; startmodel = ''
        tclean(vis       = vis,
               datacolumn     = datacolumn,
               imagename      = imagename+'.'+tc_list[cycle],
               imsize         = imsize,
               cell           = cell,
               phasecenter    = phasecenter,
               stokes         = stokes,
               field          = field,
               projection     = projection,
               startmodel     = startmodel,
               specmode       = specmode,
               nchan          = nchan,
               start          = start,
               width          = width,
               outframe       = outframe,
               veltype        = veltype,
               restfreq       = restfreq,
               interpolation  = interpolation,
               gridder        = gridder,
               pblimit        = pblimit,
               normtype       = normtype,
               deconvolver    = deconvolver,
               scales         = scales,
               restoringbeam  = restoringbeam,
               outlierfile    = outlierfile,
               weighting      = weighting,
               uvtaper        = uvtaper,
               niter          = niter_list[cycle],
               gain           = gain,
               threshold      = threshold_list[cycle],
               cycleniter     = cycleniter,
               cyclefactor    = cyclefactor,
               minpsffraction = minpsffraction,
               maxpsffraction = maxpsffraction,
               interactive    = interactive,
               mask           = mask,
               savemodel      = savemodel,
               calcres        = calcres,
               calcpsf        = calcpsf,
               parallel       = parallel)

    #Cleaning up the dir

    os.system('rm -rf '+imagename+'.'+tc_list[cycle]+'.weight')
    os.system('rm -rf '+imagename+'.'+tc_list[cycle]+'.model')
    os.system('rm -rf '+imagename+'.'+tc_list[cycle]+'.psf')
    os.system('rm -rf '+imagename+'.'+tc_list[cycle]+'.sumwt')

    #Makes mask and cleans
    for cycle in cycle_list:
        if cycle == 0:
            continue

        mask = make_mask_3d(imagename+'.'+tc_list[cycle-1], rms_list[cycle], fl = fl_list[cycle], useimage = useimage_list[cycle], pixelmin = pi
xelmin_list[cycle], major = major, minor = minor, pixelsize = pixelsize, line = True, overwrite_old = overwrite_old)
        startmodel = ''
        if startmodel_list[cycle]:
            startmodel = dir_line+'.'+tc_list[cycle-1]+'.model'

        tclean(vis       = vis,
               datacolumn     = datacolumn,
               imagename      = imagename+'.'+tc_list[cycle],
               imsize         = imsize,
               cell           = cell,
               phasecenter    = phasecenter,
               stokes         = stokes,
               field          = field,
               projection     = projection,
               startmodel     = startmodel,
               specmode       = specmode,
               nchan          = nchan,
               start          = start,
               width          = width,
               outframe       = outframe,
               veltype        = veltype,
               restfreq       = restfreq,
               interpolation  = interpolation,
               gridder        = gridder,
               pblimit        = pblimit,
               normtype       = normtype,
               deconvolver    = deconvolver,
               scales         = scales,
               restoringbeam  = restoringbeam,
               outlierfile    = outlierfile,
               weighting      = weighting,
               uvtaper        = uvtaper,
               niter          = niter_list[cycle],
               gain           = gain,
               threshold      = threshold_list[cycle],
               cycleniter     = cycleniter,
               cyclefactor    = cyclefactor,
               minpsffraction = minpsffraction,
               maxpsffraction = maxpsffraction,
               interactive    = interactive,
               mask           = mask,
               savemodel      = savemodel,
               calcres        = calcres,
               calcpsf        = calcpsf,
               parallel       = parallel)

        os.system('rm -rf '+imagename+'.'+tc_list[cycle]+'.weight')
        os.system('rm -rf '+imagename+'.'+tc_list[cycle]+'.model')
        os.system('rm -rf '+imagename+'.'+tc_list[cycle]+'.psf')
        os.system('rm -rf '+imagename+'.'+tc_list[cycle]+'.sumwt')
        os.system('rm -rf '+imagename+'.'+tc_list[cycle-1]+'.threshmask')
        os.system('rm -rf '+imagename+'.'+tc_list[cycle-1]+'.fullmask')
        os.system('rm -rf '+imagename+'.'+tc_list[cycle-1]+'.fullmask.nopb')
