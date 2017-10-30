def moments(cycle, imagename):

    im = imagename+'.'+tc_list[cycle]+'.image'
    res = imagename+'.'+tc_list[cycle]+'.residual'

    immoments(imagename = im,
              moments = [8],
              outfile = im+'.mom8')

    imview(raster = {'file': im+'.mom8', 'colorwedge': True}, out = im+'.mom8.pdf')

    os.system('rm -rf '+im+'.mom8')

    immoments(imagename = res,
              moments = [8],
              outfile = res+'.mom8')

    imview(raster = {'file': res+'.mom8', 'colorwedge': True}, out = res+'.mom8.pdf')

    os.system('rm -rf '+res+'.mom8')
