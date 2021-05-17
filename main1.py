# 不考虑装修情况,配套设施

import pandas as pd
import numpy as np
from compare_vec import normalize_price, compare_vec, grade,normalize_housetype,\
    normalize_area,normalize_direction, normalize_floor, normalize_decoration, normalize_facility
from compare_vec import normalize_timecost
from vec2mat import get_weights


infile = './data/data.csv'
outfile = './data/result1.csv'

# 读取数据文件
data = pd.read_csv(infile)
w = {}

# 指定每个考察因素对应的标准化函数
f = {
    '价格':normalize_price,
    '房屋类型':normalize_housetype,
    '房屋面积':normalize_area,
    '朝向':normalize_direction,
    '楼层':normalize_floor,
    # '虹桥':normalize_timecost,
    # '镇坪路':normalize_timecost,
    # '南京东路':normalize_timecost,
    '耗时':normalize_timecost
}
dist_keys = ['虹桥','镇坪路','南京东路','东方体育中心']
data['耗时'] = data['虹桥']*2/24 +  data['镇坪路']*12/24 + data['南京东路'] *5/24 + data['东方体育中心'] *5/24
keys = ['价格','房屋类型','房屋面积','朝向','楼层','耗时']

for key in keys:
    n_data = f[key](data[key])
    ret = compare_vec(n_data,grade)
    w[key] = get_weights(ret)

# print(w)
# 价格、房屋类型、房屋面积、朝向、楼层、耗时

data1 = [
    [1,5,1,3,7,2],
    [0,1,1/5,1/2,3,1/2],
    [0,0,1,3,7,2],
    [0,0,0,1,3,1/3],
    [0,0,0,0,1,1/5],
    [0,0,0,0,0,1],
]

w0 = get_weights(np.array(data1))

ret = np.zeros_like(w['价格'],dtype=float)
for ind, key in enumerate(keys):
    ret += w0[ind]* w[key]

ret1 = pd.DataFrame(ret)
# print(ret1)
# with open('./result.txt','w') as fi:
#     fi.write(str(ret))
ret1.sort_values(by=0,ascending=False)
data['score']=ret1 

ret2 = data.sort_values(by='score',ascending=False)

cols = ['价格','房屋面积','房屋类型','朝向','楼层','装修情况','链接','配套设施_有','房屋标题','地点/小区','耗时','score'] + dist_keys
ret2[cols].to_csv(outfile)

