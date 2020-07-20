from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def Thumb_Nail(dir, name, type, dim):
    img = Image.open(dir+name+type)
    img.thumbnail((dim, dim), Image.ANTIALIAS)
    img.save(dir+name+'_tn.png')
    return name+'_tn'

def Black_n_White(dir, name, type, intensity):
    im = mpimg.imread(dir + name + type)
    im_w = im.shape[1]
    im_h = im.shape[0]

    for i in range(im_w):
        for j in range(im_h):
            if im[j][i][0] > intensity:
                im[j][i][0] = 1.0
                im[j][i][1] = 1.0
                im[j][i][2] = 1.0
            else:
                im[j][i][0] = 0.0
                im[j][i][1] = 0.0
                im[j][i][2] = 0.0
    plt.imshow(im)
    plt.imsave(dir + name + '_bnw' + type, im)
    print(name+'_bnw')
    return name + '_bnw'
