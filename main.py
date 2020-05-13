import pandas as pd
import numpy as np
from compare_vec import normalize_price, compare_vec, grade,normalize_housetype,\
    normalize_area,normalize_direction, normalize_floor, normalize_decoration, normalize_facility
from vec2mat import get_weights
data = pd.read_csv('./mydbase.csv')
w = {}
f = {
    '价格':normalize_price,
    '房屋类型':normalize_housetype,
    '房屋面积':normalize_area,
    '朝向':normalize_direction,
    '楼层':normalize_floor,
    '装修情况':normalize_decoration,
    '配套设施_有':normalize_facility,
}

keys = ['价格','房屋类型','房屋面积','朝向','楼层','装修情况','配套设施_有']
for key in keys:
    n_data = f[key](data[key])
    ret = compare_vec(n_data,grade)
    w[key] = get_weights(ret)

data1 = [
    [1,7,2,1/2,3,1,9],
    [0,1,1/5,1/5,1/7,1/3,1/2],
    [0,0,1,2,1,2,7],
    [0,0,0,1,2,3,6],
    [0,0,0,0,1,3,6],
    [0,0,0,0,0,1,6],
    [0,0,0,0,0,0,1]
]
w0 = get_weights(np.array(data1))

ret = np.zeros_like(w['价格'],dtype=float)
for ind, key in enumerate(keys):
    ret += w0[ind]* w[key]
# print(ret)
ret1 = pd.DataFrame(ret)
# print(ret1)
# with open('./result.txt','w') as fi:
#     fi.write(str(ret))
ret1.sort_values(by=0,ascending=False)
data['score']=ret1 

ret2 = data.sort_values(by='score',ascending=False)
cols = ['价格','房屋面积','房屋类型','房源Id','朝向','楼层','装修情况','链接','配套设施_无','配套设施_有','房屋标题','租赁方式','房源描述','房源维护时间','score']

ret2[cols].to_csv('./result.csv')