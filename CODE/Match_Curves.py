import Get_Curves
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import os

dir = '/Users/martin/puzzle/project_puzzle/Math_Research/PIECE/'
dir_curves = dir + 'CURVES/'

p=Path(dir_curves)
files = []
for entry in os.scandir(p):
    if entry.is_file():
        files.append(entry)

List_curves = []

for i in range(4):
    piece = 'P'+str(i+1)
    curves = Get_Curves.get_curves(dir, piece)
    for curve in curves:
        List_curves.append(curve)

Holes =[]
Bulbs = []
color = ['r','b','m','c','k','g','y','aqua','coral','gold','grey','lime','navy','plum','tan']


for curve in List_curves:
    if Get_Curves.bulb_or_hole(curve) == 'hole':
        Holes.append(curve)
    elif Get_Curves.bulb_or_hole(curve) == 'bulb':
        for pts in curve:
            pts[0] = -pts[0]
        Bulbs.append(curve)

for k, curve in enumerate(List_curves):
    print(k)
    x, y = Get_Curves.slope(curve)
    # plt.plot(x, y, color[k], label=str(files[k+1])[11:21])
    Get_Curves.scatter_curve(curve, color[k], str(files[k+1])[11:21])
    plt.legend()
puzzle_Matrix = np.zeros((len(Holes), len(Bulbs)))

for i,curve_h in enumerate(Holes):
    for j,curve_b in enumerate(Bulbs):
        diff = 0
        len_diff = min(len(curve_h), len(curve_b))
        for k in range(len_diff):
            diff += abs(curve_h[k][0] - curve_b[k][0])
        puzzle_Matrix[i][j] = diff

print(puzzle_Matrix)



plt.show()
