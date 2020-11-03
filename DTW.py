import sys
import numpy as np

def euclidean_distance(x,y):
    sum=0
    for i in range(len(x)):
        sum+=(x[i]-y[i])**2
    return sum**0.5

def cal_dtw_distance(ts_a, ts_b):
    """Returns the DTW similarity distance between two 2-D
    timeseries numpy arrays.

    Arguments
    ---------
    ts_a, ts_b : array of shape [n_samples, n_timepoints]
        Two arrays containing n_samples of timeseries data
        whose DTW distance between each sample of A and B
        will be compared

    d : DistanceMetric object (default = abs(x-y))
        the distance measure used for A_i - B_j in the
        DTW dynamic programming function

    Returns
    -------
    DTW distance between A and B
    """
    d = lambda x, y: abs(x - y)
    max_warping_window = 10000

    # Create cost matrix via broadcasting with large int
    ts_a, ts_b = np.array(ts_a), np.array(ts_b)
    M, N = len(ts_a), len(ts_b)
    cost = sys.maxsize * np.ones((M, N))

    # Initialize the first row and column
    cost[0, 0] = d(ts_a[0], ts_b[0])
    for i in range(1, M):
        cost[i, 0] = cost[i - 1, 0] + d(ts_a[i], ts_b[0])

    for j in range(1, N):
        cost[0, j] = cost[0, j - 1] + d(ts_a[0], ts_b[j])

    # Populate rest of cost matrix within window
    for i in range(1, M):
        for j in range(max(1, i - max_warping_window),
                       min(N, i + max_warping_window)):
            choices = cost[i - 1, j - 1], cost[i, j - 1], cost[i - 1, j]
            cost[i, j] = min(choices) + d(ts_a[i], ts_b[j])

    # Return DTW distance given window
    return cost[-1, -1]


#加速度
def acceleration_x_y_z(data_1st):
    data_1st = list(data_1st)
    data = []
    count = 1
    for i in range(len(data_1st)):
        data_2nd = []
        if i < len(data_1st) - 1:
            if data_1st[i][-1] == data_1st[i + 1][-1]:
                count += 1
                data_1st[i + 1][0] = data_1st[i][0] + data_1st[i + 1][0]
                data_1st[i + 1][1] = data_1st[i][1] + data_1st[i + 1][1]
                data_1st[i + 1][2] = data_1st[i][2] + data_1st[i + 1][2]
            else:
                data_2nd.append(data_1st[i][0] / count)
                data_2nd.append(data_1st[i][1] / count)
                data_2nd.append(data_1st[i][2] / count)
                data_2nd.append(data_1st[i][-1])
                count = 1
                data.append(data_2nd)
        else:
            data_2nd.append(data_1st[i][0] / count)
            data_2nd.append(data_1st[i][1] / count)
            data_2nd.append(data_1st[i][2] / count)
            data_2nd.append(data_1st[i][-1])
            data.append(data_2nd)
    # print(data)


    t = []
    x = []
    y = []
    z = []
    Handle=[]
    for i in range(len(data)):
        x.append(data[i][0])
        y.append(data[i][1])
        z.append(data[i][2])
        #Handle.append((data[i][0]**2+data[i][1]**2+data[i][2]**2)**0.5)
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    return x,y,z
    #Handle=np.array(Handle)

if __name__ == "__main__":
    data_xiaomi6 = np.loadtxt('静止水平靠近10-立定状态-2020-09-28_04-53-16/acceleration.txt',dtype=np.float64, delimiter=',')
    data_huaweiP20 = np.loadtxt('静止水平靠近10-立定状态-2020-10-09_07-30-04/acceleration.txt',dtype=np.float64, delimiter=',')
    data_xiaomi6_new=np.loadtxt('静止水平接电话10-立定状态-2020-09-28_05-45-02/acceleration.txt',dtype=np.float64, delimiter=',')
    ts_xiaomi6=data_xiaomi6[:,[0,1,2]]
    ts_huaweiP20=data_huaweiP20[:,[0,1,2]]
    ts_xiaomi6_new=data_xiaomi6_new[:,[0,1,2]]
    ts_xiaomi6_x,ts_xiaomi6_y,ts_xiaomi6_z=acceleration_x_y_z(data_xiaomi6)
    ts_huaweiP20_x,ts_huaweiP20_y,ts_huaweiP20_z=acceleration_x_y_z(data_huaweiP20)
    ts_xiaomi6_new_x,ts_xiaomi6_new_y,ts_xiaomi6_new_z=acceleration_x_y_z(data_xiaomi6_new)
    d1_x=cal_dtw_distance(ts_xiaomi6_x,ts_huaweiP20_x)
    d1_y=cal_dtw_distance(ts_xiaomi6_y,ts_huaweiP20_y)
    d1_z=cal_dtw_distance(ts_xiaomi6_z,ts_huaweiP20_z)

    d2_x = cal_dtw_distance(ts_xiaomi6_x, ts_xiaomi6_new_x)
    d2_y = cal_dtw_distance(ts_xiaomi6_y, ts_xiaomi6_new_y)
    d2_z = cal_dtw_distance(ts_xiaomi6_z, ts_xiaomi6_new_z)
    print(d1_x,d1_y,d1_z)
    print(d2_x,d2_y,d2_z)
    #distance1=cal_dtw_distance(ts_xiaomi6,ts_huaweiP20)
    #distance2= cal_dtw_distance(ts_xiaomi6, ts_xiaomi6_new)
    #print(distance1)
    #print(distance2)
