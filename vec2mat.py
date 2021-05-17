import numpy as np
class Err(Exception):
    pass

def get_weights(data):
    """
    获取数据权值，返回权向量
    """

    rc = len(data[0])
    for i in range(rc):
        for j in range(i):
                data[i,j]=1/data[j,i]
        
    # 计算一致性指标CI
    lams, vecs = np.linalg.eig(data)
    # maxlam = np.abs(lams)[0]
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
    print(maxlam,CI,CR)

    if CR < 0.1:
        print('不一致程度CR=%f, 在容许范围之内'% CR)
    else:
        raise(Err('不一致程度CR=%f, 不在容许范围内'%CR))

    # ret = np.zeros_like(data1)
    # for i in range(rc):
    #     for j in range(rc):
    #         ret[i,j]=vec[i]/vec[j]
    
    # vec即为权向量
    # ret即为变换后的一致性矩阵
    return vec

if __name__ == "__main__":
    data = [
        [1,7,2,1/2,3,1/2,9],
        [0,1,1/5,1/5,1/7,1/3,1],
        [0,0,1,2,1,2,6],
        [0,0,0,1,2,3,6],
        [0,0,0,0,1,3,6],
        [0,0,0,0,0,1,6],
        [0,0,0,0,0,0,1]
    ]
    data1 = np.array(data)
    w = get_weights(data1)
    print(w)

