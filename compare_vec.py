import numpy as np
from functools import reduce
import re


def compare_vec(vec,grade_fun):
    """
    这里传入的应是经过规范化的vec
    """
    l = len(vec)
    ret = np.eye(l)
    for i in range(l):
        for j in range(l):
            ret[i,j] = grade_fun(vec[i],vec[j])
    return ret

def normalize_price(prices):
    MAX_GRADE = 9
    MIN_GRADE = 1
    max_p = max(prices)
    min_p = min(prices)
    return MAX_GRADE-(prices-min_p)/(max_p-min_p)*(MAX_GRADE-MIN_GRADE)

def normalize_housetype(types):
    MAX_GRADE = 9
    MIN_GRADE = 1
    ret = np.zeros_like(types,dtype=np.float)
    def fun(x):
        ret = re.match(r'(\d)室(\d)厅(\d)卫',x)
        if ret != None:
            a1,a2,a3 = re.match(r'(\d)室(\d)厅(\d)卫',x).groups()
            return (2**int(a1)+2**int(a2) + 2**int(a3))/12.0*(MAX_GRADE-MIN_GRADE)+1
        return None

    for i in range(len(types)):
        try:
            result = fun(types[i])
            ret[i] = result if result else 5
        except:
            print(types[i])
            print(re.match(r'(\d)室(\d)厅(\d)卫',types[i]))
            print(fun(types[i]))
    return ret

def normalize_area(areas):
    MAX_GRADE = 9
    MIN_GRADE = 1
    ret = np.zeros_like(areas,dtype=np.float)
    for i in range(len(areas)):
        if type(areas[i]) == str:
            ret[i] = areas[i][:-1]
        else:
            ret[i] = areas[i]
    max_p = max(ret)
    min_p = min(ret)
    return (ret-min_p)/(max_p-min_p)*(MAX_GRADE-MIN_GRADE)+1

def normalize_direction(directions):
    d={
        '南':9,
        '东南':8,
        '西南':6,
        '南/北':8,
        '东':6,
        '北':1,
        '西北/北':2,
        '西北':2,
        '南/西':5,
        '南/西南':6,
        '东南/东北':5,
        '东/东南':7,
        '西':3,
        '东北':4,
        '东/西':3,
        '东/南/西':6,
        '南/东北':5,
        '东/南':7,
        '西/北':2,
        '东/西/西北':6
    }
    ret = np.zeros_like(directions,dtype=np.float)
    for i in range(len(directions)):
        ret[i] = d[directions[i]]
    return ret

def normalize_floor(floors):
    d={
        '低楼层':1,
        '中楼层':2,
        '高楼层':3,
    }
    ret = np.zeros_like(floors,dtype=np.float)
    for i in range(len(floors)):
        f1, f2 = floors[i].split('/')
        try:
            ff1 = int(f1)
            ff2 = int(f2)
            r = ff1/ff2
            if r <= 1/3:
                # 低楼层
                ret[i] = d['低楼层']
            elif r<=2/3:
                # 中楼层
                ret[i] = d['中楼层']
            else:
                ret[i] = d['高楼层']
            ret[i] += ff2/15
        except:
            ret[i] = d[f1]+int(f2[:-1])/15
    return ret

def normalize_decoration(decorations):
    ret = np.zeros_like(decorations,dtype=np.float)
    for i in range(len(decorations)):
        ret[i] = 5 if decorations[i] else 1
    return ret

def normalize_facility(facilities):
    def fun(x):
        d = {
            '洗衣机':0,
            '空调':1,
            '衣柜':1,
            '冰箱':1,
            '热水器':1,
            '床':1,
            '天然气':1,
            '宽带':1,
            '电视':1,
            '暖气':0
        }
        return d[x]
    ret = np.zeros_like(facilities,dtype=np.float)
    for i in range(len(facilities)):
        if not facilities[i]:
            ret[i] = 1
            continue
        try:
            if type(facilities[i])==str:
                if facilities[i]=='自如':
                    ret[i] = 7
                    continue

                temp = map(fun, facilities[i].split(';'))
                ret[i] = reduce(lambda x,y: x+y,temp)
            else:
                ret[i] = 1
        except:
            print(type(facilities[i]))
            print(facilities[i])
    return ret

def grade(x,y):
    return x/y

if __name__ == "__main__":
    vec1 = np.array([4000,5500,4200,4500])
    vec2 = np.array(['2室1厅1卫','1室1厅1卫','2室0厅1卫'])
    vec3 = np.array(['56㎡','56㎡','55㎡'])
    vec4 = np.array(['南','东南','北'])
    vec5 = np.array(['中楼层/9层','低楼层/6层','高楼层/6层'])
    vec6 = np.array(['','精装修','','精装修'])
    vec7 = np.array(['洗衣机;空调;衣柜;冰箱;热水器;床;天然气','','衣柜;床;天然气'])
    normalize_price(vec1)
    normalize_housetype(vec2)
    normalize_area(vec3)
    normalize_direction(vec4)
    normalize_floor(vec5)
    normalize_decoration(vec6)
    normalize_facility(vec7)