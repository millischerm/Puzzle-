import numpy as np

def extract_data(dir):
    len_list = len_file(dir)
    data = [[0,0] for k in range(len_list)]
    file = open(dir)
    for i in range(len_list):
        coord = file.readline().split('\t')
        for j in range(2):
            data[i][j]= int(coord[j])
    return data


def len_file(dir):
    file=open(dir)
    rl=file.readline()
    len_f=0
    while rl!='':
        len_f+=1
        rl=file.readline()
    return len_f

def save_list_point(list, dir, name, type):
    file = open(dir + name + type,'w')
    for point in list:
        file.write(str(point[0]))
        file.write('\t')
        file.write(str(point[1]))
        file.write('\n')
    return True


