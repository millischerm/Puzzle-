import File_Function as ff
import matplotlib.pyplot as plt
import numpy as np

def split_contour(corner, contour, len_contour):
    list_curve = []
    list_index = []
    for i in corner:
        list_index.append(contour.index(i))
    list_index.append(len_contour-1)
    for k in range(len(list_index)-1):
        start = list_index[k]
        stop = list_index[k+1]
        list_curve.append(contour[start:stop])
    start = 0
    stop = list_index[0]
    list_curve[-1] += contour[start:stop]
    return list_curve

def scatter_curve(curve,col,lab):
    x=[]
    y=[]
    for i in range(len(curve)):
        x.append(curve[i][1])
        y.append(curve[i][0])
    plt.scatter(x, y, c=col, label=lab)
    return True

def zero_curve(curve):
    x_init = curve[0][0]
    y_init = curve[0][1]
    for i in range(len(curve)):
        curve[i][0] -= x_init
        curve[i][1] -= y_init
    return curve, x_init, y_init

def rotate_curve(curve):
    x_last = curve[-1][0]
    y_last = curve[-1][1]
    v = np.array([[x_last],[y_last]])
    i = np.array([[0.0],[1.0]])
    j = np.array([[1.0],[0.0]])
    if np.sign(np.vdot(v, j)) == 0:
        theta = np.arccos(np.vdot(v, i)/np.linalg.norm(v))
    else:
        theta = np.arccos(np.vdot(v, i)/np.linalg.norm(v))*np.sign(np.vdot(v, j))
    c = np.cos(theta)
    s = np.sin(theta)
    R = np.array([[c,-s],[s, c]])
    for i in range(len(curve)):
        x = curve[i][0]
        y = curve[i][1]
        v = np.array([[x],[y]])
        vr = np.dot(R,v)
        curve[i][0] = vr[0][0]
        curve[i][1] = vr[1][0]
    return curve, R

def slope(curve):
    x = []
    y = []
    step = 30
    for i in range(step,len(curve)-step):
        x.append(i)
        y.append((curve[i+step][0]-curve[i-step][0])/(step*2))
    return x,y

def center(corner):
    g = np.array([[0.0],[0.0]])
    for cor in corner:
        g[0][0] += cor[0]
        g[1][0]+= cor[1]
    g[0][0] = g[0][0]/len(corner)
    g[1][0] = g[1][0]/len(corner)
    return g

def orientation(curves, corner):
    # this function orients the curve in the right position the center of mass of the piece has to be under the curve, if it not then flip all the curve.
    gis=0.0
    for k, curve in enumerate(curves):
        g = center(corner)
        gi = g
        curve, x, y = zero_curve(curve)
        curve, R = rotate_curve(curve)
        gi[0][0] -= x
        gi[1][0] -= y
        gi = np.dot(R,gi)
        gis+=gi[1][0]
    if gis > 0.0:
        for curve in curves:
            for y in curve:
                y[0]=-y[0]
    return curves

def bulb_or_hole(curve):
    center = 0
    for y in curve:
        center += y[0]
    if center > 0:
        return 'bulb'
    else:
        return 'hole'

def reverse_bulb(curves):
    for curve in curves:
        if bulb_or_hole(curve) == 'bulb':
            for point in curve:
                point[1] = -point[1]
            curve.reverse()
            zero_curve(curve)
    return curves

def get_curves(dir,piece):
    dir_corner = dir + 'CORNER/'
    dir_contour = dir + 'CONTOUR/'
    dir_curves = dir + 'CURVES/'
    type = '.txt'
    color = ['r', 'b', 'g', 'm']


    corner = ff.extract_data(dir_corner + piece + type)
    len_corner = ff.len_file(dir_corner + piece + type)
    contour = ff.extract_data(dir_contour + piece + type)
    len_contour = ff.len_file(dir_contour + piece + type)


    curves = split_contour(corner, contour, len_contour)
    g = center(corner)
    curves = orientation(curves, corner)
    curves = reverse_bulb(curves)

    for k, curve in enumerate(curves):
        name_curve = piece + '_C' + str(k) + '_' + bulb_or_hole(curve)
        ff.save_list_point(curve, dir_curves, name_curve, type)
    return curves

dir = '/Users/martin/puzzle/project_puzzle/Math_Research/PIECE/'
piece = 'P4'

curves = get_curves(dir, piece)
