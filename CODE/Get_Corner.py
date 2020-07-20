import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import Modify_Image as mod
import Combinations_Corner as cc

def init_pixel(piece):
    p_w = piece.shape[1]
    p_h = piece.shape[0]-1
    k = 0
    scan = True
    while piece[p_h][k][0] == piece[p_h][k+1][0] and scan:
        if k == p_w-2:
            if p_h == 0:
                scan = False
                print('The Image is entirely white')
            else:
                p_h = p_h - 1
                k = 0
        else:
            k += 1
    if scan:
        return p_h, k+1

def next_point(piece, y_init, x_init, ccw):
    l_x = [1, 1, 0, -1, -1, -1, 0, 1]
    l_y = [0, 1, 1, 1, 0, -1, -1, -1]
    for i in range(8):
        l_x[i] += x_init
        l_y[i] += y_init
    k = 0
    if ccw:
        while piece[l_y[k]][l_x[k]][0] == piece[l_y[k+1]][l_x[k+1]][0]:
            k += 1
        if piece[l_y[k]][l_x[k]][0] == 0:
            return l_y[k], l_x[k]
        else:
            return l_y[k+1], l_x[k+1]
    else:
        while piece[l_y[k]][l_x[k]][0] == piece[l_y[k-1]][l_x[k-1]][0]:
            k -= 1

        if piece[l_y[k]][l_x[k]][0] == 0:
            return l_y[k], l_x[k]
        else:
            return l_y[k-1], l_x[k-1]

def Contour(piece, y_init, x_init, dir_Contour, name):
    file = open(dir_Contour+name+'.txt','w')
    contour = []
    cont = True
    k = 0
    y, x = next_point(piece, y_init, x_init, True)
    plt.scatter(x, y, s=0.1, c='r')
    print(y, x)
    while cont:
        y1, x1 = next_point(piece, y, x, True)
        if [y1, x1] in contour:
            y1, x1 = next_point(piece, y, x, False)
            if [y1, x1] in contour:
                cont = False
        file.write(str(y1))
        file.write('\t')
        file.write(str(x1))
        file.write('\n')
        contour.append([y1, x1])
        plt.scatter(x1, y1, s=0.1, c='r')
        y, x= y1, x1
        k +=1
        # if k > 2000:
        #     cont = False
    return contour

def Circle(y, x, r):
    circle =[]
    for i in range(360):
        a=i*2*np.pi/360
        xc = int(r*np.cos(a))+x
        yc = int(r*np.sin(a))+y
        if not([yc, xc] in circle):
            circle.append([yc, xc])
            # plt.scatter(xc,yc,s=0.5,c='b')
    return circle

def Weight_circle(piece, y, x, r):
    circle = Circle(y, x, r)
    w = 0
    for i in range(len(circle)):
        yc = circle[i][0]
        xc = circle[i][1]
        if piece[yc][xc][0]==0.0:
            w += 1
    return w

def fisrt_corner_point(piece,min_we,r,num_corn):
    w_corner = []
    coord_corner = []
    sub_w_corner = []
    sub_coord_corner = []
    corner_f = False

    for coord in contour:
        we = Weight_circle(piece, coord[0], coord[1], r)
        if we <= min_we:
            corner_f = True
            sub_w_corner.append(we)
            sub_coord_corner.append([coord[0], coord[1]])
        elif we > min_we and corner_f:
            if len(sub_coord_corner)>num_corn:
                corner_f = False
                w_corner.append(min(sub_w_corner))
                ind = sub_w_corner.index(min(sub_w_corner))
                coord_corner.append([sub_coord_corner[ind][0],sub_coord_corner[ind][1]])
                sub_w_corner = []
                sub_coord_corner = []
                # plt.scatter(coord_corner[-1][1],coord_corner[-1][0],c='g')
            else:
                sub_w_corner = []
                sub_coord_corner = []
    return coord_corner

dir = '/Users/martin/puzzle/project_puzzle/Math_Research/PIECE/'
dir_Image = dir + 'IMAGE/'
dir_Contour = dir + 'CONTOUR/'
dir_Corner = dir + 'CORNER/'
name = 'P4'
type = '.png'

name_tn = mod.Thumb_Nail(dir_Image, name, type, 400)

name_bnw = mod.Black_n_White(dir_Image, name_tn, type, 0.4)

P1 = mpimg.imread(dir_Image + name_bnw + type)

print('shape ', P1.shape)

y_init, x_init = init_pixel(P1)

contour = Contour(P1, y_init, x_init, dir_Contour,name)
r=15
Circle(y_init, x_init, r)

coord_corner = fisrt_corner_point(P1, 40, r,8)

if len(coord_corner)<4:
    coord_corner = fisrt_corner_point(P1, 40, r,3)


final_corner = cc.get_corner_area(coord_corner)
file_corner = open(dir_Corner + name + '.txt','w')

for coord in final_corner:
    plt.scatter(coord[1],coord[0], c='g')
    file_corner.write(str(coord[0]))
    file_corner.write('\t')
    file_corner.write(str(coord[1]))
    file_corner.write('\n')


# print(Weight_circle(P1, 87, 38, 7))


plt.imshow(P1)
plt.show()

