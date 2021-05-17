from os import name
import csv

class Factors:
    def __init__(self, factors, cmp_mat):
        self.factors = factors
        for row, val in enumerate(cmp_mat):
            for col in range(0,row):
                cmp_mat[row][col] = 1/cmp_mat[col][row]
        self.cmp_mat = cmp_mat
        self.weights = get_weights(cmp_mat)


def get_weights(mat):
        """
        获取数据权值，返回权向量
        """
        import numpy as np
        rc = len(mat[0])
        data1 = np.array(mat)
            
        # 计算一致性指标CI
        lams, vecs = np.linalg.eig(data1)
        lams = np.abs(lams)
        maxlam = max(np.abs(lams))
        ind = -1
        for i,val in enumerate(lams):
            if maxlam == lams[i]:
                ind = i

        vec = abs(vecs[:,ind]/np.sum(vecs[:,ind]))
        CI = (maxlam-rc)/(rc-1)

        # RIs 定义, e.g. n=7时 RI=1.32
        RIs =[0,0,0.58,0.90,1.12,1.24,1.32,1.41,1.45,1.49,1.51]

        # CR定义 一致性比率
        CR = CI/ (RIs[rc] if rc<=10 else 1.6)
        print('最大lambda',maxlam)
        print('CI:',CI)
        print('CR:',CR)
        if CR < 0.1:
            print('不一致程度CR=%f, 在容许范围之内'% CR)
        else:
            print('不一致程度CR=%f, 不在容许范围内'% CR)
        # vec即为权向量
        ret = []
        for i in vec:
            ret.append(float(i))
        return ret




def compare_vec(data):
    """
    所有备选方案对每一个factor计算一个B矩阵
    """
    def compute_b_mat(vec):
        ret = []
        l = len(vec)
        for i in range(l):
            line = []
            for j in range(l):
                line.append(vec[i]/vec[j])
            ret.append(line)
        return ret
    r = len(data)
    c = len(data[0])
    b_mat_list = [None for i in range(c)]
    for j in range(c):
        vec = [data[i][j] for i in range(r)]
        b_mat_list[j] = compute_b_mat(vec)
    return b_mat_list

def compute_weights(b_mat_list):
    all_weights = []
    for b_mat in b_mat_list:
        ret = get_weights(b_mat)
        all_weights.append(ret)
    return all_weights
        
def compute_score(all_weights, a_weights):
    # print(all_weights)
    # print(a_weights)

    l1 = len(all_weights)
    l2 = len(all_weights[0])
    print(l1,l2)
    scores = []
    for j in range(l2):
        score = 0
        for i in range(l1):
            # print(i,j,all_weights[i][j],a_weights[i])
            score += all_weights[i][j] * a_weights[i]
        # print(score)
        # print('-----')
        scores.append(score)
    return scores

def integrate_scores(data,scores):
    data[0].append('得分')
    for i in range(1, len(data)):
        data[i].append(scores[i-1])
    
def process(data, factors):
    b_mat_list = compare_vec(data)
    all_weights = compute_weights(b_mat_list)
    scores = compute_score(all_weights, factors.weights)
    return scores

def normalize_price(prices):
    prices = [float(price) for price in prices]
    MAX_GRADE = 9
    MIN_GRADE = 1
    max_p = max(prices)
    min_p = min(prices)
    ret = [MAX_GRADE- (price-min_p)/(max_p-min_p)*(MAX_GRADE-MIN_GRADE)  for price in prices]
    return ret


def normalize_housetype(types):
    import re
    MAX_GRADE = 9
    MIN_GRADE = 1
    ret=[]
    def fun(x):
        ret = re.match(r'(\d)室(\d)厅(\d)卫',x)
        if ret != None:
            a1,a2,a3 = re.match(r'(\d)室(\d)厅(\d)卫',x).groups()
            return (2**int(a1)+2**int(a2) + 2**int(a3))/12.0*(MAX_GRADE-MIN_GRADE)+1
        return None

    for i in range(len(types)):
        try:
            result = fun(types[i])
            ret.append(result if result else 5)
        except:
            print(types[i])
            print(re.match(r'(\d)室(\d)厅(\d)卫',types[i]))
            print(fun(types[i]))
    return ret

def normalize_area(areas):
    MAX_GRADE = 9
    MIN_GRADE = 1
    ret = [float(ele) for ele in areas]
    max_p = max(ret)
    min_p = min(ret)
    ret = [(ele-min_p)/(max_p-min_p)*(MAX_GRADE-MIN_GRADE)+1 for ele in ret]
    return ret
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
    ret = []
    for i in range(len(directions)):
        ret.append(d[directions[i]])
    return ret
def normalize_floor(floors):
    d={
        '低楼层':1,
        '中楼层':2,
        '高楼层':3,
    }
    ret = []
    for i in range(len(floors)):
        f1, f2 = floors[i].split('/')
        temp = 0
        try:
            ff1 = int(f1)
            ff2 = int(f2)
            r = ff1/ff2
            if r <= 1/3:
                # 低楼层
                temp = d['低楼层']
            elif r<=2/3:
                # 中楼层
                temp = d['中楼层']
            else:
                temp = d['高楼层']
            ret.append(temp + ff2/15)
        except:
            ret.append(d[f1]+int(f2[:-1])/15)
    return ret

if __name__ == '__main__':

    col_names = ['价格','房屋类型','房屋面积','朝向','楼层']
    cmp_mat = [
        [1,3,1/2,2,7],
        [0,1,1/3,1/2,5],
        [0,0,1,3,7],
        [0,0,0,1,3],
        [0,0,0,0,1],
    ]
    # 指定每个考察因素对应的标准化函数
    mappings = {
        '价格':normalize_price,
        '房屋类型':normalize_housetype,
        '房屋面积':normalize_area,
        '朝向':normalize_direction,
        '楼层':normalize_floor,
    }
    factors = Factors(col_names, cmp_mat)

    infile = './data/data.csv'
    outfile = './data/result2.csv'
    
    oridata = []

    with open(infile) as f:
        count = -1
        f_csv = csv.reader(f)
        for row in f_csv:
            oridata.append([count] + row)
            count += 1

    data_temp = []
    for i in range(1,len(oridata)):
        d ={}
        for ind,key in enumerate(oridata[0]):
            d[key] = oridata[i][ind]
        data_temp.append(d)
    
    for key in factors.factors:
        vec = [line[key] for line in data_temp]
        vec1 = mappings[key](vec)
        for i in range(len(data_temp)):
            data_temp[i][key] = vec1[i]

    data = []
    for data_line in data_temp:
        line = []
        for key in factors.factors:
            line.append(data_line[key])
        data.append(line)








    
    # print(data)
    scores = process(data, factors)
    integrate_scores(oridata, scores)

    def takelast(ele):
        return -ele[-1]

    temp = oridata[1:]
    temp.sort(key=takelast)

    with open(outfile,'w') as f:
        f.write(','.join([str(x) for x in oridata[0]])+'\n')
        for line in temp:
            line = ','.join([str(x) for x in line])
            line = line +'\n'
            f.write(line)

    # with open('./data/temp.csv','w') as f:
    #     for line in data:
    #         line = ','.join([str(x) for x in line])
    #         line = line +'\n'
    #         f.write(line)

    

