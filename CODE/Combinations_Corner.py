import itertools


def area(quad):
    A=quad[0]
    B=quad[1]
    C=quad[2]
    D=quad[3]
    q1=A[0]*B[1]+B[0]*C[1]+C[0]*D[1]+D[0]*A[1]
    q2=A[1]*B[0]+B[1]*C[0]+C[1]*D[0]+D[1]*A[0]
    return abs((q1-q2)/2)

def get_corner_area(l):
    if len(l) < 4:
        return l
    else:
        Area=[]
        corner_seq =[]


        for p in itertools.combinations(l,4):
            a = area(p)
            Area.append(a)
            corner_seq.append(p)

        m = max(Area)
        k = Area.index(m)
        return corner_seq[k]
